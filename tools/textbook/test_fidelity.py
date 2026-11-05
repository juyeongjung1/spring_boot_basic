"""原文への復元と、行間・段落間・小見出しの余白を生成PDFで検証する。"""
import json
import unittest
from collections import Counter

import typst

from build import (ROOT, compile_pdf, flow_layout, native_runs, read_markdown,
                   style_header, updated_native_block)


class FidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = ROOT / 'tmp/fidelity-tests'
        cls.work.mkdir(exist_ok=True)
        folder = ROOT / 'docs/textbook/chapters/01'
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        source = style_header(layout['styles']) + '''
#set page(width: 340pt, height: 600pt, margin: 24pt)
#set text(font: "MS PMincho", size: 11.04pt, top-edge: "ascender", bottom-edge: "descender")
#set par(leading: 6.96pt, spacing: 12.96pt)
#paragraph("first", [第一段落の一行目です。#linebreak()第一段落の二行目です。])
#paragraph("second", [第二段落です。])
#instruction("group", above: 18pt)[
  #section-heading("heading", [2. 依存ライブラリの簡単な管理])
  #paragraph("third", [見出しに続く段落です。])
  #paragraph("fourth", [次の段落です。])
]
#paragraph("multi", [一つの要素内の第一段落です。#parbreak()一つの要素内の第二段落です。])
'''
        cls.pdf, path = compile_pdf(cls.work, 'spacing', source, ['C:/Windows/Fonts'])
        cls.marks = json.loads(typst.query(str(path), '<book-check>', field='value', format='json',
                                          root=str(ROOT), font_paths=['C:/Windows/Fonts']))

    def mark(self, ident, edge):
        return next(m for m in self.marks if m['id'] == ident and m['edge'] == edge)

    def test_paragraph_boundary_is_wider_than_a_line_break(self):
        first = self.pdf[0].search_for('第一段落の一行目です。')[0]
        second = self.pdf[0].search_for('第一段落の二行目です。')[0]
        next_paragraph = self.pdf[0].search_for('第二段落です。')[0]
        self.assertAlmostEqual(second.y0 - first.y0, 18, places=2)
        self.assertAlmostEqual(next_paragraph.y0 - second.y0, 24, places=2)
        gap = self.mark('fourth', 'start')['y'] - self.mark('third', 'end')['y']
        self.assertAlmostEqual(gap, 12.96, places=2)

    def test_grouped_heading_keeps_its_outer_space(self):
        before = self.mark('second', 'end')
        heading = self.mark('heading', 'heading')
        self.assertEqual(before['page'], heading['page'])
        self.assertAlmostEqual(heading['y'] - before['y'], 18, places=2)
        self.assertAlmostEqual(self.mark('third', 'start')['y'] - heading['y'], 23.04, places=2)

    def test_multiple_paragraphs_inside_one_element_have_the_same_spacing(self):
        first = self.pdf[0].search_for('一つの要素内の第一段落です。')[0]
        second = self.pdf[0].search_for('一つの要素内の第二段落です。')[0]
        self.assertAlmostEqual(second.y0 - first.y0, 24, places=2)
        self.assertAlmostEqual(first.x0, 35.04, places=2)
        self.assertAlmostEqual(second.x0, first.x0, places=2)

    def test_chapter_one_has_no_added_explanation_or_command_line_steps(self):
        folder = ROOT / 'docs/textbook/chapters/01'
        old, old_figures, old_order = read_markdown(folder / 'baseline.md')
        new, new_figures, new_order = read_markdown(folder / 'chapter.md')
        self.assertEqual(set(old), set(new))
        self.assertEqual(set(old_figures), set(new_figures))
        self.assertEqual(old_order, new_order)
        for ident, node in old.items():
            expected = node['text']
            if ident == 'p020-b10':
                expected = '本書では、Spring Framework 7.0.3を利用します。'
            if ident == 'p022-b08':
                expected += '。'
            self.assertEqual(expected, new[ident]['text'], ident)
        config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        source = flow_layout(folder, config, layout, new, new_figures, new_order)
        self.assertIn('#instruction("instruction-p022-b05", above: 18pt)', source)

    def test_native_punctuation_preserves_every_original_character_position(self):
        folder = ROOT / 'docs/textbook/chapters/front'
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        group = layout['blocks']['p012-b05']
        original = '\n'.join(line['text'] for line in group['lines'])
        updated = original.replace('選択します\n', '選択します。\n')
        prefix = style_header(layout['styles']) + '\n#set page(width: 595.32pt, height: 841.92pt, margin: 0pt)\n'
        prefix += '#set text(lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false)\n'
        old, _ = compile_pdf(self.work, 'native-before', prefix + '\n'.join(
            command for line in group['lines'] for command in native_runs(line['runs'])), ['C:/Windows/Fonts'])
        new, _ = compile_pdf(self.work, 'native-after', prefix + '\n'.join(
            updated_native_block(group, {'text': updated})), ['C:/Windows/Fonts'])

        def characters(pdf):
            return Counter((c['c'], round(c['origin'][0], 3), round(c['origin'][1], 3))
                           for b in pdf[0].get_text('rawdict')['blocks'] for line in b.get('lines', [])
                           for span in line['spans'] for c in span['chars'] if not c['c'].isspace())

        before, after = characters(old), characters(new)
        self.assertFalse(before - after)
        added = list((after - before).elements())
        self.assertEqual([c[0] for c in added], ['。'])
        self.assertLess(added[0][1], 420)
        with self.assertRaises(ValueError):
            updated_native_block(group, {'text': original.replace('選択します', 'クリックします')})

    def test_parallel_subheadings_are_all_classified_as_headings(self):
        for chapter, identifiers in {
            '03': ('p080-b06', 'p080-b10'),
            '07': ('p246-b03', 'p246-b06', 'p246-b09', 'p247-b03', 'p247-b05'),
        }.items():
            nodes, _, _ = read_markdown(ROOT / 'docs/textbook/chapters' / chapter / 'chapter.md')
            for ident in identifiers:
                self.assertEqual(nodes[ident]['kind'], 'heading', ident)

    def test_word_paragraphs_and_answer_choices_are_not_concatenated(self):
        for chapter, ident, breaks in [('04', 'p137-b04', 2), ('ex01', 'p009-b02', 4)]:
            folder = ROOT / 'docs/textbook/chapters' / chapter
            before, _, _ = read_markdown(folder / 'baseline.md')
            after, _, _ = read_markdown(folder / 'chapter.md')
            self.assertEqual(after[ident]['text'].count('\n\n'), breaks, ident)
            self.assertEqual(''.join(before[ident]['text'].split()), ''.join(after[ident]['text'].split()), ident)


if __name__ == '__main__':
    unittest.main(verbosity=2)
