"""括弧の字幅・リンク・コード背景・表の線を、生成したPDFで確認する。"""
import json
import unittest

import pymupdf as fitz
import typst

from build import ROOT, compile_pdf, flatten, inline, style_header, typographic_parts
from links import add_url_links, visible_urls


class RemainingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = ROOT / 'tmp/remaining-tests'
        cls.work.mkdir(exist_ok=True)
        styles = {
            's001': {'font': 'MS-PMincho', 'size': 11.04, 'color': '#000000', 'flags': 4, 'stroke': 0},
            's002': {'font': 'MS-PGothic', 'size': 11.04, 'color': '#000000', 'flags': 0, 'stroke': .31543},
        }
        cls.url = 'http://localhost:8080/product/search'
        source = style_header(styles) + '\n#set page(width: 360pt, height: 650pt, margin: 24pt)\n#set text(font: "MS PMincho", size: 11.04pt, lang: "ja", kerning: false, overhang: false)\n'
        source += inline([('「Maven」【作業手順】（タイムリーフ）', 's001')])
        source += '\n#parbreak()\n' + inline([('「Bean」', 's002'), ('と呼ばれます。', 's001')])
        source += '\n#parbreak()\n' + inline([('Getter と Setter', 'strong:s001')])
        source += '\n#parbreak()\n#text("http://localhost:8080/")#linebreak()#text("product/search")\n#parbreak()\n'
        link = {'t': 'Link', 'c': [['', [], []], [{'t': 'Str', 'c': '開く'}], ['http://localhost:8080/login3', '']]}
        source += inline(flatten([link], 's001'))
        source += '\n#code-panel("settings", ("spring.thymeleaf.cache=false", "// 緑色のコメント"), "java")\n'
        source += '#table-panel("data", (("列", "内容"), ("id", "商品番号")), (1fr, 2fr), true)'
        source += '\n#paragraph("after-table", [表の後の説明です。])'
        source += '\n#instruction("picture-group")[#illustration("diagram", "/docs/textbook/chapters/01/assets/p018-f02.svg", 60)]'
        source += '\n#paragraph("after-picture", [図の後の説明です。])'
        pdf, path = compile_pdf(cls.work, 'remaining', source, ['C:/Windows/Fonts'])
        cls.marks = json.loads(typst.query(str(path), '<book-check>', field='value', format='json', root=str(ROOT), font_paths=['C:/Windows/Fonts']))
        cls.annotations = add_url_links(pdf, {'url': {'kind': 'paragraph', 'text': cls.url, 'parts': [(cls.url, None)]}})
        path = cls.work / 'remaining.pdf'
        pdf.save(path)
        cls.pdf = fitz.open(path)

    def test_brackets_have_full_width_in_regular_and_emphasized_text(self):
        seen = set()
        for block in self.pdf[0].get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    for char in span['chars']:
                        if char['c'] in '「」【】（）':
                            seen.add(char['c'])
                            self.assertAlmostEqual(char['bbox'][2] - char['bbox'][0], span['size'], places=2)
                            self.assertIn(span['font'], ('MS-Mincho', 'MS-Gothic'))
        self.assertEqual(seen, set('「」【】（）'))

    def test_manual_bracket_padding_is_removed_across_style_boundaries(self):
        parts = [('  「 ', 's001'), ('Maven', 's002'), (' 」 ', 's001')]
        self.assertEqual(''.join(v for v, _ in typographic_parts(parts)), '「Maven」')

    def test_named_markdown_link_and_wrapped_url_keep_their_destinations(self):
        links = self.pdf[0].get_links()
        self.assertEqual(sum(link.get('uri') == self.url for link in links), 2)
        self.assertTrue(any(link.get('uri') == 'http://localhost:8080/login3' for link in links))
        self.assertEqual(len(self.annotations), 2)
        self.assertNotEqual(self.annotations[0]['rect'][1], self.annotations[1]['rect'][1])

    def test_url_does_not_include_surrounding_punctuation(self):
        nodes = {'a': {'kind': 'paragraph', 'text': '', 'parts': [('（http://localhost:8080/login3）。', None)]}}
        self.assertEqual(visible_urls(nodes), ['http://localhost:8080/login3'])

    def test_explicit_emphasis_and_comments_are_visible(self):
        self.assertTrue(any(trace['type'] == 1 for trace in self.pdf[0].get_texttrace()))
        spans = [s for b in self.pdf[0].get_text('dict')['blocks'] for line in b.get('lines', []) for s in line['spans']]
        self.assertTrue(any('コメント' in span['text'] and span['color'] == 0x008000 for span in spans))

    def test_first_code_line_has_the_same_pale_background(self):
        page = self.pdf[0]
        first = page.search_for('spring.thymeleaf.cache=false')[0]
        backgrounds = [d['rect'] for d in page.get_drawings() if d['fill'] is not None
                       and all(abs(a - b) < .001 for a, b in zip(d['fill'], (1, 251 / 255, 240 / 255)))
                       and d['rect'].contains(first)]
        self.assertTrue(backgrounds)
        pixmap = page.get_pixmap(alpha=False)
        actual = pixmap.pixel(int(backgrounds[0].x0 + 2), int((first.y0 + first.y1) / 2))
        self.assertLessEqual(max(abs(a - b) for a, b in zip(actual, (255, 251, 240))), 1)

    def test_table_lines_have_consistent_width_and_contrast(self):
        lines = [d for d in self.pdf[0].get_drawings() if d.get('color') is not None
                 and all(abs(v - 64 / 255) < .001 for v in d['color'])]
        self.assertGreaterEqual(len(lines), 4)
        self.assertTrue(all(abs(d['width'] - .65) < .01 for d in lines))

    def test_table_has_space_before_the_following_paragraph(self):
        page = self.pdf[0]
        after = page.search_for('表の後の説明です。')[0]
        bottom = max(d['rect'].y1 for d in page.get_drawings() if d.get('color') is not None
                     and all(abs(v - 64 / 255) < .001 for v in d['color']))
        self.assertGreaterEqual(after.y0 - bottom, 6)

    def test_instruction_picture_has_space_before_the_following_paragraph(self):
        end = next(m for m in self.marks if m['id'] == 'diagram' and m['edge'] == 'end')
        after = next(m for m in self.marks if m['id'] == 'after-picture' and m['edge'] == 'start')
        self.assertEqual(end['page'], after['page'])
        self.assertGreaterEqual(after['y'] - end['y'], 6)


if __name__ == '__main__':
    unittest.main(verbosity=2)
