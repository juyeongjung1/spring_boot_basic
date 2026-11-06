"""【】の原書体と小小見出しの太字を、実際のPDF文字で検証する。"""
import json
import unittest

from build import ROOT, compile_pdf, flow_layout, inline, read_markdown, style_header


class BracketHeadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / 'docs/textbook/chapters/02'
        cls.layout = json.loads((cls.folder / 'source-layout.json').read_text(encoding='utf-8'))
        cls.work = ROOT / 'tmp/bracket-heading-tests'
        cls.work.mkdir(exist_ok=True)
        cls.value = '【参考】サーブレットの基本'
        source = style_header(cls.layout['styles']) + '''
#set page(width: 340pt, height: 300pt, margin: 24pt)
#set text(font: "MS PMincho", size: 11.04pt, kerning: false, cjk-latin-spacing: none, overhang: false)
'''
        for y, style, heading in ((30, 's014', False), (70, 's014', True),
                                  (110, 's010', False), (150, 's010', True),
                                  (190, 's004', True)):
            source += (f'#at(24, {y}, text(top-edge: 0pt, bottom-edge: 0pt)['
                       + inline([(cls.value, style)], heading=heading) + '])\n')
        cls.pdf, _ = compile_pdf(cls.work, 'bracket-headings', source, ['C:/Windows/Fonts'])
        styles = {
            'regular': {'font': 'MS-PGothic', 'size': 9.96, 'color': '#000000', 'flags': 0, 'stroke': 0},
            'outlined': {'font': 'MS-PGothic', 'size': 9.96, 'color': '#000000', 'flags': 0, 'stroke': .28457},
            'bold': cls.layout['styles']['s004'],
        }
        source = style_header(styles) + '''
#set page(width: 180pt, height: 160pt, margin: 0pt)
#set text(lang: "ja", overhang: false, cjk-latin-spacing: none, kerning: false)
'''
        cls.native_positions = list(zip('【参考】サ', (24, 31.0621, 45.1021, 59.0157, 66.0779)))
        for y, style in ((30, 'regular'), (70, 'outlined'), (110, 'bold')):
            for char, x in cls.native_positions:
                source += f'#glyph({x}, {y}, "{char}", "{style}")\n'
        cls.native_pdf, _ = compile_pdf(cls.work, 'native-brackets', source, ['C:/Windows/Fonts'])

    def traces_at(self, y):
        return [t for t in self.pdf[0].get_texttrace() if t['chars']
                and abs(t['chars'][0][2][1] - (y + 24)) < .1]

    def test_regular_small_heading_is_outlined_without_changing_its_font_or_size(self):
        regular, heading = self.traces_at(30), self.traces_at(70)
        self.assertTrue(regular and heading)
        self.assertFalse(any(t['type'] == 1 for t in regular))
        self.assertTrue(any(t['type'] == 1 for t in heading))
        self.assertTrue(all(t['font'] == 'MS-PGothic' and abs(t['size'] - 12) < .01 for t in heading))
        for traces in (regular, heading):
            chars = [c for t in traces if t['type'] == 0 for c in t['chars']]
            self.assertEqual(''.join(chr(c[0]) for c in chars), self.value)
            self.assertAlmostEqual(chars[1][2][0] - chars[0][2][0], 6, places=2)

    def test_original_outline_and_large_bold_font_are_preserved(self):
        before, after = self.traces_at(110), self.traces_at(150)
        self.assertTrue(before and after)
        self.assertEqual([(t['font'], t['size'], t['type'], t['linewidth']) for t in before],
                         [(t['font'], t['size'], t['type'], t['linewidth']) for t in after])
        large = self.traces_at(190)
        self.assertTrue(large)
        self.assertTrue(all(t['font'] == 'MeiryoUI-Bold' and abs(t['size'] - 14.04) < .01 for t in large))
        self.assertFalse(any(t['type'] == 1 for t in large))

    def test_only_heading_rendering_requests_extra_emphasis(self):
        expected = {'02': ['p037-b01'],
                    '07': ['p246-b03', 'p246-b06', 'p246-b09', 'p247-b03', 'p247-b05']}
        for chapter, ids in expected.items():
            folder = ROOT / 'docs/textbook/chapters' / chapter
            nodes, figures, order = read_markdown(folder / 'chapter.md')
            config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
            layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
            source = flow_layout(folder, config, layout, nodes, figures, order)
            for ident in ids:
                line = next(line for line in source.splitlines() if line.startswith('#section-heading("' + ident + '"'))
                self.assertIn('heading: true', line, ident)
        folder = ROOT / 'docs/textbook/chapters/ex07'
        nodes, figures, order = read_markdown(folder / 'chapter.md')
        config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        source = flow_layout(folder, config, layout, nodes, figures, order)
        fragment = next(line for line in source.splitlines() if line.startswith('#section-heading("p067-b03"'))
        self.assertNotIn('heading: true', fragment)
        self.assertNotIn('heading: true', inline([('本文【参考】。', 's014')]))
        self.assertNotIn('flowing', inline([('【参考】', 's014')], typography=False))

    def test_native_brackets_and_neighboring_characters_keep_the_exact_source_coordinates(self):
        traces = self.native_pdf[0].get_texttrace()
        for y in (30, 70, 110):
            chars = [c for t in traces if t['type'] == 0 for c in t['chars'] if abs(c[2][1] - y) < .01]
            self.assertEqual(''.join(chr(c[0]) for c in chars), '【参考】サ')
            for char, (expected_char, expected_x) in zip(chars, self.native_positions):
                self.assertEqual(chr(char[0]), expected_char)
                self.assertAlmostEqual(char[2][0], expected_x, places=3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
