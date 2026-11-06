"""原文を保持するHTMLカードと、ブラウザーPDFの分割・文字・書式を検証する。"""
from collections import Counter
from functools import lru_cache
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import os
import re
import subprocess
import unittest
from unittest.mock import patch

import pymupdf as fitz

from build import ROOT, read_markdown
import html_components as components


@lru_cache(maxsize=None)
def chapter(name):
    folder = ROOT / 'docs/textbook/chapters' / name
    nodes, figures, order = read_markdown(folder / 'chapter.md')
    return (folder, json.loads((folder / 'source.json').read_text(encoding='utf-8')),
            json.loads((folder / 'source-layout.json').read_text(encoding='utf-8')), nodes, figures, order)


class ComponentSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = json.loads((components.HERE / 'code_explanations.json').read_text(encoding='utf-8'))

    def test_explanation_fragments_reconstruct_every_original_character(self):
        self.assertEqual(len(self.records), 46)
        self.assertEqual(sum(len(r['rows']) for r in self.records), 84)
        for record in self.records:
            nodes = chapter(record['chapter'])[3]
            self.assertEqual(set(record['source_texts']), set(record['consume_ids']))
            for ident, original in record['source_texts'].items():
                with self.subTest(chapter=record['chapter'], source=ident):
                    self.assertEqual(original, nodes[ident]['text'])
                    fragments = sorted((f for row in record['rows'] for f in row['source_fragments']
                                        if f['source_id'] == ident), key=lambda f: f['start'])
                    cursor = 0
                    for fragment in fragments:
                        self.assertEqual(fragment['start'], cursor, '原文の重複または隙間')
                        self.assertEqual(fragment['text'], original[cursor:fragment['end']])
                        cursor = fragment['end']
                    self.assertEqual(cursor, len(original))
                    self.assertEqual(''.join(f['text'] for f in fragments), original)
            for row in record['rows']:
                meaning = ''.join(f['text'] for f in row['source_fragments'] if f['role'] == 'meaning')
                self.assertEqual(components.normalized(meaning), components.normalized(row['meaning']))

    def test_explanations_consume_each_id_once_and_reference_real_code_lines(self):
        consumed = Counter()
        for record in self.records:
            _, _, _, nodes, figures, order = chapter(record['chapter'])
            pages = {ident: p['source_page'] for p in order for ident in p['entries']}
            self.assertEqual({pages[i] for i in record['consume_ids']}, set(record['source_pages']))
            self.assertEqual(len(record['source_pages']), 1)
            self.assertEqual(record['anchor_id'], record['consume_ids'][0])
            self.assertFalse(set(record['consume_ids']) & figures.keys())
            consumed.update((record['chapter'], ident) for ident in record['consume_ids'])
            for row in record['rows']:
                self.assertTrue(set(row['source_ids']).issubset(record['consume_ids']))
                self.assertEqual(row['code'], '\n'.join(line['text'] for line in row['code_line_sources']))
                for line in row['code_line_sources']:
                    source = nodes[line['code_id']]
                    self.assertEqual(source['kind'], 'code')
                    numbered, current = {}, None
                    for text in source['text'].split('\n'):
                        match = re.match(r'^\s*(\d+):(.*)$', text)
                        if match:
                            current = int(match[1])
                            numbered[current] = match[2]
                        elif current is not None:
                            numbered[current] += '\n' + text
                    self.assertEqual(numbered[line['line_number']], line['text'], line)
        self.assertEqual(len(consumed), 163)
        self.assertTrue(all(count == 1 for count in consumed.values()))

    def test_plan_has_no_duplicate_consumption_and_preserves_five_filename_labels(self):
        labels = json.loads((components.HERE / 'filename_labels.json').read_text(encoding='utf-8'))
        self.assertEqual({(r['chapter'], r['code_id'], r['figure_id'], r['text']) for r in labels}, {
            ('03', 'p071-b03', 'p071-f07', 'application.properties'),
            ('03', 'p113-b04', 'p113-f49', 'pom.xml'),
            ('04', 'p149-b05', 'p149-f13', 'pom.xml'),
            ('04', 'p161-b02', 'p161-f24', '/resources/messages.properties'),
            ('05', 'p182-b04', 'p182-f15', 'pom.xml')})
        def fake_render(specs, _):
            for spec in specs:
                spec['result'] = {'parts': [dict(pdf='', width=spec['width'], height=1,
                    text='', pdf_text='', anchors={i: dict(x0=0, y0=0, x1=1, y1=1) for i in spec['consume']})]}
        for name in sorted({r['chapter'] for r in self.records}):
            with patch.object(components, '_render', fake_render):
                plan = components.prepare(*chapter(name))
            counts = Counter(i for spec in plan['specs'] for i in spec['consume'])
            self.assertTrue(all(count == 1 for count in counts.values()), name)
            expected = {i for r in self.records if r['chapter'] == name for i in r['consume_ids']}
            self.assertTrue(expected.issubset(plan['consume']), name)
            for label in (r for r in labels if r['chapter'] == name):
                matches = [s for s in plan['specs'] if label['code_id'] in s['consume'] and label['figure_id'] in s['consume']]
                self.assertEqual(len(matches), 1, label)
                file_items = re.findall(r'<span class="file-item"([^>]*)>(.*?)</span>', matches[0]['html'])
                self.assertTrue(any(unescape(text) == label['text'] and label['figure_id'] in attrs
                                    for attrs, text in file_items), label)

    def test_markdown_attributes_and_reference_file_languages_survive(self):
        nodes = chapter('04')[3]
        for ident, filename, language in (
            ('revision-messages-bundles', 'messages.properties', 'properties'),
            ('revision-messages-ja', 'messages_ja.properties', 'properties'),
            ('revision-messages-en', 'messages_en.properties', 'properties'),
            ('revision-messages-html', 'message.html', 'html')):
            with self.subTest(source=ident):
                self.assertEqual(nodes[ident]['attrs']['filename'], filename)
                self.assertEqual(nodes[ident]['attrs']['reference-group'], 'messages')
                self.assertEqual(nodes[ident]['language'], language)
                self.assertEqual(components.language(nodes[ident], filename), language)
        self.assertIn('#{screen.login}', nodes['revision-messages-html']['text'])

    def test_highlighting_keeps_leading_trailing_blank_lines_and_multiline_comments(self):
        class Text(HTMLParser):
            def __init__(self):
                super().__init__()
                self.parts = []
            def handle_data(self, data):
                self.parts.append(data)
        for source in ('\nclass Example {}\n\n', '\n/* 日本語の説明\n   複数行のコメント */\n\n',
                       '// 日本語の説明', 'String expression = "${product.id}";\n'):
            with self.subTest(source=source):
                html = components.highlighted(source, 'java')
                parser = Text()
                parser.feed(html)
                self.assertEqual(''.join(parser.parts), source)
                if '/*' in source or source.startswith('//'):
                    self.assertIn('class="comment"', html)


class BrowserComponentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = ROOT / 'tmp/html-components-tests'
        cls.work.mkdir(parents=True, exist_ok=True)
        short = components.code_html([{'number': 1, 'code': '// 日本語コメント', 'ids': ['comment-source']}],
            'java', [('非常に長いファイル名/MessageController.java', ['filename-source'])])
        rows = [{'number': i, 'code': f'int value{i:03d} = {i}; // 説明{i:03d}', 'ids': [f'row-{i:03d}']}
                for i in range(1, 81)]
        long_code = components.code_html(rows, 'java', [('LongCode.java', [])],
            '<div data-source-ids="footer-source">最後だけの補足</div>')
        node = {'rows': [['列名', '内容']] + [[f'項目{i:03d}', f'表の説明{i:03d}'] for i in range(1, 81)], 'has_header': True}
        table = components.table_html(cls.work, {}, 'table-source', node)
        folder, _, layout, nodes, _, _ = chapter('03')
        original_table = components.table_html(folder, layout, 'p069-table01', nodes['p069-table01'])
        record = {'owner_code_ids': [], 'rows': [dict(line_label='1 行', code='// 解説コメント',
            meaning='入力値を確認します。原文の説明を続けます。', source_ids=['explanation-source'],
            source_fragments=[{'source_id': 'explanation-source', 'role': 'meaning',
                               'text': '入力値を確認します。原文の説明を続けます。'}])]}
        explanation = components.explanation_html(record, {})
        cls.cards = [{'id': ident, 'width': 426.672, 'html': html} for ident, html in (
            ('short-code', short), ('long-code', long_code), ('long-table', table),
            ('original-table', original_table), ('explanation', explanation))]
        wrapped = components.code_html([{'number': 1, 'code': '// 折り返し確認', 'ids': ['wrapped-code-source']}],
            'java', [('非常に長いファイル名/授業教材/商品管理画面の入力値を確認する/MessageController.java', ['wrapped-filename-source'])])
        cls.cards.append({'id': 'wrapped-code', 'width': 240, 'html': wrapped})
        request = cls.work / 'request.json'
        request.write_text(json.dumps({'output_dir': str(cls.work / 'render'), 'cards': cls.cards}, ensure_ascii=False), encoding='utf-8')
        cls.env = dict(os.environ)
        cls.env.setdefault('NODE_PATH', str(components.RUNTIME / 'node/node_modules'))
        run = subprocess.run(['node', str(components.HERE / 'render_components.cjs'), str(request)],
            cwd=ROOT, env=cls.env, capture_output=True, text=True, encoding='utf-8')
        if run.returncode:
            raise AssertionError(run.stdout + run.stderr)
        cls.results = {c['id']: c['parts'] for c in json.loads((cls.work / 'render/results.json').read_text(encoding='utf-8'))['cards']}

    def test_actual_component_pdfs_are_single_page_and_keep_all_dom_text_and_anchors(self):
        for ident, parts in self.results.items():
            for index, part in enumerate(parts):
                with self.subTest(card=ident, part=index), fitz.open(part['pdf']) as pdf:
                    self.assertEqual(len(pdf), 1)
                    self.assertEqual(Counter(components.normalized(part['text'])), Counter(components.normalized(pdf[0].get_text())))
                    self.assertLessEqual(part['height'], 620.75)
                    # Chromiumの用紙寸法は1 CSS px（0.75pt）以内で丸められる。
                    self.assertLess(abs(pdf[0].rect.width - part['width']), .76)
                    self.assertLess(abs(pdf[0].rect.height - part['height']), .76)
                    for box in part['anchors'].values():
                        self.assertTrue(0 <= box['x0'] < box['x1'] <= part['width'] + .02)
                        self.assertTrue(0 <= box['y0'] < box['y1'] <= part['height'] + .02)

    def test_rows_are_not_lost_or_duplicated_and_headers_and_footer_repeat_correctly(self):
        code = self.results['long-code']
        table = self.results['long-table']
        self.assertGreater(len(code), 1)
        self.assertGreater(len(table), 1)
        code_ids = Counter(i for part in code for i in part['anchors'] if i.startswith('row-'))
        self.assertEqual(code_ids, Counter({f'row-{i:03d}': 1 for i in range(1, 81)}))
        table_text = components.normalized(''.join(p['text'] for p in table))
        for i in range(1, 81):
            self.assertEqual(table_text.count(f'項目{i:03d}'), 1)
        for parts, filename in ((code, 'LongCode.java'), (table, None)):
            for index, part in enumerate(parts):
                self.assertEqual('続き' in part['text'], index > 0)
                if filename:
                    self.assertIn(filename, part['text'])
                    self.assertEqual('最後だけの補足' in part['text'], index == len(parts) - 1)
                else:
                    self.assertIn('列名', part['text'])
                    self.assertIn('内容', part['text'])
                    self.assertIn('table-source', part['anchors'])

    def test_syntax_comments_are_green_and_original_table_colors_and_emphasis_survive(self):
        for ident, phrase in (('short-code', '日本語コメント'), ('explanation', '解説コメント')):
            with fitz.open(self.results[ident][0]['pdf']) as pdf:
                spans = [s for b in pdf[0].get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'] if phrase in s['text']]
                self.assertTrue(spans)
                self.assertTrue(all(s['color'] == 0x008000 and not s['flags'] & 2 for s in spans))
        colors = set()
        for part in self.results['original-table']:
            with fitz.open(part['pdf']) as pdf:
                colors.update(s['color'] for b in pdf[0].get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'])
        self.assertTrue({0x374151, 0xff0000}.issubset(colors))
        html = next(c['html'] for c in self.cards if c['id'] == 'original-table')
        self.assertIn('font-weight:700', html)
        self.assertIn('meaning-summary', next(c['html'] for c in self.cards if c['id'] == 'explanation'))
        # 合成太字はPDFのfont flagsに出ない書体もあるため、実DOMの適用結果も調べる。
        script = r'''const fs=require('node:fs');const {chromium}=require('playwright');
          (async()=>{const request=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
          const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
          try{const page=await browser.newPage();await page.setContent('<style>'+fs.readFileSync(process.argv[2],'utf8')+'</style>'+request.cards.map(c=>c.html).join(''));
          await page.evaluate(()=>document.fonts.ready);
          console.log(JSON.stringify(await page.evaluate(()=>({
            filenames:[...document.querySelectorAll('.filename')].map(e=>getComputedStyle(e).fontWeight),
            originalEmphasis:[...document.querySelectorAll('.source-style')].some(e=>Number(getComputedStyle(e).fontWeight)>=700),
            summaries:[...document.querySelectorAll('.meaning-summary')].map(e=>getComputedStyle(e).fontWeight)
          }))));}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});'''
        run = subprocess.run(['node', '-e', script, str(self.work / 'request.json'),
            str(components.HERE / 'components.css')], cwd=ROOT, env=self.env,
            capture_output=True, text=True, encoding='utf-8', check=True)
        applied = json.loads(run.stdout)
        self.assertTrue(all(int(weight) >= 700 for weight in applied['filenames']))
        self.assertTrue(applied['originalEmphasis'])
        self.assertTrue(applied['summaries'] and all(int(weight) >= 700 for weight in applied['summaries']))

    def test_filenames_embed_real_bold_font_and_keep_underlines_when_wrapped_or_continued(self):
        filenames = {
            'short-code': '非常に長いファイル名/MessageController.java',
            'wrapped-code': '非常に長いファイル名/授業教材/商品管理画面の入力値を確認する/MessageController.java',
            'long-code': 'LongCode.java',
        }
        for ident, filename in filenames.items():
            for part in self.results[ident]:
                with self.subTest(card=ident, pdf=part['pdf']), fitz.open(part['pdf']) as pdf:
                    page = pdf[0]
                    spans = [s for b in page.get_text('dict')['blocks'] for line in b.get('lines', [])
                             for s in line['spans'] if s['color'] == 0x123d68]
                    self.assertEqual(components.normalized(''.join(s['text'] for s in spans)),
                                     components.normalized(filename))
                    self.assertTrue(all(s['flags'] & 16 and s['font'] == 'Meiryo-Bold' for s in spans))
                    self.assertTrue(all(0 <= s['bbox'][0] < s['bbox'][2] <= part['width'] for s in spans))
                    underlines = [drawing for drawing in page.get_drawings()
                                  if drawing.get('fill') and all(abs(a-b) < .005 for a, b in
                                      zip(drawing['fill'], (18/255, 61/255, 104/255)))
                                  and .5 <= drawing['rect'].height <= 1 and drawing['rect'].width > 10]
                    self.assertGreaterEqual(len(underlines), len(spans))
                    if ident == 'wrapped-code':
                        self.assertGreater(len(spans), 1)

    def test_oversized_rows_and_overflowing_cells_fail_with_card_and_original_id(self):
        html = components.code_html([{'number': 1, 'code': '// 行\n' * 50, 'ids': ['oversized-source']}], 'java', [])
        table = components.table_html(self.work, {}, 'overflow-source',
            {'rows': [['金額', '説明'], ['1234567890' * 20, '確認']], 'has_header': True})
        for ident, source, body, width in (('oversized-card', 'oversized-source', html, 426.672),
                ('overflow-card', 'overflow-source', table, 160)):
            with self.subTest(card=ident):
                request = self.work / (ident + '.json')
                request.write_text(json.dumps({'output_dir': str(self.work / ident), 'cards': [
                    {'id': ident, 'width': width, 'html': body}]}, ensure_ascii=False), encoding='utf-8')
                run = subprocess.run(['node', str(components.HERE / 'render_components.cjs'), str(request)],
                    cwd=ROOT, env=self.env, capture_output=True, text=True, encoding='utf-8')
                self.assertNotEqual(run.returncode, 0)
                self.assertIn(ident, run.stderr)
                self.assertIn(source, run.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
