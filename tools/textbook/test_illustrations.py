"""小型挿絵の寸法・caption・元頁所属と、追加前の原文を検証する。"""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import subprocess
import unittest

import pymupdf as fitz
from PIL import Image

from build import ROOT, read_markdown

CATALOG = ROOT / 'docs/textbook/illustrations.json'
APPROVED_EDITION = 'f16135f3cebb2e2f9ab481e9cfead35b05bd52d4'
FIGURE_REVISION_EDITION = '96a99882326d65ec048100b2f20fa0ed4aaa72d2'
DI_INTRO = 'illustration-figure-cards-2026-di-remote-intro'
MANAGED = 'illustration-expansion-2026-boot-managed-versions'
BEAN = 'illustration-expansion-2026-bean-auto-configuration'
REMOVED_MANAGED_ASSET = 'docs/textbook/chapters/01/assets/revision-ill-boot-managed-versions.png'


@lru_cache(maxsize=None)
def catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def chapter(name):
    folder = ROOT / 'docs/textbook/chapters' / name
    nodes, figures, pages = read_markdown(folder / 'chapter.md')
    config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
    return folder, nodes, figures, pages, config


@lru_cache(maxsize=None)
def base_chapter(name, base=None):
    base = base or catalog()['base_commit']
    relative = 'docs/textbook/chapters/' + name + '/chapter.md'
    result = subprocess.run(['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show', base + ':' + relative],
                            cwd=ROOT, check=True, capture_output=True)
    path = ROOT / 'tmp/illustrations-tests/base' / base / (name + '.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.stdout)
    return read_markdown(path)


def image_size(record):
    folder = ROOT / 'docs/textbook/chapters' / record['chapter']
    with Image.open(folder / record['asset']) as image:
        width = float(record['width'])
        height = width * image.height / image.width
    if height > record['max_height']:
        width *= record['max_height'] / height
        height = record['max_height']
    return width, height


class IllustrationSourceTests(unittest.TestCase):
    def test_new_assets_and_existing_di_follow_print_limits(self):
        data = catalog()
        self.assertEqual(len(data['new']), 33)
        self.assertEqual(len(data['resized']), 1)
        self.assertEqual(data['resized'][0]['figure_id'], 'revision-di-remote')
        ids = [r['figure_id'] for r in data['new'] + data['resized']]
        self.assertEqual(len(ids), len(set(ids)))
        for record in data['new'] + data['resized']:
            with self.subTest(figure=record['figure_id']):
                folder = chapter(record['chapter'])[0]
                asset = folder / record['asset']
                self.assertTrue(asset.is_file())
                if record in data['new']:
                    self.assertIn('asset_sha256', record)
                    self.assertIn('image_pixels', record)
                if 'asset_sha256' in record:
                    self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), record['asset_sha256'])
                with Image.open(asset) as image:
                    if 'image_pixels' in record:
                        self.assertEqual(list(image.size), record['image_pixels'])
                        # 既存9図の比率は保持し、追加図は実寸と印刷上限で検査する。
                        if record['figure_id'].startswith('illustration-2026-'):
                            self.assertAlmostEqual(image.width / image.height, 2.4, delta=.04)
                width, height = image_size(record)
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)
                self.assertLessEqual(width, data['print_limits']['max_width'])
                self.assertLessEqual(height, data['print_limits']['max_height'])
                self.assertLessEqual(width, 260 if record in data['resized'] else 280)

    def test_figure_and_caption_are_adjacent_in_the_declared_source_page(self):
        for record in catalog()['new'] + catalog()['resized']:
            with self.subTest(figure=record['figure_id']):
                _, nodes, figures, pages, config = chapter(record['chapter'])
                owners = {ident: p['source_page'] for p in pages for ident in p['entries']}
                order = [ident for p in pages for ident in p['entries']]
                figure, caption = record['figure_id'], record['caption_id']
                self.assertEqual(figures[figure], record['asset'])
                self.assertEqual(owners[figure], record['source_page'])
                self.assertEqual(owners[caption], record['source_page'])
                self.assertEqual(order.index(caption), order.index(figure) + 1)
                options = config['illustrations'][figure]
                self.assertEqual(options['caption_id'], caption)
                self.assertEqual(options['width'], record['width'])
                self.assertEqual(options['max_height'], record['max_height'])
                if 'caption' in record:
                    self.assertEqual(nodes[caption]['text'], record['caption'])
                    self.assertEqual(order.index(figure), order.index(record['after_id']) + 1)
                    self.assertEqual(order.index(record['before_id']), order.index(caption) + 1)

    def test_original_text_code_and_id_order_are_unchanged(self):
        additions = defaultdict(set)
        captions = defaultdict(set)
        for record in catalog()['new']:
            additions[record['chapter']].add(record['figure_id'])
            captions[record['chapter']].add(record['caption_id'])
        original_count = current_count = 0
        for name in catalog()['reviewed_chapters']:
            before_nodes, before_figures, before_pages = base_chapter(name)
            _, nodes, figures, pages, _ = chapter(name)
            with self.subTest(chapter=name):
                self.assertEqual(set(nodes) - set(before_nodes), captions[name])
                self.assertEqual(set(figures) - set(before_figures), additions[name])
                self.assertFalse(set(before_nodes) - set(nodes))
                self.assertFalse(set(before_figures) - set(figures))
                for ident, node in before_nodes.items():
                    # 字下げなど表示用attrsは本文の文字や既存書式Spanと区別する。
                    self.assertEqual({k:v for k,v in node.items() if k != 'attrs'},
                                     {k:v for k,v in nodes[ident].items() if k != 'attrs'}, ident)
                for ident, path in before_figures.items():
                    self.assertEqual(figures[ident], path, ident)
                self.assertEqual([p['source_page'] for p in pages], [p['source_page'] for p in before_pages])
                for old, new in zip(before_pages, pages):
                    allowed = additions[name] | captions[name]
                    self.assertEqual([i for i in new['entries'] if i not in allowed], old['entries'])
            original_count += len(before_nodes) + len(before_figures)
            current_count += len(nodes) + len(figures)
        self.assertEqual(original_count, 2879)
        self.assertEqual(current_count, original_count + 66)

    def test_only_new_illustration_settings_are_added_since_the_approved_edition(self):
        command = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show']
        previous = subprocess.run(command + [APPROVED_EDITION + ':docs/textbook/illustrations.json'],
            cwd=ROOT, check=True, capture_output=True)
        previous = json.loads(previous.stdout)
        previous_records = {r['figure_id']: r for r in previous['new']}
        current_records = {r['figure_id']: r for r in catalog()['new']}
        self.assertEqual(len(current_records.keys() - previous_records.keys()), 24)
        for ident, record in previous_records.items():
            self.assertEqual(current_records[ident], record, ident)
        additions = defaultdict(set)
        for ident in current_records.keys() - previous_records.keys():
            additions[current_records[ident]['chapter']].add(ident)
        for name in catalog()['reviewed_chapters']:
            with self.subTest(chapter=name):
                relative = 'docs/textbook/chapters/' + name + '/source.json'
                before = subprocess.run(command + [APPROVED_EDITION + ':' + relative],
                    cwd=ROOT, check=True, capture_output=True)
                before = json.loads(before.stdout)
                config = chapter(name)[4]
                self.assertEqual({k:v for k,v in config.items() if k not in {'illustrations','pagination'}},
                                 {k:v for k,v in before.items() if k not in {'illustrations','pagination'}})
                old_options = before.get('illustrations', {})
                new_options = config.get('illustrations', {})
                self.assertEqual(set(new_options) - set(old_options), additions[name])
                for ident, options in old_options.items():
                    self.assertEqual(new_options[ident], options, ident)

    def test_original_baseline_layout_and_assets_are_unchanged(self):
        paths = []
        for name in catalog()['reviewed_chapters']:
            folder = 'docs/textbook/chapters/' + name
            paths += [folder+'/baseline.md', folder+'/source-layout.json', folder+'/assets']
        result = subprocess.run(['git', '-c', 'safe.directory='+ROOT.as_posix(), 'diff', '--name-only',
            '--no-renames', catalog()['base_commit'], '--', *paths], cwd=ROOT, check=True,
            capture_output=True, encoding='utf-8')
        allowed = {'docs/textbook/chapters/'+r['chapter']+'/'+r['asset'] for r in catalog()['new']}
        allowed.add(REMOVED_MANAGED_ASSET)
        self.assertTrue(set(result.stdout.splitlines()).issubset(allowed), result.stdout)

    def test_only_requested_di_bean_changes_follow_the_previous_edition(self):
        command = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show']
        previous = json.loads(subprocess.run(command +
            [FIGURE_REVISION_EDITION + ':docs/textbook/illustrations.json'],
            cwd=ROOT, check=True, capture_output=True).stdout)
        old_records = {r['figure_id']: r for r in previous['new'] + previous['resized']}
        records = {r['figure_id']: r for r in catalog()['new'] + catalog()['resized']}
        self.assertEqual(set(records) - set(old_records), {DI_INTRO})
        self.assertEqual(set(old_records) - set(records), {MANAGED})
        for ident, record in old_records.items():
            if ident not in {MANAGED, BEAN}:
                self.assertEqual(records[ident], record, ident)
        self.assertEqual(records[BEAN]['asset'], old_records[BEAN]['asset'])
        self.assertNotEqual(records[BEAN]['asset_sha256'], old_records[BEAN]['asset_sha256'])
        old_count = current_count = 0
        for name in catalog()['reviewed_chapters']:
            before_nodes, before_figures, before_pages = base_chapter(name, FIGURE_REVISION_EDITION)
            _, nodes, figures, pages, config = chapter(name)
            added = {DI_INTRO, DI_INTRO + '-caption'} if name == '01' else set()
            removed = {MANAGED, MANAGED + '-caption'} if name == '01' else set()
            moved = {BEAN, BEAN + '-caption'} if name == '01' else set()
            with self.subTest(chapter=name):
                old_ids, current_ids = set(before_nodes) | set(before_figures), set(nodes) | set(figures)
                self.assertEqual(current_ids - old_ids, added)
                self.assertEqual(old_ids - current_ids, removed)
                for ident, node in before_nodes.items():
                    if ident in removed or name == '01' and ident == BEAN + '-caption':
                        continue
                    self.assertEqual({k:v for k,v in node.items() if k != 'attrs'},
                                     {k:v for k,v in nodes[ident].items() if k != 'attrs'}, ident)
                for ident, path in before_figures.items():
                    if ident not in removed:
                        self.assertEqual(figures[ident], path, ident)
                self.assertEqual([p['source_page'] for p in pages], [p['source_page'] for p in before_pages])
                for old, new in zip(before_pages, pages):
                    ignored = added | removed | moved
                    self.assertEqual([i for i in old['entries'] if i not in ignored],
                                     [i for i in new['entries'] if i not in ignored])
                relative = 'docs/textbook/chapters/' + name + '/source.json'
                before_config = json.loads(subprocess.run(command + [FIGURE_REVISION_EDITION + ':' + relative],
                    cwd=ROOT, check=True, capture_output=True).stdout)
                current_config = dict(config)
                # 頁継続・小幅な図縮小はtest_paginationと専用監査で別に検査する。
                current_config.pop('pagination',None)
                current_options = dict(current_config.get('illustrations', {}))
                if name == '01':
                    old_options = before_config['illustrations']
                    old_options.pop(MANAGED)
                    current_options.pop(DI_INTRO)
                current_config['illustrations'] = current_options
                if 'illustrations' not in before_config:
                    current_config.pop('illustrations')
                self.assertEqual(current_config, before_config)
            old_count += len(before_nodes) + len(before_figures)
            current_count += len(nodes) + len(figures)
        self.assertEqual(old_count, 2945)
        self.assertEqual(current_count, old_count)
        _, _, _, pages, _ = chapter('01')
        for ident, anchor, source in [(DI_INTRO, 'p020-b03', 20), (BEAN, 'p023-b02', 23)]:
            entries = next(p['entries'] for p in pages if p['source_page'] == source)
            position = entries.index(anchor)
            self.assertEqual(entries[position:position+3], [anchor, ident, ident + '-caption'])
            self.assertEqual(records[ident]['source_page'], source)
            self.assertEqual(records[ident]['after_id'], anchor)
        self.assertFalse((ROOT / REMOVED_MANAGED_ASSET).exists())
        allowed_assets = {REMOVED_MANAGED_ASSET,
            'docs/textbook/chapters/01/' + records[DI_INTRO]['asset'],
            'docs/textbook/chapters/01/' + records[BEAN]['asset']}
        asset_paths = ['docs/textbook/chapters/' + name + '/assets' for name in catalog()['reviewed_chapters']]
        changed_assets = subprocess.run(command[:-1] + ['diff', '--name-only', '--no-renames',
            FIGURE_REVISION_EDITION, '--', *asset_paths], cwd=ROOT, check=True,
            capture_output=True, encoding='utf-8').stdout.splitlines()
        self.assertTrue(set(changed_assets).issubset(allowed_assets), changed_assets)


