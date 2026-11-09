"""原本の教材単位を、改訂後も前ページへ繰り上げないことを検証する。"""
import json
import unittest
import xml.etree.ElementTree as ET

import pymupdf as fitz

from build import ROOT, normalized, read_markdown, pagination_options


class PaginationTests(unittest.TestCase):
    def test_code_introductions_stay_with_the_first_code_panel(self):
        path = ROOT / 'output/pdf/textbook/chapter-06/checks.json'
        marks = json.loads(path.read_text(encoding='utf-8'))['flow']['block_positions']
        for introduction, code in [('p233-b09', 'p233-b10'), ('p234-b01', 'p234-b02'),
                                   ('p206-b11', 'p206-b13'), ('p206-b12', 'p206-b13')]:
            with self.subTest(introduction=introduction):
                intro = [m for m in marks if m['id'] == introduction and m['edge'] in ('start', 'end')]
                start = min((m for m in marks if m['id'] == code and m['edge'] == 'start'),
                            key=lambda m: (m['page'], m['y']))
                self.assertEqual({m['page'] for m in intro}, {start['page']})

    def test_only_reviewed_source_pages_can_continue_the_previous_content(self):
        for folder in (ROOT / 'docs/textbook/chapters').iterdir():
            if not (folder / 'source.json').exists():
                continue
            config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
            checks = json.loads((ROOT / 'output/pdf/textbook' / ('chapter-' + folder.name) / 'checks.json').read_text(encoding='utf-8'))
            layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
            nodes, figures, order = read_markdown(folder / 'chapter.md')
            allowed, _, _ = pagination_options(config, layout, nodes, figures, order)
            marks = checks['flow']['block_positions']
            expected = list(range(config['first_page'], config['last_page'] + 1))
            if config.get('cover_mode', 'classic') != 'none':
                expected = expected[1:]
            boundaries = [(i, int(m['id'].rsplit('-', 1)[1]), m['page']) for i, m in enumerate(marks) if m['edge'] == 'source-page']
            self.assertEqual([source for _, source, _ in boundaries], expected, folder.name)
            previous_end = 1 if config.get('cover_mode', 'classic') != 'none' else 0
            for n, (start, source, page) in enumerate(boundaries):
                stop = boundaries[n + 1][0] if n + 1 < len(boundaries) else len(marks)
                content = marks[start + 1:stop]
                if source in allowed:
                    self.assertGreaterEqual(page, previous_end, (folder.name, source))
                else:
                    self.assertGreater(page, previous_end, (folder.name, source))
                self.assertTrue(content, (folder.name, source, '空白ページも実体を保持する'))
                self.assertTrue(all(m['page'] >= page for m in content), (folder.name, source))
                previous_end = max(m['page'] for m in content)

    def test_requested_continuations_and_short_operation_pages_stay_together(self):
        checks = json.loads((ROOT / 'output/pdf/textbook/chapter-02/checks.json').read_text(encoding='utf-8'))
        marks = checks['flow']['block_positions']
        def edge(ident, kind):
            return next(m for m in marks if m['id']==ident and m['edge']==kind)
        self.assertEqual(edge('p043-b09','end')['page'], edge('p044-b01','start')['page'])
        self.assertEqual(edge('p048-b07','end')['page'], edge('p049-b01','start')['page'])
        self.assertEqual(edge('p045-b01','heading')['page'], edge('p045-f17','end')['page'])
        # 旧54～56pの短い説明は、次のHTMLコードと同じ頁へ続ける。
        self.assertEqual(edge('p048-b07','end')['page'], edge('p049-b04','start')['page'])
        self.assertEqual(edge('p047-b04','end')['page'], edge('p048-b01','heading')['page'])

        def position(ident, kind):
            mark = edge(ident, kind)
            return mark['page'], mark['y']
        anchors = [
            position('p058-b05','end'), position('p059-b04','heading'),
            position('p059-b05','start'), position('p059-b06','end'), position('p058-b06','start'),
        ]
        self.assertEqual(anchors, sorted(anchors))
        self.assertEqual(anchors[1][0], anchors[2][0])

        checks = json.loads((ROOT / 'output/pdf/textbook/chapter-03/checks.json').read_text(encoding='utf-8'))
        marks = checks['flow']['block_positions']
        prior = edge('p086-b11','end')
        step = edge('p087-b01','heading')
        self.assertEqual(prior['page'], step['page'])
        self.assertEqual(step['page'], edge('p087-f20','end')['page'])
        self.assertGreaterEqual(step['y'] - prior['y'], 18)

    def test_service_examples_and_quick_fix_stay_with_their_headings(self):
        folder = ROOT / 'docs/textbook/chapters/03'
        nodes, _, order = read_markdown(folder / 'chapter.md')
        checks = json.loads((ROOT / 'output/pdf/textbook/chapter-03/checks.json').read_text(encoding='utf-8'))
        groups = [
            p['entries'][i:i+4] for p in order for i, ident in enumerate(p['entries'])
            if ident.startswith('revision-service-') and nodes.get(ident, {}).get('attrs', {}).get('keep-next')=='3'
        ]
        self.assertEqual(len(groups), 5)
        for group in groups:
            self.assertEqual(len(group), 4)
            pages = {m['page'] for m in checks['flow']['block_positions'] if m['id'] in group}
            self.assertEqual(len(pages), 1, group)

    def test_section_and_subsection_page_starts_remain_protected(self):
        import re
        for folder in (ROOT/'docs/textbook/chapters').iterdir():
            if not (folder/'source.json').exists():
                continue
            config=json.loads((folder/'source.json').read_text(encoding='utf-8'))
            nodes,_,order=read_markdown(folder/'chapter.md')
            for page in order:
                first=next((nodes[i] for i in page['entries'] if i in nodes),None)
                if first and re.match(r'^(?:演習\s*)?\d+\.\d+(?:\.\d+)?(?:[.\s]|$)',first['text'].strip()):
                    self.assertNotIn(str(page['source_page']),config.get('pagination',{}).get('continue_before',{}))

    def test_slide_positions_keep_the_original_upper_area(self):
        count = 0
        for folder in (ROOT / 'docs/textbook/chapters').iterdir():
            if not (folder / 'source-layout.json').exists():
                continue
            layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
            checks = json.loads((ROOT / 'output/pdf/textbook' / ('chapter-' + folder.name) / 'checks.json').read_text(encoding='utf-8'))
            marks = checks['flow']['block_positions']
            for figure in layout['figures']:
                if not figure.get('slide'):
                    continue
                ends = {m['edge']: m for m in marks if m['id'] == figure['id']}
                self.assertEqual(ends['start']['page'], ends['end']['page'], figure['id'])
                self.assertAlmostEqual(ends['start']['y'], figure['box'][1], places=3, msg=figure['id'])
                self.assertAlmostEqual(ends['end']['y'], figure['box'][3], places=3, msg=figure['id'])
                count += 1
        self.assertEqual(count, 65)

    def test_course_outline_does_not_spill_into_the_next_page(self):
        pdf = fitz.open(ROOT / 'output/pdf/textbook/chapter-front/chapter-flow.pdf')
        self.assertEqual(len(pdf), 14)
        outline = pdf[9].get_text()
        position = pdf[10].get_text()
        self.assertIn('6. 外部参照', outline)
        self.assertIn('7. Bootstrap', outline)
        self.assertNotIn('6. 外部参照', position)
        self.assertNotIn('7. Bootstrap', position)

    def test_running_headers_follow_the_original(self):
        for folder in (ROOT / 'docs/textbook/chapters').iterdir():
            if not (folder / 'source-layout.json').exists():
                continue
            layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
            output = ROOT / 'output/pdf/textbook' / ('chapter-' + folder.name)
            checks = json.loads((output / 'checks.json').read_text(encoding='utf-8'))
            pdf = fitz.open(output / 'chapter-flow.pdf')
            fixed = set(checks['flow']['fixed_pages'])
            for mark in checks['flow']['block_positions']:
                if mark['edge'] != 'source-page' or mark['page'] in fixed:
                    continue
                source = next(p for p in layout['pages'] if p['source_page'] == int(mark['id'].rsplit('-', 1)[1]))
                expected = normalized(''.join(r['text'] for r in source['furniture'] if r['bbox'][1] < 80))
                actual = normalized(pdf[mark['page'] - 1].get_textbox(fitz.Rect(0, 0, 595.32, 80)))
                self.assertEqual(expected, actual, (folder.name, source['source_page']))

    def test_no_environment_paragraph_is_added_to_the_goals(self):
        for folder in (ROOT / 'docs/textbook/chapters').iterdir():
            if not (folder / 'chapter.md').exists():
                continue
            nodes, _, _ = read_markdown(folder / 'chapter.md')
            self.assertNotIn('revision-environment', nodes, folder.name)
            self.assertFalse(any(ident.endswith('-environment') and ident.startswith('migration-') for ident in nodes), folder.name)

    def test_bean_section_starts_on_its_own_page(self):
        path = ROOT / 'output/pdf/textbook/chapter-01'
        checks = json.loads((path / 'checks.json').read_text(encoding='utf-8'))
        marks = checks['flow']['block_positions']
        heading = next(m for m in marks if m['id'] == 'p023-b01')
        maven = next(m for m in marks if m['id'] == 'p024-b01')
        self.assertLess(heading['y'], 110)
        self.assertGreater(maven['page'], heading['page'])
        pdf = fitz.open(path / 'chapter-flow.pdf')
        self.assertNotIn('1.4. Maven', pdf[heading['page'] - 1].get_text())

    def test_appendix_contents_are_original_with_version_changes_only(self):
        for chapter in ('appendix-a', 'appendix-b'):
            folder = ROOT / 'docs/textbook/chapters' / chapter
            before, original_figures, _ = read_markdown(folder / 'baseline.md')
            after, current_figures, _ = read_markdown(folder / 'chapter.md')
            allowed_additions = {'revision-errors-' + suffix for suffix in (
                'title', 'console', 'name', 'trace-intro', 'trace', 'trace-read', 'template', 'sql', 'status')}
            config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
            illustration_ids = {ident for ident in config.get('illustrations', {}) if ident not in original_figures}
            allowed_additions.update(config['illustrations'][ident]['caption_id'] for ident in illustration_ids)
            self.assertFalse(set(before) - set(after), chapter)
            self.assertEqual(set(after) - set(before), allowed_additions if chapter == 'appendix-b' else set(), chapter)
            self.assertFalse(set(original_figures) - set(current_figures), chapter)
            self.assertEqual(set(current_figures) - set(original_figures), illustration_ids, chapter)
            allowed = {'p285-f07', 'p287-f09', 'p287-f10', 'p288-f11', 'p288-f13'}
            for ident, old_path in original_figures.items():
                new_path = current_figures[ident]
                if old_path != new_path:
                    self.assertIn(ident, allowed)
                    old = ET.parse(folder / old_path).getroot()
                    new = ET.parse(folder / new_path).getroot()
                    for attribute in ('width', 'height', 'viewBox'):
                        self.assertEqual(old.get(attribute), new.get(attribute), ident)
            for ident, node in before.items():
                text = node['text'].replace('Eclipse 2022(pleiades)', 'Pleiades 2025').replace('Java 17', 'Java 21').replace('Java17', 'Java21').replace('3.1.5', '4.0.2')
                text = text.replace('© 2024 Trainocate Japan, Ltd.', '© 2027 Trainocate Japan, Ltd.')
                if ident == 'p285-b03':
                    text += '。'
                corrected = {
                    'p291-b06': '5. 修正したファイルを保存し、ビルドが正常に完了していますか？Pleiades のコンソールでアプリケーションの起動完了を確認し、正しいポート番号へアクセスしてください。',
                    'p291-b07': '6. テンプレートファイルの配置は正しいですか？Thymeleaf テンプレートファイルは、通常src/main/resources/templates ディレクトリに配置します。Controller が返した名前のテンプレートが見つからない場合は、通常500 エラーになります。404 と区別して確認してください。',
                    'p291-b08': '7. テンプレートファイルの拡張子は正しいですか？Thymeleaf テンプレートのファイル名は.html で終わる必要があります。間違った拡張子を使用していると、テンプレートが見つからず、通常500 エラーになります。'}
                if chapter == 'appendix-b' and ident in corrected:
                    self.assertEqual(normalized(corrected[ident]), normalized(after[ident]['text']), ident)
                else:
                    self.assertEqual(text, after[ident]['text'], ident)


if __name__ == '__main__':
    unittest.main(verbosity=2)
