"""独立図の採番・対象漏れと、固定ページの番号タブの干渉を検証する。"""
from functools import lru_cache
import json
import unittest

import typst

from build import ROOT, compile_pdf, q, read_markdown, style_header
from figure_numbers import figure_numbers, native_number_box


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


def intersects(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


class FigureNumberTests(unittest.TestCase):
    def test_numbered_figures_cover_all_independent_images(self):
        labels = json.loads((ROOT / 'tools/textbook/filename_labels.json').read_text(encoding='utf-8'))
        all_numbers = []
        for chapter, config, layout, nodes, figures, order, numbers in chapters():
            omitted = {r['figure_id'] for r in labels if r['chapter'] == chapter}
            if chapter == '03':
                omitted |= {'p071-f08', 'p113-f50'}
            excluded = set(config.get('unnumbered_figures', []))
            self.assertLessEqual(excluded, set(figures), chapter)
            omitted |= excluded | {f['id'] for f in layout['figures'] if f.get('slide')}
            if config.get('cover_mode', 'classic') != 'none':
                omitted |= set(order[0]['entries'])
            with self.subTest(chapter=chapter):
                self.assertEqual(set(numbers), set(figures) - omitted)
                for record in numbers.values():
                    self.assertRegex(record['number'], r'^図(?:E?\d+|A|B)\.\d+\.\d+$')
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

    def test_native_number_tabs_do_not_intersect_source_content(self):
        count = 0
        for chapter, config, layout, nodes, figures, order, numbers in chapters():
            for ident, record in numbers.items():
                if record['kind'] != 'native':
                    continue
                count += 1
                figure = next(f for f in layout['figures'] if f['id'] == ident)
                page = next(p for p in layout['pages'] if p['source_page'] == figure['page'])
                box = native_number_box(ident, record['number'], page, layout)
                obstacles = [f['box'] for f in layout['figures'] if f['page'] == figure['page']]
                obstacles += [r['bbox'] for b in layout['blocks'].values()
                              if b['source_page'] == figure['page'] for line in b['lines']
                              for r in line.get('runs', []) if r.get('bbox')]
                obstacles += [r['bbox'] for r in page['furniture'] if r.get('bbox')]
                with self.subTest(chapter=chapter, figure=ident):
                    self.assertTrue(0 <= box[0] < box[2] <= 595.32)
                    self.assertTrue(0 <= box[1] < box[3] <= 841.92)
                    self.assertFalse(any(intersects(box, obstacle) for obstacle in obstacles))
        self.assertEqual(count, 14)


if __name__ == '__main__':
    unittest.main()
