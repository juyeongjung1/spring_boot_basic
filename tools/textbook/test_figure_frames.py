"""本文の独立図の採番と、付録の図番号の省略を検証する。"""
from functools import lru_cache
import json
import unittest

import pymupdf as fitz
import typst

from build import ROOT, compile_pdf, q, read_markdown, style_header
from figure_numbers import figure_numbers


@lru_cache(maxsize=None)
def chapters():
    result = []
    for folder in sorted((ROOT / 'docs/textbook/chapters').iterdir()):
        if not (folder / 'chapter.md').exists():
            continue
        config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        nodes, figures, order = read_markdown(folder / 'chapter.md')
        result.append((folder.name, config, layout, nodes, figures, order,
                       figure_numbers(config, layout, nodes, figures, order)))
    return result


class FigureNumberTests(unittest.TestCase):
    def test_numbered_figures_cover_all_independent_images(self):
        labels = json.loads((ROOT / 'tools/textbook/filename_labels.json').read_text(encoding='utf-8'))
        all_numbers = []
        for chapter, config, layout, nodes, figures, order, numbers in chapters():
            omitted = {r['figure_id'] for r in labels if r['chapter'] == chapter}
            if chapter == '03':
                omitted |= {'p071-f08', 'p113-f50'}
            omitted |= {f['id'] for f in layout['figures'] if f.get('slide')}
            if config.get('cover_mode', 'classic') != 'none':
                omitted |= set(order[0]['entries'])
            with self.subTest(chapter=chapter):
                if chapter in ('appendix-a', 'appendix-b'):
                    self.assertFalse(numbers)
                    continue
                self.assertEqual(set(numbers), set(figures) - omitted)
                for record in numbers.values():
                    self.assertRegex(record['number'], r'^図E?\d+\.\d+\.\d+$')
                    if record['caption_id']:
                        self.assertEqual(record['caption'], nodes[record['caption_id']]['text'])
                all_numbers += [r['number'] for r in numbers.values()]
        self.assertEqual(len(all_numbers), len(set(all_numbers)))

    def test_section_numbering_uses_main_section_not_subsection(self):
        nodes = {ident: dict(kind='heading', text=text, parts=[(text, 's1')]) for ident, text in
                 [('h1', '2.1. Web'), ('h2', '2.1.2. MVC'), ('h3', '2.2. Controller')]}
        figures = {'slide': 'slide.svg', 'a': 'a.svg', 'b': 'b.svg', 'c': 'c.svg'}
        layout = dict(figures=[dict(id='slide', slide='slide.pptx')], styles={})
        order = [dict(source_page=1, entries=['h1', 'slide', 'a', 'h2', 'b', 'h3', 'c'])]
        numbers = figure_numbers(dict(chapter=2, cover_mode='none'), layout, nodes, figures, order)
        self.assertEqual({i: n['number'] for i, n in numbers.items()},
                         dict(a='図2.1.1', b='図2.1.2', c='図2.2.1'))

    def test_only_actual_code_images_receive_figure_numbers(self):
        actual = {(chapter, ident) for chapter, config, layout, nodes, figures, order, numbers in chapters()
                  for ident, record in numbers.items() if record['kind'] == 'code'}
        self.assertEqual(actual, {('07', 'p243-f03'), ('07', 'p243-f04')})

    def test_left_margin_figure_keeps_image_position_and_number_inside_body(self):
        folder = ROOT / 'docs/textbook/chapters/03'
        layout = json.loads((folder / 'source-layout.json').read_text(encoding='utf-8'))
        figure = next(f for f in layout['figures'] if f['id'] == 'p109-f44')
        x0, y0, x1, y1 = figure['box']
        path = '/' + (folder / figure['path']).relative_to(ROOT).as_posix()
        work = ROOT / 'tmp/figure-cards-2026/left-margin-regression'
        work.mkdir(parents=True, exist_ok=True)
        source = style_header(layout['styles']) + '''
#set page(width: 595.32pt, height: 841.92pt,
  margin: (left: 85.104pt, right: 83.664pt, top: 86pt, bottom: 68pt))
#set text(font: "MS PMincho", size: 11.04pt, lang: "ja", cjk-latin-spacing: none,
  top-edge: "ascender", bottom-edge: "descender")
'''
        source += (f'#illustration("p109-f44", {q(path)}, {x1-x0}, '
                   f'offset: {x0-85.104}pt, number: "図3.7.1")')
        fonts = ['C:/Windows/Fonts']
        pdf, script = compile_pdf(work, 'left-margin', source, fonts)
        marks = json.loads(typst.query(str(script), '<book-check>', field='value', format='json',
                                     root=str(ROOT), font_paths=fonts, ignore_system_fonts=True))
        image_start = next(m for m in marks if m['id'] == 'p109-f44' and m['edge'] == 'start')
        number_start = next(m for m in marks if m['id'] == 'figure-number-p109-f44' and m['edge'] == 'start')
        self.assertAlmostEqual(image_start['x'], x0, places=3)
        self.assertAlmostEqual(number_start['x'], 85.104, places=3)
        number = pdf[0].search_for('図3.7.1')
        self.assertTrue(number)
        self.assertGreaterEqual(min(r.x0 for r in number), 85.103)

    def test_appendix_pdfs_have_no_figure_numbers(self):
        for chapter in ('appendix-a', 'appendix-b'):
            with self.subTest(chapter=chapter):
                folder = ROOT / 'output/pdf/textbook' / ('chapter-' + chapter)
                flow = json.loads((folder / 'checks.json').read_text(encoding='utf-8'))['flow']
                self.assertFalse(flow['numbered_figures'])
                self.assertFalse([m for m in flow['block_positions'] if m['id'].startswith('figure-number-')])
                with fitz.open(folder / 'chapter-flow.pdf') as pdf:
                    for page in pdf:
                        self.assertNotRegex(page.get_text(), r'図\s*[AB]\s*\.\s*\d')


if __name__ == '__main__':
    unittest.main()
