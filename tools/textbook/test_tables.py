"""表の専用デザイン、列整列、原文・配色と実PDFの可読性を検証する。"""
from collections import Counter
from functools import lru_cache
from html import unescape
from pathlib import Path
import json
import re
import unittest

import pymupdf as fitz

from build import ROOT, read_markdown
import html_components as components


@lru_cache(maxsize=1)
def tables():
    result={}
    for folder in sorted((ROOT/'docs/textbook/chapters').iterdir()):
        if not (folder/'chapter.md').exists():
            continue
        nodes,_,_=read_markdown(folder/'chapter.md')
        layout=json.loads((folder/'source-layout.json').read_text(encoding='utf-8'))
        for ident,node in nodes.items():
            if node['kind']=='table':
                width,_=components.table_dimensions(folder,layout,ident,node)
                result[folder.name+'-'+ident]=dict(folder=folder,layout=layout,node=node,width=width,
                    html=components.table_html(folder,layout,ident,node))
    return result


def pdf_grid(page):
    colors={(188,200,213),(135,155,175),(169,186,203)}
    rules=[drawing['rect'] for drawing in page.get_drawings() if drawing['fill']
           and tuple(round(value*255) for value in drawing['fill']) in colors
           and min(drawing['rect'].width,drawing['rect'].height)<=1.5]
    xs=sorted({round((rect.x0+rect.x1)/2,4) for rect in rules if rect.width<=1.5<rect.height})
    ys=sorted({round((rect.y0+rect.y1)/2,4) for rect in rules if rect.height<=1.5<rect.width})
    return rules,xs,ys


class TableSourceTests(unittest.TestCase):
    def test_all_tables_keep_the_original_cell_text_without_a_code_header(self):
        self.assertGreaterEqual(len(tables()),32)
        for ident,table in tables().items():
            with self.subTest(table=ident):
                html=table['html']
                actual=unescape(re.sub(r'<[^>]*>','',html))
                expected=''.join(cell for row in table['node']['rows'] for cell in row)
                self.assertEqual(components.normalized(actual),components.normalized(expected))
                self.assertNotIn('card-header',html)
                self.assertNotIn('language-badge',html)

    def test_every_header_is_centered_and_all_data_columns_are_left_aligned(self):
        product=tables()['03-p067-table03']['node']
        self.assertEqual(components.table_column_alignments(product),['left']*3)
        for ident in ('03-p067-table02','03-p073-table01'):
            node=tables()[ident]['node']
            self.assertEqual(components.table_column_alignments(node),['left']*7)
        for table in tables().values():
            self.assertTrue(all('text-align:center' in cell
                for cell in re.findall(r'<th\b[^>]*>',table['html'])))
            self.assertTrue(all('text-align:left' in cell
                for cell in re.findall(r'<td\b[^>]*>',table['html'])))
        html=tables()['03-p067-table03']['html']
        self.assertIn('text-align:left">乾燥機能付き洗濯機',re.sub(r'<span[^>]*>|</span>','',html))

    def test_short_tables_use_content_width_without_shrinking_description_tables(self):
        self.assertLess(tables()['03-p067-table01']['width'],250)
        self.assertLess(tables()['03-p067-table03']['width'],260)
        for ident in ('03-p069-table01','03-p071-b05','06-p200-table01','ex06-p059-table01'):
            self.assertEqual(tables()[ident]['width'],426.672)

    def test_modern_fill_styles_keep_constraints_and_message_line_pairs(self):
        for table in tables().values():
            self.assertNotIn('background:',table['html'])
        self.assertIn('color:#334155',tables()['03-p073-table01']['html'])
        self.assertIn('PRIMARY KEY<br>AUTO_INCREMENT',tables()['03-p073-table01']['html'])
        self.assertIn('<br>',tables()['ex04-p034-table01']['html'])
        comparison=tables()['03-p069-table01']['html']
        self.assertNotIn('<br>',comparison)
        self.assertIn('width:25.00000%',comparison)
        self.assertIn('width:37.50000%',comparison)
        self.assertIn('color:#ff0000',comparison)

    def test_property_keys_have_room_and_use_table_structure(self):
        node=dict(has_header=True,rows=[['設定項目','意味'],
            ['spring.datasource.url','データベースのURL'],
            ['spring.datasource.username','接続するユーザ名']])
        html=components.table_html(ROOT,{},'settings',node)
        self.assertIn('property-table',html)
        self.assertIn('width:43.00000%',html)
        self.assertIn('width:57.00000%',html)
        self.assertIn('<thead>',html)
        self.assertNotIn('card-header',html)

    def test_restored_employee_validation_row_keeps_its_original_red_text(self):
        table=tables()['ex04-p036-table01']
        node=table['node']
        self.assertEqual(len(node['rows']),5)
        self.assertEqual(node['rows'][1][0],'社員番号\n（アノテーション削除）')
        original=table['layout']['tables']['p036-table01']['rows']
        self.assertEqual(Counter(components.normalized(''.join(cell for row in node['rows'] for cell in row))),
                         Counter(components.normalized(''.join(cell for row in original for cell in row))))
        rows=re.findall(r'<tr[^>]*>(.*?)</tr>',table['html'],re.S)
        self.assertIn('color:#ff0000',rows[1])
        for row in rows[2:]:
            self.assertNotIn('color:#ff0000',row)


class TablePdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        specs=[dict(id=ident,width=table['width'],html=table['html']) for ident,table in tables().items()]
        components._render(specs,'tables-v4-tests')
        cls.rendered={spec['id']:spec['result']['parts'] for spec in specs}

    def test_all_real_tables_fit_and_the_pdf_keeps_every_cell(self):
        for ident,parts in self.rendered.items():
            with self.subTest(table=ident):
                self.assertEqual(len(parts),1)
                part=parts[0]
                self.assertLessEqual(part['height'],620.75)
                node=tables()[ident]['node']
                expected=''.join(cell for row in node['rows'] for cell in row)
                self.assertEqual(Counter(components.normalized(part['pdf_text'])),
                                 Counter(components.normalized(expected)))

    def test_product_names_and_prices_are_left_aligned_by_column(self):
        with fitz.open(self.rendered['03-p067-table03'][0]['pdf']) as pdf:
            first=pdf[0].search_for('スマートテレビ')[0]
            eighth=pdf[0].search_for('乾燥機能付き洗濯機')[0]
            self.assertAlmostEqual(first.x0,eighth.x0,delta=.05)
            prices=[pdf[0].search_for(value)[0] for value in ('20000','15000','40000','60000')]
            self.assertLess(max(r.x0 for r in prices)-min(r.x0 for r in prices),.1)

    def test_every_pdf_cell_aligns_and_the_complete_grid_stays_inside_the_clip(self):
        for ident,parts in self.rendered.items():
            with self.subTest(table=ident),fitz.open(parts[0]['pdf']) as pdf:
                page=pdf[0]
                rules,xs,ys=pdf_grid(page)
                node=tables()[ident]['node']
                self.assertEqual(len(xs),len(node['rows'][0])+1)
                self.assertEqual(len(ys),len(node['rows'])+1)
                self.assertLessEqual(max(rect.x1 for rect in rules),page.rect.width+.01)
                self.assertLessEqual(max(rect.y1 for rect in rules),min(page.rect.height,parts[0]['height'])+.01)
                self.assertGreaterEqual(min(rect.x0 for rect in rules),0)
                self.assertGreaterEqual(min(rect.y0 for rect in rules),0)
                for x in xs:
                    for top,bottom in zip(ys,ys[1:]):
                        self.assertTrue(any(rect.contains(fitz.Point(x,(top+bottom)/2)) for rect in rules))
                for y in ys:
                    for left,right in zip(xs,xs[1:]):
                        self.assertTrue(any(rect.contains(fitz.Point((left+right)/2,y)) for rect in rules))
                outer=[drawing['rect'] for drawing in page.get_drawings() if drawing['fill']
                       and tuple(round(value*255) for value in drawing['fill'])==(135,155,175)]
                for top,bottom in zip(ys,ys[1:]):
                    for x in (xs[0],xs[-1]):
                        self.assertTrue(any(rect.contains(fitz.Point(x,(top+bottom)/2)) for rect in outer))
                for left,right in zip(xs,xs[1:]):
                    for y in (ys[0],ys[-1]):
                        self.assertTrue(any(rect.contains(fitz.Point((left+right)/2,y)) for rect in outer))
                chars=[char for block in page.get_text('rawdict')['blocks']
                       for line in block.get('lines',[]) for span in line['spans']
                       for char in span['chars'] if components.normalized(char['c'])]
                for row,values in enumerate(node['rows']):
                    for column,value in enumerate(values):
                        cell=fitz.Rect(xs[column],ys[row],xs[column+1],ys[row+1])
                        inside=[char for char in chars if cell.contains(
                            (fitz.Rect(char['bbox']).tl+fitz.Rect(char['bbox']).br)/2)]
                        self.assertEqual(Counter(components.normalized(''.join(char['c'] for char in inside))),
                                         Counter(components.normalized(value)),(row,column,value))
                        lines={}
                        for char in inside:
                            lines.setdefault(round(char['origin'][1],1),[]).append(fitz.Rect(char['bbox']))
                        for boxes in lines.values():
                            left,right=min(box.x0 for box in boxes),max(box.x1 for box in boxes)
                            if row==0 and node['has_header']:
                                self.assertAlmostEqual((left+right)/2,(cell.x0+cell.x1)/2,delta=1)
                            else:
                                self.assertAlmostEqual(left-cell.x0,6.375,delta=1)

    def test_comparison_labels_and_technical_terms_are_not_split_in_the_middle(self):
        with fitz.open(self.rendered['03-p069-table01'][0]['pdf']) as pdf:
            page=pdf[0]
            for value in ('ハードコーディング','mysql-connector-j.jar',
                          'application.properties','DriverManager.getConnection'):
                self.assertEqual(len(page.search_for(value)),1,value)
            jdbc=min(page.search_for('JDBC'),key=lambda r:r.y0)
            self.assertAlmostEqual((jdbc.x0+jdbc.x1)/2,426.672*.4375,delta=1)

    def test_category_column_identifier_is_not_split_in_either_table(self):
        for ident in ('06-p197-table01','06-p200-table01'):
            with self.subTest(table=ident),fitz.open(self.rendered[ident][0]['pdf']) as pdf:
                lines=[''.join(span['text'] for span in line['spans'])
                       for block in pdf[0].get_text('dict')['blocks'] for line in block.get('lines',[])]
                self.assertEqual(lines.count('category_id'),1)

    def test_modern_pdf_palette_keeps_the_meaningful_red_emphasis(self):
        vivid={(237,125,49),(251,228,213),(255,255,0),(255,192,0)}
        header=(234,240,246)
        for ident,parts in self.rendered.items():
            with self.subTest(table=ident),fitz.open(parts[0]['pdf']) as pdf:
                fills={tuple(round(channel*255) for channel in drawing['fill'])
                       for drawing in pdf[0].get_drawings() if drawing['fill']}
                self.assertFalse(vivid & fills)
                if tables()[ident]['node']['has_header']:
                    self.assertIn(header,fills)
                if ident in {'03-p069-table01','ex04-p036-table01'}:
                    colors={span['color'] for block in pdf[0].get_text('dict')['blocks']
                            for line in block.get('lines',[]) for span in line['spans']}
                    self.assertIn(0xff0000,colors)


if __name__=='__main__':
    unittest.main(verbosity=2)
