"""全章の生成PDFで、原文・図の左端・コード枠・表の書式を検証する。"""
from collections import Counter
import json
import unittest

import pymupdf as fitz

from build import ROOT, normalized, read_markdown
from code_geometry import code_geometries


class SourceLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {}
        cls.drawings = {}
        for folder in sorted((ROOT / 'docs/textbook/chapters').iterdir()):
            if not (folder / 'source.json').exists():
                continue
            config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
            layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
            original, original_figures, _ = read_markdown(folder / 'baseline.md')
            current, current_figures, _ = read_markdown(folder / 'chapter.md')
            output = ROOT / 'output/pdf/textbook' / ('chapter-' + folder.name)
            checks = json.loads((output / 'checks.json').read_text(encoding='utf-8'))
            pdf = fitz.open(output / 'chapter-flow.pdf')
            cls.addClassCleanup(pdf.close)
            modern = {ident: component for component in checks['flow'].get('html_components', [])
                      for ident in component['consume_ids']}
            cls.chapters[folder.name] = dict(config=config, layout=layout, original=original,
                current=current, marks=checks['flow']['block_positions'], pdf=pdf,
                codes=code_geometries(folder, layout, current), modern=modern,
                original_figures=original_figures, current_figures=current_figures)

    def mark(self, chapter, ident, edge):
        matches = [m for m in chapter['marks'] if m['id'] == ident and m['edge'] == edge]
        self.assertEqual(len(matches), 1, (ident, edge, matches))
        return matches[0]

    @staticmethod
    def fixed(chapter, source_page):
        config = chapter['config']
        return source_page in config.get('native_pages', []) or (
            source_page == config['first_page'] and config.get('cover_mode', 'classic') != 'none')

    def page_drawings(self, name, page):
        key = (name, page)
        if key not in self.drawings:
            self.drawings[key] = [{k: d.get(k) for k in ('rect', 'fill', 'color', 'width')}
                for d in self.chapters[name]['pdf'][page - 1].get_drawings()]
        return self.drawings[key]

    def component_parts(self, chapter, ident):
        for part in chapter['modern'][ident]['parts']:
            position = self.mark(chapter, part['token'], 'html-component')
            yield part, position, fitz.Rect(position['x'], position['y'],
                position['x'] + part['width'], position['y'] + part['height'])

    @staticmethod
    def color_is(actual, expected):
        return actual is not None and max(abs(a - b) for a, b in zip(actual, expected)) < .001

    @staticmethod
    def text_characters(page, rect=None):
        return [dict(c, font=span['font'], color=span['color'], size=span['size'])
            for block in page.get_text('rawdict')['blocks'] for line in block.get('lines', [])
            for span in line['spans'] for c in span['chars']
            if normalized(c['c']) and (rect is None or rect.contains(fitz.Rect(c['bbox'])))]

    def text_hit(self, characters, text):
        value = ''.join(c['c'] for c in characters)
        self.assertIn(text, value)
        start = value.index(text)
        return characters[start:start + len(text)]

    @staticmethod
    def text_box(characters):
        result = fitz.Rect(characters[0]['bbox'])
        for character in characters[1:]:
            result |= fitz.Rect(character['bbox'])
        return result

    def test_only_explicitly_authorized_content_is_added(self):
        added = set()
        added_figures = set()
        self.assertEqual(len(self.chapters), 19)
        for name, chapter in self.chapters.items():
            removed = ({'p060-b09','p060-b10','p060-b11'} if name=='02' else
                       {'p071-b06','p071-b07','p071-b08','p115-b05'} if name=='03' else set())
            self.assertEqual(chapter['original'].keys() - chapter['current'].keys(), removed, name)
            self.assertFalse(chapter['original_figures'].keys() - chapter['current_figures'].keys(), name)
            added_figures.update((name, ident) for ident in
                chapter['current_figures'].keys() - chapter['original_figures'].keys())
            for ident in chapter['current'].keys() - chapter['original'].keys():
                added.add((name, ident))
        messages = ('title', 'purpose', 'files', 'bundles', 'ja', 'en', 'fallback', 'settings',
                    'settings-note', 'thymeleaf', 'html', 'java', 'controller', 'locale')
        errors = ('title', 'console', 'name', 'trace-intro', 'trace', 'trace-read', 'template', 'sql', 'status')
        expected = {('03', 'migration-03-jpa-pom'), ('03', 'revision-di-caption'),
                    ('02','revision-login3-instruction'), ('02','revision-model-moving-pack'),
                    ('02','revision-model-moving-unpack')}
        service = (
            'quick-fix-title', 'quick-fix-1', 'quick-fix-2', 'quick-fix-3',
            'examples-intro',
            'examples-list-title', 'examples-list-definition', 'examples-list-implementation', 'examples-list-controller',
            'examples-insert-title', 'examples-save-definition', 'examples-save-implementation', 'examples-insert-controller',
            'examples-update-title', 'examples-update-definition', 'examples-update-implementation', 'examples-update-controller',
            'examples-delete-title', 'examples-delete-definition', 'examples-delete-implementation', 'examples-delete-controller',
        )
        expected.update(('03', 'revision-service-' + name) for name in service)
        expected.update(('04', 'revision-messages-' + name) for name in messages)
        expected.update(('appendix-b', 'revision-errors-' + name) for name in errors)
        expected_figures = {('03', 'revision-di-remote')}
        for name, chapter in self.chapters.items():
            for ident, spec in chapter['config'].get('illustrations', {}).items():
                if ident not in chapter['original_figures']:
                    expected.add((name, spec['caption_id']))
                    expected_figures.add((name, ident))
        self.assertEqual(added, expected)
        self.assertEqual(added_figures, expected_figures)
        start = self.mark(self.chapters['03'], 'revision-di-remote', 'start')
        end = self.mark(self.chapters['03'], 'revision-di-remote', 'end')
        self.assertEqual(start['page'], end['page'])
        self.assertGreater(end['y'], start['y'])
        self.assertAlmostEqual(start['x'], 85.104, delta=.02)

    def test_all_figures_keep_the_source_left_edge_and_one_page(self):
        modes = Counter()
        for name, chapter in self.chapters.items():
            for figure in chapter['layout']['figures']:
                ident, box = figure['id'], figure['box']
                with self.subTest(chapter=name, figure=ident):
                    start, end = self.mark(chapter, ident, 'start'), self.mark(chapter, ident, 'end')
                    if ident in chapter['modern']:
                        if ident in {'p243-f03', 'p243-f04'}:
                            # コード実行結果の元画像を、同じカードのfooterへ保持する。
                            self.assertEqual(chapter['original_figures'][ident], chapter['current_figures'][ident])
                            self.assertEqual(chapter['modern'][ident]['kind'], 'code')
                        else:
                            # 明示許可された画像内ファイル名とコード付属の2注記だけを文字へ変換する。
                            self.assertIn(ident, {'p071-f07', 'p113-f49', 'p149-f13', 'p161-f24',
                                                 'p182-f15', 'p071-f08', 'p113-f50'})
                        self.assertEqual(start['page'], end['page'])
                        self.assertIn(start['page'], {position['page']
                            for _, position, _ in self.component_parts(chapter, ident)})
                        continue
                    mode = 'native' if self.fixed(chapter, figure['page']) else 'slide' if figure.get('slide') else 'flow'
                    modes[mode] += 1
                    self.assertEqual(start['page'], end['page'])
                    self.assertAlmostEqual(start['x'], box[0], delta=.02)
                    scale = chapter['config'].get('pagination',{}).get('figure_scales',{}).get(ident,1)
                    self.assertGreaterEqual(scale,.85)
                    self.assertLessEqual(scale,1)
                    self.assertAlmostEqual(end['y'] - start['y'], (box[3] - box[1])*scale, delta=.02)
                    if mode != 'flow':
                        self.assertAlmostEqual(start['y'], box[1], delta=.02)
        for mode in ('native', 'slide', 'flow'):
            self.assertGreater(modes[mode], 0, mode)

    def test_code_frames_and_all_attached_captions_keep_their_geometry(self):
        checked = 0
        for name, chapter in self.chapters.items():
            for ident, geometry in chapter['codes'].items():
                if self.fixed(chapter, geometry['source_page']):
                    continue
                with self.subTest(chapter=name, code=ident):
                    if ident in chapter['modern']:
                        component = chapter['modern'][ident]
                        if component['kind'] == 'code':
                            checked += 1
                            for part, position, rect in self.component_parts(chapter, ident):
                                self.assertAlmostEqual(rect.x0, geometry['frame'][0], delta=.02)
                                self.assertAlmostEqual(part['width'], geometry['frame'][2] - geometry['frame'][0], delta=.02)
                                self.assertLessEqual(part['height'], 620.75)
                                self.assertLessEqual(rect.y1, 784.02)
                        else:
                            self.assertEqual(component['kind'], 'explanation')
                        continue
                    start, end = self.mark(chapter, ident, 'start'), self.mark(chapter, ident, 'end')
                    owner = next(i for i,g in chapter['codes'].items()
                                 if g['source_page'] == geometry['source_page'] and g['frame'] == geometry['frame'])
                    if owner != ident:
                        outer_start, outer_end = self.mark(chapter, owner, 'start'), self.mark(chapter, owner, 'end')
                        self.assertEqual(start['page'], outer_start['page'])
                        self.assertEqual(end['page'], outer_end['page'])
                        self.assertGreaterEqual(start['y'], outer_start['y'])
                        self.assertLessEqual(end['y'], outer_end['y']+.02)
                        start, end = outer_start, outer_end
                    for member in geometry['caption_ids']:
                        self.assertEqual(self.mark(chapter, member, 'heading')['page'], start['page'], member)
                    for member in geometry['figure_ids']:
                        self.assertEqual(self.mark(chapter, member, 'start')['page'], start['page'], member)
                        self.assertEqual(self.mark(chapter, member, 'end')['page'], start['page'], member)
                    if not geometry['has_background']:
                        continue
                    checked += 1
                    x0, _, x1, _ = geometry['frame']
                    self.assertAlmostEqual(start['x'], x0, delta=.02)
                    for page in range(start['page'], end['page'] + 1):
                        top = start['y'] if page == start['page'] else 0
                        bottom = end['y'] if page == end['page'] else chapter['pdf'][page - 1].rect.height
                        backgrounds = [d for d in self.page_drawings(name, page)
                            if self.color_is(d['fill'], (1, 251 / 255, 240 / 255))
                            # SVG内に残る行単位の塗りと、実際の外枠を区別する。
                            and self.color_is(d['color'], (0, 0, 0)) and abs(d['width']-.48) < .02
                            and d['rect'].y1 > top + .02 and d['rect'].y0 < bottom - .02]
                        self.assertTrue(backgrounds, (ident, page, 'コード背景がない'))
                        for drawing in backgrounds:
                            self.assertAlmostEqual(drawing['rect'].x0, x0, delta=.3)
                            self.assertAlmostEqual(drawing['rect'].width, x1 - x0, delta=.3)
                            if geometry['framed']:
                                self.assertTrue(self.color_is(drawing['color'], (0, 0, 0)))
                                self.assertAlmostEqual(drawing['width'], .48, delta=.02)
        self.assertGreater(checked, 0)

    def test_controller_filename_is_visible_in_the_upper_right_header(self):
        chapter = self.chapters['02']
        ident = 'p041-b01'
        owner, geometry = next((i, g) for i, g in chapter['codes'].items() if ident in g['caption_ids'])
        start = self.mark(chapter, owner, 'start')
        page = chapter['pdf'][start['page'] - 1]
        label = self.text_box(self.text_hit(self.text_characters(page), chapter['current'][ident]['text']))
        if ident in chapter['modern']:
            _, position, rect = next(self.component_parts(chapter, ident))
            self.assertEqual(position['page'], start['page'])
            self.assertTrue(rect.contains(label))
            self.assertLess(label.y1, start['y'])
            self.assertLessEqual(rect.x1 - label.x1, 16)
            return
        original = chapter['layout']['blocks'][ident]['lines'][0]['runs'][0]['bbox']
        frame = geometry['frame']
        self.assertAlmostEqual(label.x0 - start['x'], original[0] - frame[0], delta=.02)
        self.assertAlmostEqual(label.y0 - start['y'], original[1] - frame[1], delta=.03)
        self.assertGreater(label.x0, (frame[0] + frame[2]) / 2)
        self.assertLess(label.y1, start['y'])
        red = [d for d in self.page_drawings('02', start['page']) if self.color_is(d['color'], (1, 0, 0))
               and d['rect'].contains(label)]
        self.assertTrue(red, '実PDFの赤枠にファイル名が収まっていない')

    def test_jdbc_comparison_preserves_colors_emphasis_and_column_centering(self):
        chapter = self.chapters['03']
        ident = 'p069-table01'
        table = chapter['layout']['tables'][ident]
        if ident in chapter['modern']:
            parts = list(self.component_parts(chapter, ident))
            characters = []
            for part, position, area in parts:
                self.assertAlmostEqual(part['width'], 426.672, delta=.02)
                characters += self.text_characters(chapter['pdf'][position['page'] - 1], area)
            for text in ('要素', 'JDBC', 'ドライバー', 'mysql-connector-j.jar',
                         '手動でプロジェクトに追加する', 'application.properties'):
                style = chapter['layout']['styles'][next(r for r in table['runs'] if text in r['text'])['style']]
                color = 0x334155 if text in ('要素', 'JDBC') else int(style['color'].lstrip('#'), 16)
                self.assertTrue(all(c['color'] == color
                                    for c in self.text_hit(characters, text)), text)
            jdbc = self.text_box(self.text_hit(characters, 'JDBC'))
            _, _, area = parts[0]
            ratio = .4375  # 要素25%、JDBC37.5%、JPA37.5%の新しい比較用レイアウト。
            self.assertAlmostEqual((jdbc.x0 + jdbc.x1) / 2, area.x0 + area.width * ratio, delta=1)
            border = (188 / 255, 200 / 255, 213 / 255)
            self.assertTrue(any(self.color_is(d['fill'], border) or self.color_is(d['color'], border)
                                for d in self.page_drawings('03', parts[0][1]['page'])))
            return
        start, end = self.mark(chapter, ident, 'start'), self.mark(chapter, ident, 'end')
        self.assertEqual(start['page'], end['page'])
        area = fitz.Rect(table['xs'][0] - 1, start['y'] - 1, table['xs'][-1] + 1, end['y'] + 1)
        characters = self.text_characters(chapter['pdf'][start['page'] - 1], area)
        targets = ('要素', 'JDBC', 'ドライバー', 'mysql-connector-j.jar', '手動でプロジェクトに追加する', 'application.properties')
        for text in targets:
            with self.subTest(text=text):
                source = next(run for run in table['runs'] if text in run['text'])
                style = chapter['layout']['styles'][source['style']]
                actual = self.text_hit(characters, text)
                for char in actual:
                    self.assertEqual(char['font'], style['font'])
                    self.assertEqual(char['color'], int(style['color'].lstrip('#'), 16))
                    self.assertAlmostEqual(char['size'], style['size'], delta=.02)
        jdbc = self.text_box(self.text_hit(characters, 'JDBC'))
        self.assertAlmostEqual((jdbc.x0 + jdbc.x1) / 2, (table['xs'][1] + table['xs'][2]) / 2, delta=.02)
        lines = [d for d in self.page_drawings('03', start['page'])
                 if self.color_is(d['color'], (64 / 255,) * 3)
                 and d['rect'].x1 >= area.x0 and d['rect'].x0 <= area.x1
                 and d['rect'].y1 >= area.y0 and d['rect'].y0 <= area.y1]
        self.assertGreaterEqual(len(lines), 4)
        self.assertTrue(all(abs(d['width'] - .65) < .01 for d in lines))

    def test_all_seven_operation_checks_are_pdf_headings(self):
        for name, identifiers in {'02': ('p061-b01',), '05': ('p174-b04', 'p180-b01'),
                '07': ('p249-b02', 'p261-b05', 'p268-b01', 'p271-b01')}.items():
            chapter = self.chapters[name]
            for ident in identifiers:
                with self.subTest(chapter=name, heading=ident):
                    node = chapter['current'][ident]
                    self.assertEqual(node['kind'], 'heading')
                    self.assertEqual(normalized(node['text']).lstrip('■'), '動作確認')
                    self.mark(chapter, ident, 'heading')

    def test_long_repository_method_keeps_its_identifier_and_readable_code_font(self):
        chapter = self.chapters['06']
        ident = 'p224-b08'
        if ident in chapter['modern']:
            chars = [char for _, position, area in self.component_parts(chapter, ident)
                     for char in self.text_characters(chapter['pdf'][position['page'] - 1], area)]
            method = self.text_hit(chars, 'findByNameLikeOrCategoryNameLikeOrDescriptionLikeOrBrandLikeOrSkuLike')
            self.assertTrue(all(abs(c['size'] - 10.5) < .02 and c['font'] == 'Consolas' for c in method))
            return
        start = self.mark(chapter, 'p224-b08', 'start')
        end = self.mark(chapter, 'p224-b08', 'end')
        self.assertEqual(start['page'], end['page'])
        chars = self.text_characters(chapter['pdf'][start['page']-1],
            fitz.Rect(0, start['y']-.5, 595.32, end['y']+.5))
        method = self.text_hit(chars, 'findByNameLikeOrCategoryNameLikeOrDescriptionLikeOrBrandLikeOrSkuLike')
        self.assertTrue(all(abs(c['size']-11.04) < .02 for c in method))
        self.assertLess(max(c['origin'][1] for c in method)-min(c['origin'][1] for c in method), .02)


if __name__ == '__main__':
    unittest.main(verbosity=2)
