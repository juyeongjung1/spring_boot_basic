"""原稿の欠落、座標の誤流用、編集後の自動改ページを検証する。"""
import json
import unittest

import pymupdf as fitz

from build import ROOT, build, normalized, read_markdown, source_layout
from import_source import escape
from assemble import remove_number_text


class TextbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / "docs/textbook/chapters/01"
        cls.layout = json.loads((cls.folder / "source-layout.json").read_text(encoding="utf-8"))
        cls.markdown = (cls.folder / "baseline.md").read_text(encoding="utf-8")
        cls.work = ROOT / "tmp/textbook-tests"
        cls.work.mkdir(parents=True, exist_ok=True)

    def test_every_source_block_survives_markdown(self):
        nodes, figures, _ = read_markdown(self.folder / "baseline.md")
        self.assertEqual(set(nodes), set(self.layout["blocks"]))
        self.assertEqual(len(figures), 15)
        for ident, block in self.layout["blocks"].items():
            expected = "\n".join(l["text"] for l in block["lines"])
            self.assertEqual(nodes[ident]["text"], expected, ident)

    def test_duplicate_ids_are_rejected(self):
        path = self.work / "duplicate.md"
        path.write_text('::: {.source-page}\n\n::: {#same .paragraph}\n\n一つ目\n\n:::\n\n::: {#same .paragraph}\n\n二つ目\n\n:::\n\n:::\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "重複"):
            read_markdown(path)

    def test_thymeleaf_and_spaces_survive_inline_markdown(self):
        text='例：${emp == null}  と ${product.id} を保持します。'
        path=self.work/'thymeleaf.md'
        path.write_text('::: {.source-page}\n\n::: {#expression .paragraph}\n\n'+escape(text)+'\n\n:::\n\n:::\n',encoding='utf-8')
        nodes,_,_=read_markdown(path)
        self.assertEqual(nodes['expression']['text'],text)

    def test_single_row_table_without_header_keeps_its_data(self):
        path=self.work/'headerless.md'
        path.write_text('::: {.source-page}\n\n::: {#data .table has-header="false"}\n\n| | |\n| --- | --- |\n| category | ID |\n\n:::\n\n:::\n',encoding='utf-8')
        nodes,_,_=read_markdown(path)
        self.assertEqual(nodes['data']['rows'],[['category','ID']])

    def test_edited_text_cannot_reuse_old_positions(self):
        path = self.work / "changed.md"
        path.write_text(self.markdown.replace("章の概要", "章の概要を編集", 1), encoding="utf-8")
        nodes, figures, _ = read_markdown(path)
        with self.assertRaisesRegex(ValueError, "変更を検出"):
            source_layout(self.folder, self.layout, nodes, figures, path)

    def test_windows_newlines_keep_the_same_reference(self):
        path = self.work / "windows-newlines.md"
        path.write_bytes(self.markdown.replace("\n", "\r\n").encode("utf-8"))
        nodes, figures, _ = read_markdown(path)
        content = source_layout(self.folder, self.layout, nodes, figures, path)
        self.assertIn("#glyph(", content)

    def test_number_replacement_preserves_body_pixels_and_strokes(self):
        pdf=fitz.open(ROOT/'output/pdf/textbook/chapter-01/chapter-flow.pdf')
        index=next(i for i,p in enumerate(pdf) if i>0 and any(t['type']==1 for t in p.get_texttrace()))
        page=pdf[index]
        body=fitz.Rect(0,0,595.32,784)
        footer=fitz.Rect(240,786,355,817)
        before=page.get_pixmap(clip=body).samples
        widths=[t['linewidth'] for t in page.get_texttrace() if t['type']==1]
        self.assertTrue(widths)
        old=page.get_textbox(footer).strip()
        page=remove_number_text(page,[footer],old)
        self.assertEqual(page.get_textbox(footer).strip(),'')
        page.insert_text((290,797.04),'999',fontname='tiro',fontsize=11.04)
        pdf.subset_fonts()
        target=self.work/'renumbered.pdf'
        pdf.save(target,garbage=4,deflate=True)
        actual=fitz.open(target)[index]
        self.assertEqual(actual.get_pixmap(clip=body).samples,before)
        self.assertEqual([t['linewidth'] for t in actual.get_texttrace() if t['type']==1],widths)
        self.assertEqual(actual.get_textbox(footer).strip(),'999')

    def test_added_paragraphs_reach_the_pdf_and_paginate(self):
        additions = []
        for i in range(1, 19):
            value = f"追加検証{i:03d}：**編集したMarkdown**からも本文を生成します。" + "元の位置情報に依存せず、文章の量に合わせて改ページします。" * 5
            additions.append(f'::: {{#addition-{i:03d} .paragraph}}\n\n{value}\n\n:::\n')
        identifier='productRepository.findByNameLikeOrCategoryNameLikeOrDescriptionLikeOrBrandLikeOrSkuLike('
        code='\n'.join(f'{identifier}{i});' for i in range(40))
        additions.append(f'::: {{#long-code .code}}\n\n```java\n{code}\n```\n\n:::\n')
        rows='\n'.join(f'| 項目{i:03d} | 表の改ページも文字を失わず継続します。 |' for i in range(80))
        additions.append('::: {#long-table .table has-header="true"}\n\n| 列名 | 内容 |\n| --- | --- |\n'+rows+'\n\n:::\n')
        last = self.markdown.rfind(":::")
        path = self.work / "edited.md"
        path.write_text(self.markdown[:last] + "\n".join(additions) + "\n" + self.markdown[last:], encoding="utf-8")
        report = build("01", "flow", path, self.work / "edited")
        original = build("01", "flow", self.folder / "baseline.md", self.work / "unmodified")
        self.assertGreater(report["flow"]["pages"], original["flow"]["pages"])
        self.assertTrue(report["flow"]["native_text_complete"])
        table = next(c for c in report['flow']['html_components']
                     if c['kind'] == 'table' and 'long-table' in c['consume_ids'])
        self.assertGreater(len(table['parts']), 1)
        self.assertTrue(any(m['edge']=='long-code' and m['id']=='long-code' for m in report['flow']['block_positions']))
        pdf = fitz.open(self.work / "edited/chapter-flow.pdf")
        for part in table['parts']:
            position = next(m for m in report['flow']['block_positions']
                            if m['id'] == part['token'] and m['edge'] == 'html-component')
            area = fitz.Rect(position['x'], position['y'], position['x'] + part['width'], position['y'] + part['height'])
            repeated_header = normalized(pdf[position['page'] - 1].get_textbox(area))
            self.assertIn('列名', repeated_header)
            self.assertIn('内容', repeated_header)
        content = normalized("".join(p.get_text() for p in pdf))
        for i in range(1, 19):
            self.assertEqual(content.count(f"追加検証{i:03d}"), 1)
        for i in range(80):
            self.assertEqual(content.count(f'項目{i:03d}'), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