class IllustrationPdfTests(unittest.TestCase):
    def test_each_image_and_caption_stay_between_the_declared_pdf_anchors(self):
        contexts = {}
        for record in catalog()['new']:
            name = record['chapter']
            if name not in contexts:
                folder = ROOT / 'output/pdf/textbook' / ('chapter-' + name)
                checks = json.loads((folder / 'checks.json').read_text(encoding='utf-8'))
                pdf = fitz.open(folder / 'chapter-flow.pdf')
                self.addCleanup(pdf.close)
                contexts[name] = (checks['flow']['block_positions'], pdf)
            marks, pdf = contexts[name]

            def position(ident, edge):
                matches = [m for m in marks if m['id'] == ident and m['edge'] == edge]
                if edge == 'start':
                    matches += [m for m in marks if m['id'] == ident and m['edge'] == 'heading']
                if matches:
                    points = [(m['page'], round(m['y'], 2)) for m in matches]
                    return max(points) if edge == 'end' else min(points)
                # 見出し・手順には終端マーカーがないため、実PDFの文字の下端で確認する。
                heading = [m for m in marks if m['id'] == ident and m['edge'] == 'heading']
                self.assertTrue(edge == 'end' and len(heading) == 1, (ident, edge))
                mark = heading[0]
                rectangles = pdf[mark['page'] - 1].search_for(chapter(name)[1][ident]['text'])
                rectangles = [r for r in rectangles if abs(r.y0 - mark['y']) < 2]
                self.assertTrue(rectangles, ident)
                return mark['page'], round(max(r.y1 for r in rectangles), 2)

            with self.subTest(figure=record['figure_id']):
                anchors = [(record['after_id'], 'end'), (record['figure_id'], 'start'),
                           (record['figure_id'], 'end'), (record['caption_id'], 'start'),
                           (record['caption_id'], 'end'), (record['before_id'], 'start')]
                points = [position(ident, edge) for ident, edge in anchors]
                for index in range(len(points) - 1):
                    self.assertLessEqual(points[index], points[index + 1],
                        (anchors[index], points[index], anchors[index + 1], points[index + 1]))

    def test_image_dimensions_and_caption_are_kept_on_one_physical_page(self):
        for record in catalog()['new'] + catalog()['resized']:
            with self.subTest(figure=record['figure_id']):
                folder = ROOT / 'output/pdf/textbook' / ('chapter-'+record['chapter'])
                checks = json.loads((folder/'checks.json').read_text(encoding='utf-8'))
                marks = checks['flow']['block_positions']
                figure = [m for m in marks if m['id'] == record['figure_id']]
                caption = [m for m in marks if m['id'] == record['caption_id']]
                self.assertEqual({m['edge'] for m in figure}, {'start','end'})
                self.assertEqual({m['edge'] for m in caption}, {'start','end'})
                self.assertEqual(len(figure), 2)
                self.assertEqual(len(caption), 2)
                self.assertEqual(len({m['page'] for m in figure+caption}), 1)
                start = next(m for m in figure if m['edge']=='start')
                end = next(m for m in figure if m['edge']=='end')
                cap_start = next(m for m in caption if m['edge']=='start')
                self.assertGreaterEqual(cap_start['y'], end['y'] - .1)
                self.assertLessEqual(cap_start['y'] - end['y'], 30)
                expected_width, expected_height = image_size(record)
                with fitz.open(folder/'chapter-flow.pdf') as pdf:
                    images = pdf[start['page']-1].get_image_info()
                    matching = [fitz.Rect(i['bbox']) for i in images
                                if abs(i['bbox'][0]-start['x'])<.2 and abs(i['bbox'][1]-start['y'])<.2]
                    self.assertTrue(matching, (record['figure_id'],start,images))
                    rect = min(matching, key=lambda r: abs(r.width-expected_width)+abs(r.height-expected_height))
                    self.assertAlmostEqual(rect.width, expected_width, delta=.2)
                    self.assertAlmostEqual(rect.height, expected_height, delta=.2)
                    self.assertLessEqual(rect.width, 300.2)
                    self.assertLessEqual(rect.height, 140.2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
