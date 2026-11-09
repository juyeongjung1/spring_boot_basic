"""小小見出しの追加余白と、指定した頁継続だけを実PDFで検証する。"""
from functools import lru_cache
import json
import unittest

import typst

from build import ROOT, compile_pdf, flow_layout, read_markdown, style_header
from test_illustrations import MODEL_EDITION, TABLE_EDITION, edition_json

REVIEW = ROOT/'output/verification/table-v6-2026'
REVIEWS = ((ROOT/'output/verification/spacing-v5-2026',TABLE_EDITION),(REVIEW,MODEL_EDITION))
read = lambda path: json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def plan(review=REVIEW):
    return read(review/'heading-spacing-plan.json')


@lru_cache(maxsize=None)
def chapter(name):
    folder=ROOT/'docs/textbook/chapters'/name
    nodes,figures,pages=read_markdown(folder/'chapter.md')
    return nodes,pages,read(folder/'source.json'),read(folder/'source-layout.json')


class MinorSpacingTests(unittest.TestCase):
    def test_only_accepted_flow_minor_headings_receive_the_extra_space(self):
        expected={name for collection in read(ROOT/'docs/textbook/collections.json').values() for name in collection['parts']}
        for review,edition in REVIEWS:
            self.assertEqual({part['chapter'] for part in plan(review)['chapters']},expected)
            self.assertEqual(plan(review)['extra_space_pt'],18)
            for part in plan(review)['chapters']:
                name=part['chapter']
                nodes,_,_,layout=chapter(name)
                config=edition_json('docs/textbook/chapters/'+name+'/source.json',edition)
                accepted=part['accepted']
                with self.subTest(review=review.name,chapter=name):
                    self.assertEqual(config.get('typography',{}),
                        {'minor_heading_extra_space':accepted} if accepted else {})
                    self.assertEqual(len(accepted),len(set(accepted)))
                    self.assertTrue(set(accepted).issubset(part['candidates']))
                    self.assertFalse(set(accepted)&{row['id'] for row in part['excluded']})
                    for ident in accepted:
                        self.assertEqual(nodes[ident]['kind'],'heading')
                        styles=[layout['styles'][(style or '').split(':')[-1]]
                                for text,style in nodes[ident]['parts'] if text.strip()]
                        self.assertTrue(styles,ident)
                        self.assertTrue(all(abs(s['size']-12)<.1 and 'Gothic' in s['font'] for s in styles),ident)

    def test_marker_pages_match_approved_spacing_baselines(self):
        for review,edition in REVIEWS:
            for part in plan(review)['chapters']:
                name=part['chapter']
                before=read(review/'spacing'/name/'baseline-marks.json')
                relative='output/pdf/textbook/chapter-'+name+'/checks.json'
                checks=edition_json(relative,edition)
                signature=lambda marks:[(m['id'],m['edge'],m['page']) for m in marks]
                with self.subTest(review=review.name,chapter=name):
                    self.assertEqual(signature(checks['flow']['block_positions']),signature(before))
                    self.assertEqual(checks['flow']['pages'],part['baseline_pages'])
                    self.assertEqual(part['pages'],part['baseline_pages'])
                    if review==REVIEW:
                        current=read(ROOT/relative)
                        if name!='02':
                            self.assertEqual(current,checks)
                            continue
                        # 追加余白の全13見出しを含む、図改訂前の範囲を照合する。
                        def through_source_58(marks):
                            index=next(i for i,m in enumerate(marks) if m['id']=='__source-page-58' and m['edge']=='source-page')
                            return marks[:index+1]
                        prefix=through_source_58(current['flow']['block_positions'])
                        self.assertEqual(signature(prefix),signature(through_source_58(before)))
                        self.assertAlmostEqual(prefix[-1]['y'],86,places=3)

    def test_the_two_requested_operation_headings_follow_the_previous_page(self):
        _,pages,config,_=chapter('02')
        marks=read(ROOT/'output/pdf/textbook/chapter-02/checks.json')['flow']['block_positions']
        for source,heading in [(51,'p051-b01'),(61,'p061-b01')]:
            with self.subTest(source_page=source):
                previous=next(p['entries'] for p in pages if p['source_page']==source-1)
                previous_end=max(m['page'] for m in marks if m['id'] in previous)
                boundary=next(m for m in marks if m['id']=='__source-page-'+str(source) and m['edge']=='source-page')
                title=next(m for m in marks if m['id']==heading and m['edge']=='heading')
                self.assertEqual(config['pagination']['continue_before'][str(source)],'short-minor-heading')
                self.assertEqual(boundary['page'],previous_end)
                self.assertEqual(title['page'],previous_end)

    def test_the_extra_space_adds_eighteen_points_in_an_actual_pdf(self):
        work=ROOT/'tmp/minor-spacing-tests'
        work.mkdir(parents=True,exist_ok=True)
        styles=read(ROOT/'docs/textbook/chapters/02/source-layout.json')['styles']
        nodes={ident:dict(kind=kind,text=text,parts=[(text,style)],attrs={}) for ident,kind,text,style in
            [('before','paragraph','見出しの前の本文です。','s009'),
             ('minor','heading','動作確認','s010'),('after','paragraph','見出しの後の本文です。','s009')]}
        entries=list(nodes)
        (work/'blank.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="595.32" height="841.92"/>',encoding='utf-8')
        (work/'sample.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20"><rect width="80" height="20" fill="white"/></svg>',encoding='utf-8')
        for grouped in (False,True):
            label='instruction' if grouped else 'heading'
            pages=[dict(id='page-1',source_page=1,entries=entries+(['sample'] if grouped else []))]
            figures={'sample':'sample.svg'} if grouped else {}
            geometry=[dict(id='sample',page=1,box=[85.104,0,165.104,20])] if grouped else []
            layout=dict(styles=styles,figures=geometry,blocks={},tables={},pages=[dict(pages[0],furniture=[],decoration='blank.svg')])
            positions=[]
            for spaced in (False,True):
                config=dict(first_page=1,last_page=1,chapter=99,cover_mode='none')
                if spaced:
                    config['typography']={'minor_heading_extra_space':['minor']}
                source=style_header(styles)+flow_layout(work,config,layout,nodes,figures,pages)
                pdf,path=compile_pdf(work,label+('-extra' if spaced else '-base'),source,['C:/Windows/Fonts'])
                try:
                    self.assertEqual(len(pdf),1)
                    marks=json.loads(typst.query(str(path),'<book-check>',field='value',format='json',
                        root=str(ROOT),font_paths=['C:/Windows/Fonts']))
                    positions.append(next(m for m in marks if m['id']=='minor' and m['edge']=='heading'))
                finally:
                    pdf.close()
            with self.subTest(grouped=grouped):
                self.assertEqual(positions[0]['page'],positions[1]['page'])
                self.assertAlmostEqual(positions[0]['x'],positions[1]['x'],places=3)
                self.assertAlmostEqual(positions[1]['y']-positions[0]['y'],18,places=3)


if __name__=='__main__':
    unittest.main(verbosity=2)
