"""同じMarkdownから元位置再現版と自動組版版を生成し、元PDFと照合する。"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import quote, unquote

import pymupdf as fitz
import typst
from PIL import Image, ImageChops, ImageStat
from links import add_url_links
from code_geometry import code_geometries
from figure_numbers import figure_numbers, native_number_box
from table_styles import table_paint, table_geometry
import html_components

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FONT_FILES = ["msgothic.ttc", "msmincho.ttc", "meiryo.ttc", "meiryob.ttc", "arial.ttf", "arialbd.ttf", "ariblk.ttf", "segoeui.ttf", "segoeuib.ttf", "times.ttf", "timesbd.ttf", "timesi.ttf", "cour.ttf", "courbd.ttf", "courbi.ttf", "calibri.ttf", "calibrib.ttf", "cambria.ttc", "seguisym.ttf", "seguiemj.ttf", "YuGothR.ttc", "YuMincho.ttc", "HGRGE.TTC", "symbol.ttf", "wingding.ttf"]
PLAIN_SYMBOLS = str.maketrans({'◼': '■', '⚫': '●', '\uf09f': '•'})


def q(value):
    return json.dumps(value, ensure_ascii=False)


def plain_symbols(value):
    """Wingdingsの箇条書きを通常の単色文字にし、絵文字への代替を防ぐ。"""
    return value.translate(PLAIN_SYMBOLS)


def normalized(value):
    return re.sub(r"\s+|\u200b", "", plain_symbols(value))


def font_style(style):
    name = style["font"]
    families = [("MS-PMincho", "MS PMincho"), ("MS-Mincho", "MS Mincho"), ("MS-PGothic", "MS PGothic"), ("MS-Gothic", "MS Gothic"), ("MeiryoUI", "Meiryo UI"), ("Meiryo", "Meiryo"), ("TimesNewRoman", "Times New Roman"), ("Arial", "Arial"), ("CourierNew", "Courier New"), ("SegoeUIEmoji", "Segoe UI Emoji"), ("SegoeUISymbol", "Segoe UI Symbol"), ("SegoeUI", "Segoe UI"), ("Wingdings", "Wingdings"), ("Calibri", "Calibri"), ("Cambria", "Cambria"), ("HGPGothicE", "HGPｺﾞｼｯｸE"), ("YuGothic", "Yu Gothic"), ("YuMincho", "Yu Mincho"), ("Symbol", "Symbol")]
    family = next((v for k, v in families if k in name), None)
    if family is None:
        raise ValueError(f"未登録のフォント: {name}")
    return dict(style, font=family, weight="black" if "Black" in name else "bold" if "Bold" in name else "regular", slant="italic" if "Italic" in name else "normal")


def flatten(nodes, style=None):
    """Pandocのインライン要素を、編集された文字と書式の列にする。"""
    result = []
    for node in nodes:
        kind, value = node["t"], node.get("c")
        if kind == "Str":
            result.append((value, style))
        elif kind in ("Space", "SoftBreak"):
            result.append((" ", style))
        elif kind == "LineBreak":
            result.append(("\n", style))
        elif kind == 'RawInline' and value[1] == '<br>':
            result.append(('\n', style))
        elif kind == "Span":
            classes = value[0][1]
            base = next((c for c in classes if c.startswith("s") and c[1:].isdigit()), None)
            prefix = style.rsplit(":", 1)[0] + ":" if style and ":" in style else ""
            result += flatten(value[1], prefix + base if base else style)
        elif kind in ("Strong", "Emph", "Underline"):
            result += flatten(value, kind.lower() + ":" + (style or ""))
        elif kind == "Link":
            result += flatten(value[1], 'link%' + quote(value[2][0], safe='') + ':' + (style or ''))
        elif kind == "Code":
            result.append((value[1], style))
        else:
            raise ValueError(f"未対応のMarkdown: {kind}")
    return result


def read_markdown(path):
    run = subprocess.run(["pandoc", str(path), "-f", "markdown-smart-citations-implicit_figures-tex_math_dollars", "--preserve-tabs", "-t", "json"], check=True, capture_output=True, encoding="utf-8")
    doc = json.loads(run.stdout)
    nodes, figures, order = {}, {}, []
    for page in doc["blocks"]:
        if page["t"] == "RawBlock":
            continue
        if page["t"] != "Div":
            raise ValueError("章の最上位はsource-pageのDivにしてください")
        entries = []
        for block in page["c"][1]:
            if block["t"] == "Div":
                attrs, children = block["c"]
                if not attrs[0] or attrs[0] in nodes or attrs[0] in figures:
                    raise ValueError(f"ブロックIDの欠落または重複: {attrs[0]}")
                parts = []
                language = None
                for child in children:
                    if child["t"] == "CodeBlock":
                        parts.append((child["c"][1], None))
                        language = next(iter(child["c"][0][1]), None)
                    elif child['t']=='Table':
                        data=child['c'];raw_rows=data[3][1]+[r for body in data[4] for r in body[3]]
                        rows=[]
                        for row in raw_rows:
                            rows.append([''.join(v for b in c[4] if b['t'] in ('Plain','Para') for v,s in flatten(b['c'])) for c in row[1]])
                        has_header=dict(attrs[2]).get('has-header','true')=='true'
                        if not has_header and rows and all(not c.strip() for c in rows[0]):rows=rows[1:]
                        parts=[('\n'.join(' '.join(row) for row in rows),None)]
                    elif child["t"] in ("Para", "Plain"):
                        if parts:
                            parts.append(("\n\n", None))
                        parts += flatten(child["c"])
                    else:
                        raise ValueError(f"未対応のブロック: {child['t']}")
                nodes[attrs[0]] = {"kind": attrs[1][0], "parts": parts, "text": "".join(p[0] for p in parts), "language": language, "attrs": dict(attrs[2])}
                if attrs[1][0]=='table':nodes[attrs[0]].update(rows=rows,has_header=has_header)
                entries.append(attrs[0])
            elif block["t"] == "Para" and len(block["c"]) == 1 and block["c"][0]["t"] == "Image":
                image = block["c"][0]["c"]
                if not image[0][0] or image[0][0] in figures or image[0][0] in nodes:
                    raise ValueError("図版IDの欠落または重複")
                figures[image[0][0]] = image[2][0]
                entries.append(image[0][0])
            else:
                raise ValueError(f"未対応のページ要素: {block['t']}")
        page_id = page["c"][0][0]
        order.append({"id": page_id, "source_page": int(page_id[5:]) if re.fullmatch(r'page-\d+', page_id) else None, "entries": entries})
    return nodes, figures, order


def style_header(styles):
    entries = []
    for ident, raw in styles.items():
        s = font_style(raw)
        entries.append(f'{ident}: (font: {q(s["font"])}, size: {s["size"]}, weight: {q(s["weight"])}, slant: {q(s["slant"])}, color: {q(s["color"])}, stroke: {s["stroke"]})')
    return '#let styles = (' + ',\n'.join(entries) + ',)\n' + (HERE / "book.typ").read_text(encoding="utf-8")


def native_runs(runs):
    commands = []
    for run in runs:
        for char, x in zip(run["text"], run["positions"]):
            if not char.isspace():
                commands.append(f'#glyph({x}, {run["y"]}, {q(plain_symbols(char))}, {q(run["style"])})')
    return commands


def updated_native_block(group, node):
    """年の置換・句点補完は元の字位置を保持し、版名一行だけ幅を組み直す。"""
    lines = node['text'].split('\n')
    if len(lines) == len(group['lines']) and all(value in (old['text'], old['text'] + '。') for value, old in zip(lines, group['lines'])):
        commands = []
        for value, old in zip(lines, group['lines']):
            runs = [dict(run) for run in old['runs']]
            if value != old['text']:
                # 最後の一字の位置はそのままに、句点だけを続けて組む。
                last = runs[-1]
                index = len(last['text'].rstrip()) - 1
                commands.append(f'#glyph({last["positions"][index]}, {last["y"]}, {q(last["text"][index] + "。")}, {q(last["style"])})')
                last['text'] = last['text'][:index] + ' ' + last['text'][index + 1:]
            commands += native_runs(runs)
        return commands
    if len(lines) == len(group['lines']) and all(len(value) == len(old['text']) for value, old in zip(lines, group['lines'])):
        commands = []
        for value, old in zip(lines, group['lines']):
            offset = 0
            for run in old['runs']:
                end = offset + len(run['text'])
                commands += native_runs([dict(run, text=value[offset:end])])
                offset = end
        return commands
    if len(group['lines']) != 1 or len(lines) != 1:
        raise ValueError('固定配置の変更が元の行に収まりません')
    line = group['lines'][0]
    return [f'#at({line["x"]}, {line["y"]}, text(top-edge: 0pt, bottom-edge: 0pt)[{inline(node["parts"], typography=False)}])']


def source_layout(folder, layout, nodes, figures, markdown):
    if hashlib.sha256(markdown.read_text(encoding="utf-8").encode("utf-8")).hexdigest() != layout["markdown_sha256"]:
        raise ValueError("Markdownの変更を検出しました。編集後は--mode flowを使用してください。元位置版の座標を無断で流用しません。")
    commands = ['#set page(width: 595.32pt, height: 841.92pt, margin: 0pt)', '#set text(lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false)']
    figure_map = {f["id"]: f for f in layout["figures"]}
    for index, page in enumerate(layout["pages"]):
        if index:
            commands.append('#pagebreak(weak: false)')
        commands.append(f'#at(0, 0, image({q("/" + (folder / page["decoration"]).relative_to(ROOT).as_posix())}, width: 595.32pt, height: 841.92pt))')
        commands += native_runs(page["furniture"])
        for ident in page["entries"]:
            if ident in figure_map:
                fig = figure_map[ident]
                x0, y0, x1, y1 = fig["box"]
                path = "/" + (folder / figures[ident]).relative_to(ROOT).as_posix()
                commands.append(f'#at({x0}, {y0}, image({q(path)}, width: {x1-x0}pt, height: {y1-y0}pt))')
            elif ident in layout.get('tables',{}):
                commands += native_runs(layout['tables'][ident]['runs'])
            else:
                group = layout["blocks"][ident]
                assert nodes[ident]["text"] == "\n".join(l["text"] for l in group["lines"]), ident
                for line in group["lines"]:
                    commands += native_runs(line["runs"])
    return "\n".join(commands)


def typographic_parts(parts, keep_lines=False):
    """括弧内側と段落端の手動空白だけを除き、書式の境界は保持する。"""
    if not keep_lines:
        parts = [(value, style) for value, style in parts if value != '\n']
    text = ''.join(value for value, _ in parts)
    remove = set()
    for match in re.finditer(r'(?<=[「『【（])[ \t\u3000]+|[ \t\u3000]+(?=[」』】）])|\A[ \t\u3000]+|(?<=\n\n)[ \t\u3000]+|[ \t\u3000]+\Z', text):
        remove.update(range(match.start(), match.end()))
    result, offset = [], 0
    for value, style in parts:
        cleaned = ''.join(c for i, c in enumerate(value, offset) if i not in remove)
        if cleaned:
            result.append((cleaned, style))
        offset += len(value)
    return result


def inline(parts, typography=True, heading=False, keep_lines=False):
    result = []
    if typography:
        parts = typographic_parts(parts, keep_lines=keep_lines)
    for value, style in parts:
        if value == "\n":
            if keep_lines:
                result.append("#linebreak()")
            continue
        if value == "\n\n":
            result.append("#parbreak()")
            continue
        fields = (style or "").split(":")
        value=plain_symbols(value)
        emphasis = ', emphasis: true' if 'strong' in fields[:-1] else ''
        heading_option = ', heading: true' if heading else ''
        content = f'#styled({q(fields[-1])}, {q(value)}{emphasis}{heading_option})' if fields[-1] else f'#text({q(value)})'
        for modifier in reversed(fields[:-1]):
            if modifier.startswith('link%'):
                content = f'#link({q(unquote(modifier[5:]))})[{content}]'
            else:
                content = f'#{modifier}[{content}]'
        result.append(content)
    content = ''.join(result)
    return '#flowing[' + content + ']' if typography else content


def pagination_options(config, layout, nodes, figures, order):
    """継続が確認された境界と、小幅な図縮小だけを明示指定で許可する。"""
    options = config.get('pagination', {})
    continuations = {int(page): reason for page, reason in options.get('continue_before', {}).items()}
    scales = options.get('figure_scales', {})
    pages = {page['source_page']: page for page in order}
    owners = {ident: page['source_page'] for page in order for ident in page['entries']}
    sequence = [ident for page in order for ident in page['entries']]
    originals = {figure['id']: figure for figure in layout['figures']}
    fixed = set(config.get('native_pages', []))
    fixed |= {page['source_page'] for page in order if not page['entries']}
    if config.get('cover_mode', 'classic') != 'none':
        fixed.add(order[0]['source_page'])
    protected = fixed | {figure['page'] for figure in layout['figures'] if figure.get('slide')}
    for page, reason in continuations.items():
        if (page not in pages or page-1 not in pages or page in protected or page-1 in fixed
                or reason not in {'continued-prose', 'short-minor-heading'}):
            raise ValueError(f'継続できないページ境界です: {page}')
        first = nodes.get(pages[page]['entries'][0])
        if (not first or re.match(r'^(?:演習\s*)?\d+\.\d+(?:\.\d+)?(?:[.\s]|$)', first['text'].strip())
                or first['text'].strip() == '章のまとめ'):
            raise ValueError(f'節・項や図から始まるページは継続できません: {page}')
        if reason == 'continued-prose' and first['kind'] != 'paragraph':
            raise ValueError(f'本文の続きではありません: {page}')
        if reason == 'short-minor-heading' and first['kind'] not in {'heading', 'step'}:
            raise ValueError(f'小小見出しではありません: {page}')
    pairs = options.get('paragraph_continuations', [])
    for first, following in pairs:
        if (first not in nodes or following not in nodes or nodes[first]['kind'] != 'paragraph'
                or nodes[following]['kind'] != 'paragraph'
                or sequence.index(following) != sequence.index(first)+1
                or owners[following] != owners[first]+1
                or continuations.get(owners[following]) != 'continued-prose'):
            raise ValueError(f'段落の続きが隣接していません: {first} / {following}')
    for ident, scale in scales.items():
        figure = originals.get(ident)
        if (ident not in figures or not figure or figure.get('slide') or owners[ident] in protected
                or not .85 <= scale < 1):
            raise ValueError(f'縮小できない図または倍率です: {ident} / {scale}')
    return continuations, pairs, scales


def flow_layout(folder, config, layout, nodes, figures, order, modern=None):
    page_continuations, paragraph_pairs, figure_scales = pagination_options(config, layout, nodes, figures, order)
    heading_spacing = config.get('typography', {}).get('minor_heading_extra_space', {})
    if isinstance(heading_spacing, list):
        heading_spacing = dict.fromkeys(heading_spacing, 18)
    if any(ident not in nodes or nodes[ident]['kind'] != 'heading' for ident in heading_spacing):
        raise ValueError('小小見出しの余白指定に対応する見出しがありません')
    numbered = figure_numbers(config, layout, nodes, figures, order)
    has_cover=config.get('cover_mode','classic')!='none'
    furniture_condition='here().page() > 1' if has_cover else 'true'
    running_title = next((''.join(run['text'] for run in page['furniture'] if run['bbox'][1] < 80).strip()
                          for page in layout['pages'] if page['entries'] and page['source_page'] not in config.get('native_pages', [])
                          and (not has_cover or page['source_page'] != config['first_page'])
                          and any(run['bbox'][1] < 80 and run['text'].strip() for run in page['furniture'])), '')
    commands = [f'''#set page(width: 595.32pt, height: 841.92pt, margin: (left: 85.104pt, right: 83.664pt, top: 86pt, bottom: 68pt),
header: context if {furniture_condition} {{stack(spacing: 3pt, align(center, text(font: "Meiryo UI", size: 9.96pt, {q(running_title)})), line(length: 100%, stroke: 0.48pt))}},
footer: context if {furniture_condition} {{align(center, text(font: "Times New Roman", size: 11.04pt, counter(page).display()))}})
#set text(font: "MS PMincho", size: 11.04pt, lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false, top-edge: "ascender", bottom-edge: "descender")
#set par(leading: 6.96pt, spacing: 12.96pt)
#show strong: it => text(font: "MS PGothic", stroke: 0.31543pt, it.body)
#counter(page).update({config["first_page"]})''']
    cover_page = order[0]
    cover_nodes = [(ident, nodes[ident]["text"]) for ident in cover_page["entries"] if ident in nodes]
    if config.get('cover_mode','classic')=='classic':
        number = next(value.strip() for _, value in cover_nodes if value.strip().isdigit())
        title = next(value for _, value in cover_nodes if value.startswith("第"))
        goal_title = next(value for _, value in cover_nodes if "目標" in value)
        goals = [value.lstrip("◼■ ") for _, value in cover_nodes if value.startswith("◼")]
        commands += [f'#cover({q(number)}, {q(title)}, {q(goal_title)}, ({", ".join(q(v) for v in goals)},))', '#pagebreak()']
    elif has_cover:
        p=layout['pages'][0]
        body=[f'#at(0,0,image({q("/"+(folder/p["decoration"]).relative_to(ROOT).as_posix())},width:595.32pt,height:841.92pt))']
        for ident in p['entries']:
            if ident in layout['blocks']:
                group=layout['blocks'][ident]
                original='\n'.join(l['text'] for l in group['lines'])
                if nodes[ident]['text']!=original:raise ValueError('扉の編集は専用の再配置確認が必要です: '+ident)
                for line in group['lines']:body+=native_runs(line['runs'])
            elif ident in figures:
                f=next(f for f in layout['figures'] if f['id']==ident);x0,y0,x1,y1=f['box']
                body.append(f'#at({x0},{y0},image({q("/"+(folder/figures[ident]).relative_to(ROOT).as_posix())},width:{x1-x0}pt,height:{y1-y0}pt))')
        commands += ['#native-cover['+'\n'.join(body)+']','#pagebreak()']
    figure_map = {f["id"]: f for f in layout["figures"]}
    compact_figures, illustration_captions = {}, {}
    source_pages = {ident: page['source_page'] for page in order for ident in page['entries']}
    continuation_pairs = {
        'ex02': ('p012-b08', 'p012-b09'),
        'ex06': ('p048-b09', 'p048-b10'),
        'ex07': ('p064-b11', 'p064-b12'),
    }
    joined_paragraphs = {}
    if folder.name in continuation_pairs:
        first, following = continuation_pairs[folder.name]
        if source_pages[first] != source_pages[following]:
            raise ValueError('本文の続き断片は同じ原ページで結合してください: ' + following)
        entries_on_page = next(page['entries'] for page in order if first in page['entries'])
        if entries_on_page.index(following) != entries_on_page.index(first) + 1:
            raise ValueError('本文の続き断片が隣接していません: ' + following)
        joined_paragraphs[first] = following
    joined_continuations = set(joined_paragraphs.values())
    for first, following in paragraph_pairs:
        joined_paragraphs[first] = following
    joined_continuations.update(following for _, following in paragraph_pairs)
    joined_source_starts = {source_pages[following]: following for previous, following in paragraph_pairs
                            if source_pages[following] != source_pages[previous]}
    for ident, options in config.get('illustrations', {}).items():
        if ident in figure_map:
            continue
        caption_id = options['caption_id']
        if ident not in figures or caption_id not in nodes:
            raise ValueError('挿絵またはキャプションがありません: ' + ident)
        if source_pages[ident] != source_pages[caption_id] or source_pages[ident] in config.get('native_pages', []):
            raise ValueError('挿絵とキャプションは同じ自動組版ページへ配置してください: ' + ident)
        if caption_id in illustration_captions:
            raise ValueError('挿絵キャプションの重複: ' + caption_id)
        with Image.open(folder / figures[ident]) as image:
            width = min(float(options.get('width', 300)), 426.672)
            height = width * image.height / image.width
        maximum = float(options.get('max_height', 140))
        if height > maximum:
            width *= maximum / height
            height = maximum
        compact_figures[ident] = dict(width=width, height=height, caption_id=caption_id)
        illustration_captions[caption_id] = ident
    code_boxes = code_geometries(folder, layout, nodes)
    code_groups, frame_owners = {}, {}
    for code_id, geometry in code_boxes.items():
        key = (geometry['source_page'], tuple(geometry['frame']))
        owner = frame_owners.setdefault(key, code_id)
        code_groups.setdefault(owner, []).append(code_id)
    code_members = {}
    for owner, group in code_groups.items():
        for code_id in group:
            geometry = code_boxes[code_id]
            for member in [code_id, *geometry.get('caption_ids', []), *geometry.get('figure_ids', [])]:
                if member in code_members and code_members[member] != owner:
                    raise ValueError('コード枠の付属要素が重複しています: ' + member)
                code_members[member] = owner
    omitted_blank_pages = set(config.get('pagination', {}).get('omit_blank_pages', []))
    native_page_map={}
    for page in layout['pages']:
        current_entries = next((p['entries'] for p in order if p['source_page'] == page['source_page']), [])
        if page['source_page'] in omitted_blank_pages:
            if page['entries'] or current_entries:
                raise ValueError('空白でない元頁は省略できません: ' + str(page['source_page']))
            continue
        if page['source_page'] in config.get('native_pages',[]) or (not page['entries'] and not current_entries):
            body=[f'#at(0,0,image({q("/"+(folder/page["decoration"]).relative_to(ROOT).as_posix())},width:595.32pt,height:841.92pt))']
            for ident in page['entries']:
                if ident in layout['blocks']:
                    group=layout['blocks'][ident]
                    if nodes[ident]['text']!='\n'.join(l['text'] for l in group['lines']):
                        if ident not in config.get('native_text_updates', []):
                            raise ValueError('固定ページの編集は再配置確認が必要: '+ident)
                        body += updated_native_block(group, nodes[ident])
                    else:
                        for line in group['lines']:body+=native_runs(line['runs'])
                elif ident in layout.get('tables',{}):body+=native_runs(layout['tables'][ident]['runs'])
                elif ident in figures:
                    fig=figure_map[ident];x0,y0,x1,y1=fig['box']
                    path = '/' + (folder/figures[ident]).relative_to(ROOT).as_posix()
                    if ident in numbered:
                        number = numbered[ident]['number']
                        label = native_number_box(ident, number, page, layout)
                        body.append(f'#native-illustration({q(ident)}, {q(path)}, {x0}, {y0}, {x1-x0}, {y1-y0}, {q(number)}, {label[0]}, {label[1]})')
                    else:
                        body.append(f'#at({x0},{y0},[#mark({q(ident)}, "start")#image({q(path)},width:{x1-x0}pt,height:{y1-y0}pt)#mark({q(ident)}, "end")])')
            body += native_runs(page['furniture'])
            native_page_map['page-'+str(page['source_page'])]='\n'.join(body)
    # スライドの上段は原本の座標を保持し、下段の説明だけを組み直す。
    # 追記を図より前へ置いても、元の図を押し下げない。
    slide_headers = {}
    slide_consumed = set()
    slide_body_first = set()
    for page in order[1:] if has_cover else order:
        source = next((p for p in layout['pages'] if p['source_page'] == page['source_page']), None)
        slides = [f for f in layout['figures'] if f.get('slide') and f['page'] == page['source_page']]
        if not source or len(slides) != 1 or page['id'] in native_page_map:
            continue
        fig = slides[0]
        if fig['id'] not in page['entries']:
            continue
        original_index = source['entries'].index(fig['id'])
        preceding = source['entries'][:original_index]
        following = source['entries'][original_index + 1:]
        # 元から図の前に本文がある特殊ページは通常のフローで処理する。
        if any(ident not in nodes or nodes[ident]['kind'] != 'heading' for ident in preceding):
            continue
        body_lines = [line for ident in following if ident in layout['blocks'] for line in layout['blocks'][ident]['lines']]
        if not body_lines:
            continue
        body_top = min(run['bbox'][1] for run in body_lines[0]['runs'])
        slide_body_first.add(following[0])
        x0, y0, x1, y1 = fig['box']
        body = []
        for ident in preceding:
            group = layout['blocks'][ident]
            if nodes[ident]['text'] != '\n'.join(line['text'] for line in group['lines']):
                raise ValueError('スライド上の見出し変更には再配置確認が必要です: ' + ident)
            body += [f'#mark({q(ident)}, "start")'] + [cmd for line in group['lines'] for cmd in native_runs(line['runs'])] + [f'#mark({q(ident)}, "end")']
        path = '/' + (folder / figures[fig['id']]).relative_to(ROOT).as_posix()
        body += [f'#at({x0}, {y0}, [#mark({q(fig["id"])}, "start")#image({q(path)}, width: {x1-x0}pt, height: {y1-y0}pt)#mark({q(fig["id"])}, "end")])']
        # 元の横罫線だけを復元する。本文用の枠などは流用しない。
        decoration = ET.parse(folder / source['decoration']).getroot()
        for shape in decoration:
            if not shape.tag.endswith('path'):
                continue
            coordinates = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', shape.get('d', ''))]
            if len(coordinates) != 8:
                continue
            xs, ys = coordinates[::2], coordinates[1::2]
            if max(xs)-min(xs) > 300 and max(ys)-min(ys) < 2 and y1 < min(ys) < body_top:
                body.append(f'#at({min(xs)}, {min(ys)}, rect(width: {max(xs)-min(xs)}pt, height: {max(ys)-min(ys)}pt, fill: black, stroke: none))')
        slide_headers[page['id']] = f'#slide-header({body_top-86})[#at(-85.104, -86, box(width: 595.32pt, height: 841.92pt)['+ '\n'.join(body) + '])]'
        slide_consumed.update(preceding + [fig['id']])
    list_continuations = set()
    list_with_continuation = set()
    for page in order:
        in_list = False
        previous = None
        for ident in page['entries']:
            node = nodes.get(ident)
            if not node or node['kind'] != 'paragraph':
                in_list = False
                continue
            if re.match(r'^[■●•▪○・]', plain_symbols(node['text']).lstrip()):
                in_list = True
            elif in_list and ident in layout['blocks'] and layout['blocks'][ident]['lines'][0]['x'] >= 113:
                list_continuations.add(ident)
                list_with_continuation.add(previous)
            else:
                in_list = False
            previous = ident
    def rect_source(shape, origin):
        x0, y0, x1, y1 = shape['rect']
        fill = f'rgb({q(shape["fill"])})' if shape.get('fill') not in (None, 'none') else 'none'
        stroke = f'{shape.get("stroke_width", 0)}pt + rgb({q(shape["stroke"])})' if shape.get('stroke') not in (None, 'none') else 'none'
        return f'#at({x0-origin[0]}, {y0-origin[1]}, rect(width: {x1-x0}pt, height: {y1-y0}pt, fill: {fill}, stroke: {stroke}))'

    def render_code(ident):
        node, geometry = nodes[ident], dict(code_boxes[ident])
        code_ids = code_groups[ident]
        if len(code_ids) > 1:
            for key in ('caption_ids', 'figure_ids'):
                geometry[key] = list(dict.fromkeys(member for code_id in code_ids for member in code_boxes[code_id][key]))
            for key in ('caption_shapes', 'underlay_shapes'):
                unique = {q(shape): shape for code_id in code_ids for shape in code_boxes[code_id][key]}
                geometry[key] = list(unique.values())
            geometry['text_x'] = min(code_boxes[code_id]['text_x'] for code_id in code_ids)
            geometry['text_bottom'] = max(code_boxes[code_id]['text_bottom'] for code_id in code_ids)
        x0, y0, x1, y1 = geometry['frame']
        caption_ids = geometry.get('caption_ids', [])
        outside = {member for member in caption_ids if min(run['bbox'][1] for line in layout['blocks'][member]['lines'] for run in line['runs']) < y0}
        caption_shapes = geometry.get('caption_shapes', [])
        caption_top = min([y0] + [run['bbox'][1] for member in outside for line in layout['blocks'][member]['lines'] for run in line['runs']]
                          + [shape['rect'][1] for shape in caption_shapes if shape['rect'][1] < y0])
        caption = [rect_source(shape, (x0, caption_top)) for shape in caption_shapes if shape['rect'][1] < y0]
        overlay = [rect_source(shape, (x0, y0)) for shape in caption_shapes if shape['rect'][1] >= y0]
        for member in caption_ids:
            group = layout['blocks'][member]
            target = caption if member in outside else overlay
            origin_y = caption_top if member in outside else y0
            target.append(f'#at(0, 0, mark({q(member)}, "heading"))')
            if nodes[member]['text'] == '\n'.join(line['text'] for line in group['lines']):
                for line in group['lines']:
                    shifted = [dict(run, y=run['y']-origin_y, positions=[x-x0 for x in run['positions']]) for run in line['runs']]
                    target += native_runs(shifted)
            else:
                line = group['lines'][0]
                target.append(f'#at({line["x"]-x0}, {line["y"]-origin_y}, text(top-edge: 0pt, bottom-edge: 0pt)[{inline(nodes[member]["parts"], typography=False)}])')
        tail = 0
        for member in geometry.get('figure_ids', []):
            fig = figure_map[member]
            fx0, fy0, fx1, fy1 = fig['box']
            path = '/' + (folder / figures[member]).relative_to(ROOT).as_posix()
            overlay.append(f'#at({fx0-x0}, {fy0-y0}, [#mark({q(member)}, "start")#image({q(path)}, width: {fx1-fx0}pt, height: {fy1-fy0}pt)#mark({q(member)}, "end")])')
            tail = max(tail, fy1-y1)
        underlay = [rect_source(shape, (x0, y0)) for shape in geometry.get('underlay_shapes', [])]
        header_height = max(0, geometry.get('background', geometry['frame'])[1]-y0)
        above = 18 if any(nodes[member]['kind'] == 'heading' for member in caption_ids) else 8
        original_lines = layout['blocks'][ident]['lines']
        sizes = Counter()
        for line in original_lines:
            for run in line.get('runs', []):
                sizes[layout['styles'][run['style']]['size']] += len(run['text'])
        font_size = sizes.most_common(1)[0][0]
        pitches = Counter(round(b['y']-a['y'], 2) for a,b in zip(original_lines,original_lines[1:]) if 0 < b['y']-a['y'] < 40)
        pitch = pitches.most_common(1)[0][0] if pitches else font_size+6
        original_code = '\n'.join(line['text'] for line in layout['blocks'][ident]['lines'])
        # 接続URLの1行定義は保ち、紙面では原本の折り返し位置を使う。
        display_code = original_code if ident == 'p071-b03' and normalized(original_code) == normalized(node['text']) else node['text']
        values = ','.join(q(line) for line in display_code.split('\n'))
        content_option = ''
        if len(code_ids) > 1:
            fragments = []
            for index, code_id in enumerate(code_ids):
                box = code_boxes[code_id]
                if index:
                    gap = max(0, box['text_top']-code_boxes[code_ids[index-1]]['text_bottom'])
                    fragments.append(f'#v({gap}pt)')
                source_lines = layout['blocks'][code_id]['lines']
                sizes = Counter()
                for line in source_lines:
                    for run in line.get('runs', []):
                        sizes[layout['styles'][run['style']]['size']] += len(run['text'])
                size = sizes.most_common(1)[0][0]
                pitches = Counter(round(b['y']-a['y'], 2) for a,b in zip(source_lines,source_lines[1:]) if 0 < b['y']-a['y'] < 40)
                pitch = pitches.most_common(1)[0][0] if pitches else size+6
                lines = ','.join(q(line) for line in nodes[code_id]['text'].split('\n'))
                fragment = f'#code-fragment(({lines},), {q(nodes[code_id]["language"])}, font-size: {size}pt, leading: {max(0,pitch-size)}pt)'
                if index:
                    fragment = f'#mark({q(code_id)}, "start")' + fragment + f'#mark({q(code_id)}, "end")'
                fragments.append(f'#block(above: 0pt, below: 0pt, inset: (left: {box["text_x"]-geometry["text_x"]}pt))[{fragment}]')
            content_option = ', content: [' + '\n'.join(fragments) + ']'
        return (f'#code-panel({q(ident)}, ({values},), {q(node["language"])}, '
                f'width: {x1-x0}pt, offset: {x0-85.104}pt, left: {geometry["text_x"]-x0}pt, right: 0pt, '
                f'top: {geometry["text_top"]-y0}pt, bottom: {max(0,y1-geometry["text_bottom"])}pt, '
                f'source-height: {y1-y0}pt, framed: {str(geometry["framed"]).lower()}, filled: {str(geometry["has_background"]).lower()}, '
                f'caption: [{chr(10).join(caption)}], caption-height: {y0-caption_top}pt, '
                f'header-height: {header_height}pt, underlay: [{chr(10).join(underlay)}], '
                f'overlay: [{chr(10).join(overlay)}], tail: {tail}pt, above: {above}pt, '
                f'font-size: {font_size}pt, leading: {max(0,pitch-font_size)}pt{content_option})')

    def render(ident):
        if ident in joined_continuations:
            return ''
        if ident in figures:
            if ident in compact_figures:
                figure = compact_figures[ident]
                path = '/' + (folder / figures[ident]).relative_to(ROOT).as_posix()
                caption_id = figure['caption_id']
                return (f'#compact-illustration({q(ident)}, {q(path)}, {figure["width"]}, {figure["height"]}, '
                        f'{q(caption_id)}, {q(nodes[caption_id]["text"])}, {q(numbered[ident]["number"])})')
            fig = figure_map.get(ident, {"box": [85.104, 0, 511.776, 0]})
            path = "/" + (folder / figures[ident]).relative_to(ROOT).as_posix()
            width = (fig['box'][2] - fig['box'][0]) * figure_scales.get(ident, 1)
            offset = fig['box'][0] - 85.104
            number = f', number: {q(numbered[ident]["number"])}' if ident in numbered else ''
            return f'#illustration({q(ident)}, {q(path)}, {width}, offset: {offset}pt{number})'
        node = nodes[ident]
        if node['kind'] == 'paragraph':
            keep_lines = node['attrs'].get('keep-lines') == 'true'
            parts = typographic_parts(node['parts'], keep_lines=keep_lines)
            if parts and parts[0][0][0] in '■●•▪○・◼⚫\uf09f':
                value, style = parts[0]
                marker = inline([(value[0], style)])
                parts[0] = (value[1:], style)
                return f'#bullet-paragraph({q(ident)}, [{marker}], [{inline(parts)}], continuing: {str(ident in list_with_continuation).lower()})'
            if ident in list_continuations:
                return f'#list-continuation({q(ident)}, [{inline(parts)}], continuing: {str(ident in list_with_continuation).lower()})'
            is_time_list = folder.name.startswith('ex') and re.fullmatch(
                r'(?:演習\s*\d+\.\d+.*\d+\s*分|\d+\s*分)', node['text'].strip(), re.S)
            if node['text'].lstrip().startswith(('※', 'http://', 'https://')) or is_time_list or node['text'].strip() == 'ヒント':
                return f'#paragraph({q(ident)}, [{inline(parts)}], indent: 0pt)'
            first_style = next((style for value, style in parts if value.strip()), None)
            size = layout['styles'].get((first_style or '').split(':')[-1], {}).get('size', 11.04)
            if ident in joined_paragraphs:
                following = ident
                body = inline(parts)
                while following in joined_paragraphs:
                    previous, following = following, joined_paragraphs[following]
                    body += f'#mark({q(previous)}, "end")'
                    if source_pages[following] != source_pages[previous]:
                        body += f'#mark({q("__source-page-"+str(source_pages[following]))}, "source-page")'
                    body += f'#mark({q(following)}, "start")' + inline(nodes[following]['parts'])
                return f'#paragraph({q(ident)}, [{body}], indent: {size}pt, end-id: {q(following)})'
            if keep_lines:
                return f'#paragraph({q(ident)}, [{inline(parts, keep_lines=True)}], indent: 0pt, left: {size}pt)'
            if size != 11.04:
                return f'#paragraph({q(ident)}, [{inline(parts)}], indent: {size}pt)'
        if node['kind'] == 'step' and config['chapter'] == 'front':
            return f'#list-item({q(ident)}, [{inline(node["parts"])}])'
        if node['kind']=='table':
            info=layout.get('tables',{}).get(ident,{})
            xs=info.get('xs',list(range(len(node['rows'][0])+1)))
            widths=[max(1,xs[i+1]-xs[i]) for i in range(len(xs)-1)]
            rows='('+','.join('('+','.join(q(plain_symbols(c)) for c in row)+',)' for row in node['rows'])+',)'
            options = ''
            if info:
                paint = table_paint(folder, layout, info, node['rows'])
                geometry = table_geometry(layout, info)
                painted_rows = []
                for row in paint:
                    cells = []
                    for cell in row:
                        pieces = []
                        for value, style, underline in cell['parts']:
                            value = '\u200b'.join(plain_symbols(value).replace('\n', ' '))
                            piece = f'#styled({q(style)}, {q(value)})'
                            pieces.append(f'#underline[{piece}]' if underline else piece)
                        cells.append(f'(fill: {q(cell["fill"])}, align: {cell["align"]} + {cell["valign"]}, body: [{"".join(pieces)}])')
                    painted_rows.append('(' + ','.join(cells) + ',)')
                options = (f', paint: ({",".join(painted_rows)},), width: {xs[-1]-xs[0]}pt, '
                           f'offset: {xs[0]-85.104}pt, source-widths: ({",".join(str(w)+"pt" for w in widths)},), '
                           f'source-heights: ({",".join(str(h)+"pt" for h in geometry["row_heights"])},)')
                if geometry['font_size']:
                    options += f', font-size: {geometry["font_size"]}pt'
                    if geometry['pitch']:
                        options += f', leading: {max(0,geometry["pitch"]-geometry["font_size"])}pt'
                if geometry['inset'] is not None:
                    options += f', inset: {geometry["inset"]}pt'
            return f'#table-panel({q(ident)},{rows},({",".join(str(w)+"fr" for w in widths)},),{str(node["has_header"]).lower()}{options})'
        if node["kind"] == "code":
            values = ",".join(q(l) for l in node["text"].split("\n"))
            return f'#code-panel({q(ident)}, ({values},), {q(node["language"])})'
        method = {"heading": "section-heading", "step": "step", "paragraph": "paragraph"}.get(node["kind"])
        if method is None:
            raise ValueError(f'未対応のブロック種類: {node["kind"]}')
        options = ', above: 0pt' if method == 'section-heading' and ident in slide_body_first else ''
        if ident in heading_spacing and ident not in slide_body_first:
            options = f', above: {18 + heading_spacing[ident]}pt'
        # 見出しに分類された説明文の続き（句点終わり）は、原本の通常書体を保つ。
        heading = node['kind'] == 'heading' and not node['text'].rstrip().endswith('。')
        return f'#{method}({q(ident)}, [{inline(node["parts"], heading=heading)}]{options})'

    entries = []
    for page in order[1:] if has_cover else order:
        entries.append('__source-' + page['id'])
        if page['id'] in native_page_map:
            entries.append('__native-' + page['id'])
            continue
        if page['id'] in slide_headers:
            entries.append('__slide-' + page['id'])
        originals = next((p['entries'] for p in layout['pages'] if p['source_page'] == page['source_page']), [])
        # スライド上段は固定し、本文用の挿絵とcaptionはMDの挿入順を保つ。
        additions = [ident for ident in page['entries'] if ident not in originals
                     and ident not in compact_figures and ident not in illustration_captions]
        entries.extend(ident for ident in page['entries'] if ident not in slide_consumed and (page['id'] not in slide_headers or ident not in additions))
        if page['id'] in slide_headers:
            entries.extend(additions)
    i = 0
    rendered_codes = set()
    reference_open = False
    def modern_panel(ident):
        panels = []
        for token in modern['anchors'][ident]:
            part = modern['parts'][token]
            events = '\n'.join(f'#at({event["x"]}, {event["y"]}, mark({q(event["id"])}, {q(event["edge"])}))' for event in part['events'])
            panels.append(f'#html-panel({q(token)}, {part["width"]}, {part["height"]}, offset: {part["offset"]}pt)[{events}]')
        return '\n'.join(panels)
    while i < len(entries):
        ident = entries[i]
        is_reference = nodes.get(ident, {}).get('attrs', {}).get('reference-group') == 'messages'
        if reference_open and not is_reference:
            commands.append(']')
            reference_open = False
        if is_reference and not reference_open:
            commands += ['#pagebreak(weak: true)', '#reference-panel[']
            reference_open = True
        if ident.startswith('__source-'):
            source_page = int(ident.rsplit('-', 1)[1])
            if source_page in omitted_blank_pages:
                # 原本の元頁番号を記録し、白紙だけを自動組版から省く。
                commands.append(f'#mark({q(ident)}, "source-page")')
                i += 1
                continue
            if source_page not in page_continuations:
                commands.append('#pagebreak(weak: true)')
            elif page_continuations[source_page] == 'short-minor-heading':
                # 自分の位置で改頁を判定すると改頁後の位置との循環になる。
                # 位置が確定している直前元頁の本文末尾で半頁条件を判定する。
                previous_ids = next(page['entries'] for page in order if page['source_page']==source_page-1)
                ids = '(' + ','.join(q(value) for value in previous_ids) + ',)'
                commands.append('#context {let previous=query(<book-check>).filter(item => '
                    + ids + '.contains(item.value.id) and ("end","heading").contains(item.value.edge)); '
                    'let last=previous.sorted(key: item => (item.location().page(),item.location().position().y)).last(); '
                    'if last.location().position().y > 429.96pt {pagebreak(weak: true)}}')
            if source_page not in joined_source_starts:
                commands.append(f'#mark({q(ident)}, "source-page")')
            i += 1
            continue
        if ident.startswith('__slide-'):
            commands.append(slide_headers[ident[len('__slide-'):]])
            i += 1
            continue
        if ident.startswith('__native-'):
            commands += ['#pagebreak(weak: true)','#[#set page(header: none, footer: none)\n#mark('+q(ident)+',"native-page")\n#native-cover['+native_page_map[ident[len('__native-'):]]+']\n#pagebreak(weak: true)]']
            i+=1
            continue
        if ident in illustration_captions or ident in joined_continuations:
            i += 1
            continue
        # 続き本文の後に節・項が登場した場合は、その見出しから新頁にする。
        if (source_pages.get(ident) in page_continuations and ident in nodes
                and nodes[ident]['kind']=='heading'
                and re.match(r'^(?:演習\s*)?\d+\.\d+(?:\.\d+)?(?:[.\s]|$)', nodes[ident]['text'].strip())):
            commands.append('#pagebreak(weak: true)')
        # 手順の説明や一例分のコードを見出しと同じページに保つ。
        keep_next = int(nodes.get(ident, {}).get('attrs', {}).get('keep-next', 0))
        if keep_next:
            group = entries[i:i + keep_next + 1]
            body = '\n'.join(modern_panel(e) if modern and e in modern['anchors'] else render(e) for e in group)
            above = 18 + heading_spacing.get(ident, 0)
            commands.append(f'#instruction({q("instruction-" + ident)}, above: {above}pt)[{body}]')
            i += len(group)
            continue
        if modern and ident in modern['anchors']:
            commands.append(modern_panel(ident))
            i += 1
            continue
        if modern and ident in modern['consume']:
            i += 1
            continue
        if not modern and ident in code_members:
            code_id = code_members[ident]
            if code_id not in rendered_codes:
                commands.append(render_code(code_id))
                rendered_codes.add(code_id)
            i += 1
            continue
        if ident in nodes and nodes[ident]["kind"] in ('step','heading'):
            end = i + 1
            while end < len(entries) and entries[end] not in code_members and (not modern or entries[end] not in modern['consume']) and entries[end] in nodes and nodes[entries[end]]["kind"] == "paragraph":
                end += 1
            if end < len(entries) and entries[end] in figures and entries[end] not in compact_figures and entries[end] not in code_members and (not modern or entries[end] not in modern['consume']):
                body = "\n".join(render(e) for e in entries[i:end + 1])
                # 枠の先頭にある子見出しの上余白は相殺されるため、外側で確保する。
                above = 0 if ident in slide_body_first else (18 if nodes[ident]['kind'] == 'heading' else 8)
                if ident not in slide_body_first:
                    above += heading_spacing.get(ident, 0)
                commands.append(f'#instruction({q("instruction-" + ident)}, above: {above}pt)[{body}]')
                i = end + 1
                continue
        if ident in nodes and i+1<len(entries) and entries[i+1] in nodes and nodes[entries[i+1]]['kind']=='code' and re.search(r'[/\\].*\.(?:java|html|css|xml|properties|yml|yaml)\s*$',nodes[ident]['text']):
            commands.append(f'#code-label({q(ident)},[{inline(nodes[ident]["parts"])}])')
            i+=1
            continue
        # 短いコード導入ラベルと、その直後の説明を最初のコード枠に繋げる。
        if (ident in nodes and nodes[ident]['kind'] == 'paragraph'
                and re.fullmatch(r'[■①-⑳][^\n。]+', plain_symbols(nodes[ident]['text']).strip())):
            end = i + 1
            if (end+1 < len(entries) and entries[end] in nodes and nodes[entries[end]]['kind'] == 'paragraph'
                    and entries[end+1] in nodes and nodes[entries[end+1]]['kind'] == 'code'):
                end += 1
            if end < len(entries) and entries[end] in nodes and nodes[entries[end]]['kind'] == 'code':
                body = '\n'.join(render(e) for e in entries[i:end])
                commands.append(f'#block(sticky: true, breakable: false, above: 0pt, below: 0pt)[{body}]')
                i = end
                continue
        commands.append(render(ident))
        i += 1
    if reference_open:
        commands.append(']')
    return "\n".join(commands)


def compile_pdf(work, name, content, font_paths):
    source = work / f"{name}.typ"
    source.write_text(content, encoding="utf-8", newline="\n")
    result = typst.compile(str(source), root=str(ROOT), font_paths=font_paths, ignore_system_fonts=True)
    return fitz.open(stream=result, filetype="pdf"), source


def pdf_image(page, scale=1.5):
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def build(chapter="01", mode="all", markdown=None, output=None):
    folder = ROOT / "docs/textbook/chapters" / chapter
    work = ROOT / "tmp/textbook" / chapter
    out = Path(output) if output else ROOT / "output/pdf/textbook" / f"chapter-{chapter}"
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    font_dir = work / "fonts"
    font_dir.mkdir(exist_ok=True)
    for name in FONT_FILES:
        dest = font_dir / name
        if not dest.exists() and (Path('C:/Windows/Fonts')/name).exists():
            shutil.copyfile(Path("C:/Windows/Fonts") / name, dest)
    font_paths = [str(font_dir)]
    config = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    layout = json.loads((folder / "source-layout.json").read_text(encoding="utf-8"))
    explicit_markdown=markdown is not None
    markdown = Path(markdown) if markdown else folder / "chapter.md"
    nodes, figures, order = read_markdown(markdown)
    reference_markdown=folder/'baseline.md' if not explicit_markdown and (folder/'baseline.md').exists() else markdown
    ref_nodes,ref_figures,_=read_markdown(reference_markdown) if reference_markdown!=markdown else (nodes,figures,order)
    expected_ids = set(layout["blocks"]) | set(layout.get('tables',{}))
    if mode in ("all", "reference"):
        assert set(ref_nodes) == expected_ids, "元位置版のブロックIDが元データと一致しません"
        assert set(ref_figures) == {f["id"] for f in layout["figures"]}, "元位置版の図版IDが一致しません"
    for path in figures.values():
        assert (folder / path).is_file(), path
    header = style_header(layout["styles"])
    report = {"chapter": chapter, "source_sha256":layout['source_sha256'], "source_pages": [config["first_page"], config["last_page"]], "blocks": len(nodes), "figures": len(figures), "source_coverage": [p["coverage"] for p in layout["pages"]]}
    if mode!='all' and (out/'checks.json').exists():
        previous=json.loads((out/'checks.json').read_text(encoding='utf-8'))
        if previous.get('source_sha256')==layout['source_sha256']:
            retained='reference' if mode=='flow' else 'flow'
            if retained in previous:report[retained]=previous[retained]
    if mode in ("all", "reference"):
        original = fitz.open(ROOT / config["pdf"])
        assert hashlib.sha256(Path(original.name).read_bytes()).hexdigest() == layout["source_sha256"], "元PDFが取り込み時から変わっています"
        pdf, _ = compile_pdf(work, "reference-layout", header + source_layout(folder, layout, ref_nodes, ref_figures, reference_markdown), font_paths)
        assert len(pdf) == config["last_page"] - config["first_page"] + 1
        pdf.save(out / "chapter-reference.pdf", garbage=4, deflate=True)
        comparisons = fitz.open()
        pages = []
        for index, info in enumerate(layout["pages"]):
            expected = "".join(r["text"] for r in info["furniture"]) + "".join(ref_nodes[ident]["text"] for ident in info["entries"] if ident in ref_nodes)
            actual = pdf[index].get_text()
            matches = Counter(normalized(expected)) == Counter(normalized(actual))
            if not matches:
                missing = Counter(normalized(expected)) - Counter(normalized(actual))
                extra = Counter(normalized(actual)) - Counter(normalized(expected))
                raise AssertionError(f'元位置版 {info["source_page"]}ページの文字差: 不足{dict(missing)} 余分{dict(extra)}')
            before = original[info["source_page"] - 1]
            a, b = pdf_image(before), pdf_image(pdf[index])
            Image.blend(a, b, 0.5).save(out / f'p{info["source_page"]:03d}-overlay.png')
            diff = ImageChops.difference(a, b)
            diff.convert("L").point(lambda v: 0 if v > 20 else 255).save(out / f'p{info["source_page"]:03d}-difference.png')
            p = comparisons.new_page(width=1210.64, height=869.92)
            p.insert_text((20, 18), f'元PDF {info["source_page"]}ページ', fontname="japan", fontsize=11)
            p.insert_text((635.32, 18), "Markdownから生成した元位置再現版", fontname="japan", fontsize=11)
            p.show_pdf_page(fitz.Rect(0, 28, 595.32, 869.92), original, info["source_page"] - 1)
            p.show_pdf_page(fitz.Rect(615.32, 28, 1210.64, 869.92), pdf, index)
            pages.append({"source_page": info["source_page"], "native_text_complete": matches, "mean_absolute_rgb_error_0_255": round(sum(ImageStat.Stat(diff).mean) / 3, 4)})
        comparisons.save(out / "comparison.pdf", garbage=4, deflate=True)
        report["reference"] = {"pages": len(pdf), "page_checks": pages}
    if mode in ("all", "flow"):
        modern = html_components.prepare(folder, config, layout, nodes, figures, order)
        numbered = figure_numbers(config, layout, nodes, figures, order)
        pdf, source = compile_pdf(work, "flow", header + flow_layout(folder, config, layout, nodes, figures, order, modern=modern), font_paths)
        marks = json.loads(typst.query(str(source), "<book-check>", field="value", format="json", root=str(ROOT), font_paths=font_paths, ignore_system_fonts=True))
        boundaries = [mark for mark in marks if mark['edge']=='source-page']
        source_order = order[1:] if config.get('cover_mode','classic')!='none' else order
        assert [int(mark['id'].rsplit('-',1)[1]) for mark in boundaries]==[page['source_page'] for page in source_order], '元頁境界の順序が崩れています'
        assert all(mark['page'] >= (2 if config.get('cover_mode','classic')!='none' else 1) for mark in boundaries), '本文が扉へ流入しています'
        assert all(a['page']<=b['page'] for a,b in zip(boundaries,boundaries[1:])), '元頁の物理順序が崩れています'
        html_components.embed(pdf, modern, marks)
        url_links = add_url_links(pdf, nodes)
        pdf.save(out / "chapter-flow.pdf", garbage=4, deflate=True)
        orphan = []
        split_figures = []
        split_short_code = []
        split_short_tables = []
        split_instructions = []
        for i, m in enumerate(marks):
            if m["edge"] == "heading":
                following = None
                for candidate in marks[i + 1:]:
                    if candidate['edge'] == 'source-page':
                        break
                    if candidate['edge'] in ('start', 'heading'):
                        following = candidate
                        break
                if following and following["page"] != m["page"]:
                    orphan.append(m)
        for ident in figures:
            if (config.get('cover_mode','classic')!='none' and ident in order[0]['entries']) or any(ident in p['entries'] and p['source_page'] in config.get('native_pages',[]) for p in layout['pages']):
                continue
            locations = [m["page"] for m in marks if m["id"] == ident]
            if len(locations) != 2 or locations[0] != locations[1]:
                split_figures.append(ident)
        for ident, node in nodes.items():
            if node["kind"] == "code" and any(m['id']==ident and m['edge']=='short-code' for m in marks):
                locations = [m["page"] for m in marks if m["id"] == ident and m['edge'] in ('start','end')]
                if len(locations) != 2 or locations[0] != locations[1]:
                    split_short_code.append(ident)
            if node['kind']=='table' and any(m['id']==ident and m['edge']=='short-table' for m in marks):
                locations=[m['page'] for m in marks if m['id']==ident and m['edge'] in ('start','end')]
                if len(locations)!=2 or locations[0]!=locations[1]:split_short_tables.append(ident)
        instruction_ids = {m["id"] for m in marks if m["id"].startswith("instruction-")}
        for ident in instruction_ids:
            places = [m for m in marks if m["id"] == ident]
            if len(places) != 2 or places[0]["page"] != places[1]["page"] or places[-1]["y"] > 778:
                split_instructions.append(ident)
        overflow = []
        original_runs = [r for block in layout['blocks'].values() for line in block['lines'] for r in line.get('runs', [])]
        right_limit = min(595.32, max([545] + [r['bbox'][2]+0.5 for r in original_runs]))
        left_limit = max(0, min([78] + [r['bbox'][0]-0.5 for r in original_runs]))
        actual_body = []
        native_page_positions={m['page'] for m in marks if m['edge']=='native-page'}
        for index, page in enumerate(pdf):
            for b in page.get_text("dict")["blocks"]:
                for line in b.get("lines", []):
                    x0, y0, x1, y1 = line["bbox"]
                    content = "".join(s["text"] for s in line["spans"])
                    if index+1 not in native_page_positions and (index > 0 or config.get('cover_mode','classic')=='none') and (y1 < 80 or y0 > 784):
                        continue
                    actual_body.append(content)
                    if index == 0 and config.get('cover_mode','classic')!='none':
                        continue
                    if index+1 in native_page_positions:
                        if x0<0 or y0<0 or x1>595.32 or y1>841.92:overflow.append({'page':index+1,'bbox':list(line['bbox'])})
                        continue
                    if x0 < left_limit or x1 > right_limit or y1 > 778:
                        overflow.append({"page": index + 1, "bbox": list(line["bbox"])})
        expected = Counter(normalized("".join(n["text"] for ident,n in nodes.items() if ident not in modern['consume']) + modern['expected_text']))
        expected += Counter(normalized(''.join(record['number'] for ident, record in numbered.items()
                                                if ident not in modern['consume'])))
        # 新しい設定図のSVGには、輪郭ではなく文字として残したラベルもある。
        svg_text=''.join(''.join(node.itertext()) for ident,path in figures.items() if ident not in modern['consume'] and Path(path).suffix.lower()=='.svg' for node in ET.parse(folder/path).iter('{http://www.w3.org/2000/svg}text'))
        expected += Counter(normalized(svg_text))
        native_sources = {int(m['id'].rsplit('-', 1)[1]) for m in marks if m['edge'] == 'native-page'}
        expected += Counter(normalized(''.join(r['text'] for p in layout['pages'] if p['source_page'] in native_sources for r in p['furniture'])))
        for ident,node in nodes.items():
            if node['kind']=='table' and node['has_header'] and ident not in modern['consume']:
                repeats=max(0,sum(m['id']==ident and m['edge']=='table-header' for m in marks)-1)
                expected += Counter(normalized(''.join(node['rows'][0]))*repeats)
        actual = Counter(normalized("".join(actual_body)))
        complete = expected == actual
        if not complete:
            raise AssertionError(f"自動組版の文字差: 不足{dict(expected-actual)} 余分{dict(actual-expected)}")
        report["flow"] = {"pages": len(pdf), "native_text_complete": complete, "heading_orphans": orphan, "split_figures": split_figures, "split_short_code": split_short_code, "split_short_tables":split_short_tables, "split_instructions": split_instructions, "instruction_groups": len(instruction_ids), "fixed_pages":sorted(native_page_positions), "overflow": overflow, "block_positions": marks}
        report['flow']['url_links'] = url_links
        report['flow']['numbered_figures'] = {ident: dict(record) for ident, record in numbered.items()}
        continuations, paragraph_pairs, scales = pagination_options(config, layout, nodes, figures, order)
        omitted_blank_pages = set(config.get('pagination', {}).get('omit_blank_pages', []))
        report['flow']['pagination'] = dict(
            options=config.get('pagination', {}),
            source_boundaries=[dict(source_page=int(mark['id'].rsplit('-', 1)[1]), page=mark['page'],
                mode='omit-blank' if int(mark['id'].rsplit('-', 1)[1]) in omitted_blank_pages
                else 'continue' if int(mark['id'].rsplit('-', 1)[1]) in continuations else 'page-break',
                reason=continuations.get(int(mark['id'].rsplit('-', 1)[1])))
                for mark in marks if mark['edge'] == 'source-page'],
            paragraph_continuations=paragraph_pairs,
            scaled_figures={ident: dict(scale=scale,
                original_width=next(f['box'][2]-f['box'][0] for f in layout['figures'] if f['id']==ident),
                width=next(f['box'][2]-f['box'][0] for f in layout['figures'] if f['id']==ident)*scale)
                for ident, scale in scales.items()})
        for ident, record in report['flow']['numbered_figures'].items():
            if record['kind'] == 'native':
                fig = next(f for f in layout['figures'] if f['id'] == ident)
                page = next(p for p in layout['pages'] if p['source_page'] == fig['page'])
                record['frame_box'] = [fig['box'][0]-4, fig['box'][1]-4, fig['box'][2]+4, fig['box'][3]+4]
                record['number_box'] = native_number_box(ident, record['number'], page, layout)
        report['flow']['html_components'] = [{'id':spec['id'], 'kind':spec['kind'], 'consume_ids':spec['consume'], 'parts':[{'token':token, 'width':modern['parts'][token]['width'], 'height':modern['parts'][token]['height']} for token in modern['anchors'][spec['anchor']]]} for spec in modern['specs']]
        assert not orphan and not split_figures and not split_short_code and not split_short_tables and not split_instructions and not overflow, report["flow"]
    (out / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"chapter": chapter, "blocks": len(nodes), "figures": len(figures), "reference_pages": report.get("reference", {}).get("pages"), "flow_pages": report.get("flow", {}).get("pages")}, ensure_ascii=False))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default="01")
    parser.add_argument("--mode", choices=["all", "reference", "flow"], default="all")
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    build(args.chapter, args.mode, args.markdown)
