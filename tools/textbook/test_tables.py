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
                result[folder.name+'-'+ident]=dict(folder=folder,layout=layout,node=node,
                    html=components.table_html(folder,layout,ident,node))
    return result


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

    def test_product_names_constraints_and_numbers_align_by_column(self):
        product=tables()['03-p067-table03']['node']
        self.assertEqual(components.table_column_alignments(product),['right','left','right'])
        for ident in ('03-p067-table02','03-p073-table01'):
            node=tables()[ident]['node']
            self.assertEqual(components.table_column_alignments(node),
                ['right','left','left','left','right','left','left'])
        html=tables()['03-p067-table03']['html']
        self.assertIn('text-align:left">乾燥機能付き洗濯機',re.sub(r'<span[^>]*>|</span>','',html))

    def test_meaningful_fills_constraints_and_message_line_pairs_are_retained(self):
        self.assertIn('background:#ed7d31',tables()['03-p073-table01']['html'])
        self.assertIn('background:#fbe4d5',tables()['03-p067-table03']['html'])
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
        specs=[dict(id=ident,width=426.672,html=table['html']) for ident,table in tables().items()]
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

    def test_product_eight_is_left_aligned_like_the_other_product_names(self):
        with fitz.open(self.rendered['03-p067-table03'][0]['pdf']) as pdf:
            first=pdf[0].search_for('スマートテレビ')[0]
            eighth=pdf[0].search_for('乾燥機能付き洗濯機')[0]
            self.assertAlmostEqual(first.x0,eighth.x0,delta=.05)
            prices=[pdf[0].search_for(value)[0] for value in ('20000','15000','40000','60000')]
            self.assertLess(max(r.x1 for r in prices)-min(r.x1 for r in prices),.1)

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


if __name__=='__main__':
    unittest.main(verbosity=2)
