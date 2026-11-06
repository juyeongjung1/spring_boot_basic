"""表示される独立図を、章・節・節内連番で採番する。"""
from collections import Counter
import json
from pathlib import Path
import re

from code_geometry import code_geometries


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# ファイル名画像と、HTMLコード枠で文字に戻した注記は独立図ではない。
TEXT_NOTES = {('03', 'p071-f08'), ('03', 'p113-f50')}


def chapter_key(config):
    if config.get('kind') == 'front':
        return 'ex-front' if config['pdf'].find('-L1-') >= 0 else 'front'
    if config.get('kind') == 'back':
        return 'ex-back'
    number = config['chapter']
    if config.get('kind') == 'exercise':
        return f'ex{int(number):02d}'
    return f'{number:02d}' if isinstance(number, int) else str(number)


def figure_numbers(config, layout, nodes, figures, order):
    """現行Markdownの順序から、独立図だけの番号と表示情報を返す。"""
    chapter = chapter_key(config)
    folder = ROOT / 'docs/textbook/chapters' / chapter
    appendix = chapter.startswith('appendix-')
    prefix = chapter.rsplit('-', 1)[-1].upper() if appendix else str(config['chapter'])
    if config.get('kind') == 'exercise':
        prefix = 'E' + prefix
    originals = {f['id']: f for f in layout['figures']}
    labels = json.loads((HERE / 'filename_labels.json').read_text(encoding='utf-8'))
    omitted = {r['figure_id'] for r in labels if r['chapter'] == chapter}
    omitted |= {ident for ch, ident in TEXT_NOTES if ch == chapter}
    attached = ({ident for geometry in code_geometries(folder, layout, nodes).values()
                 for ident in geometry.get('figure_ids', [])}
                if any(n['kind'] == 'code' for n in nodes.values()) else set())
    cover = set(order[0]['entries']) if config.get('cover_mode', 'classic') != 'none' else set()
    compact = config.get('illustrations', {})
    section, appendix_section, counts, result = 1, 0, Counter(), {}
    for page in order:
        for ident in page['entries']:
            if ident in nodes and ident not in cover and nodes[ident]['kind'] == 'heading':
                text = nodes[ident]['text'].strip()
                match = re.match(r'(?:演習\s*)?(\d+)\s*\.\s*(\d+)(?:\s*\.|\s|$)', text)
                if not appendix and match and int(match[1]) == int(config['chapter']):
                    section = int(match[2])
                elif appendix and not re.search(r'【\s*参考\s*】', text):
                    styles = [layout['styles'].get((style or '').split(':')[-1], {})
                              for value, style in nodes[ident]['parts'] if value.strip()]
                    if any(style.get('size', 0) >= 14 for style in styles):
                        appendix_section += 1
                        section = appendix_section
            if ident not in figures or ident in cover or ident in omitted:
                continue
            original = originals.get(ident, {})
            if original.get('slide'):
                continue
            counts[section] += 1
            options = compact.get(ident, {})
            caption_id = options.get('caption_id')
            kind = ('compact' if ident in compact else
                    'native' if page['source_page'] in config.get('native_pages', []) else
                    'code' if ident in attached else 'flow')
            result[ident] = dict(number=f'図{prefix}.{section}.{counts[section]}', kind=kind,
                                 caption_id=caption_id,
                                 caption=nodes[caption_id]['text'] if caption_id else '', title='')
    return result


def native_number_box(ident, number, page, layout):
    """固定図の左右の空きへ番号タブを置く。原図の座標は変えない。"""
    figure = next(f for f in layout['figures'] if f['id'] == ident)
    x0, y0, x1, y1 = figure['box']
    width, height = 48, 15
    obstacles = [r['bbox'] for block in layout['blocks'].values()
                 if block['source_page'] == page['source_page']
                 for line in block['lines'] for r in line.get('runs', []) if r.get('bbox')]
    obstacles += [r['bbox'] for r in page['furniture'] if r.get('bbox')]
    obstacles += [[f['box'][0]-4, f['box'][1]-4, f['box'][2]+4, f['box'][3]+4]
                  for f in layout['figures'] if f['page'] == page['source_page'] and f['id'] != ident]
    def free(box):
        return (box[0] >= 5 and box[2] <= 590 and box[1] >= 5 and box[3] <= 836
                and not any(min(box[2], r[2])-max(box[0], r[0]) > 0
                            and min(box[3], r[3])-max(box[1], r[1]) > 0 for r in obstacles))
    for top in [y0+5, y1-height-5]:
        for left in [x1+4, x0-4-width]:
            box = [left, top, left+width, top+height]
            if free(box):
                return box
    raise ValueError(f'固定図の番号を安全に配置できません: {ident} {number}')
