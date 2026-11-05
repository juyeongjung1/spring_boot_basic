"""Word由来の箇条書きをカラー絵文字へ代替しないことを検証する。"""
from collections import Counter
import unittest

from build import ROOT, compile_pdf, inline, native_runs, normalized, plain_symbols, style_header


class PlainSymbolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work=ROOT/'tmp/symbol-tests'
        cls.work.mkdir(parents=True,exist_ok=True)
        cls.styles={'s001':{'font':'Wingdings-Regular','size':16,'color':'#000000','flags':0,'stroke':0}}
        cls.original='◼⚫▪■●•\uf09f○'
        run={'text':cls.original,'positions':[24+32*i for i in range(len(cls.original))],'y':40,'style':'s001'}
        content=style_header(cls.styles)+'\n#set page(width:320pt,height:140pt,margin:0pt)\n'
        content+='\n'.join(native_runs([run]))
        content+='\n#at(24,90)['+inline([(cls.original,'s001')])+']'
        cls.pdf,_=compile_pdf(cls.work,'plain-symbols',content,['C:/Windows/Fonts'])
        cls.pdf.save(cls.work/'plain-symbols.pdf',garbage=4,deflate=True)

    def test_only_bullet_codepoints_are_normalized(self):
        self.assertEqual(plain_symbols('◼⚫\uf09f▪■●•○'),'■●•▪■●•○')
        self.assertEqual(plain_symbols('Java 21: ${product.id} → \uf0df'),'Java 21: ${product.id} → \uf0df')
        self.assertEqual(normalized('◼ ⚫ \uf09f'),normalized('■●•'))

    def test_native_and_flow_symbols_use_the_monochrome_font(self):
        page=self.pdf[0]
        self.assertEqual(Counter(normalized(page.get_text())),Counter(normalized(self.original*2)))
        symbols=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
        self.assertTrue(symbols)
        self.assertTrue(all(s['font']=='MS-Gothic' for s in symbols),[(s['text'],s['font']) for s in symbols])
        self.assertNotIn('◼',page.get_text())
        self.assertNotIn('⚫',page.get_text())
        pix=page.get_pixmap(alpha=False)
        self.assertTrue(all(r==g==b for r,g,b in zip(pix.samples[0::3],pix.samples[1::3],pix.samples[2::3])))


if __name__=='__main__':
    unittest.main(verbosity=2)
