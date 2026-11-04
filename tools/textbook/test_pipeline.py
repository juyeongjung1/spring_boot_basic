"""原稿の欠落、座標の誤流用、編集後の自動改ページを検証する。"""
import json
import unittest

import pymupdf as fitz

from build import ROOT, build, normalized, read_markdown, source_layout


class TextbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / "docs/textbook/chapters/01"
        cls.layout = json.loads((cls.folder / "source-layout.json").read_text(encoding="utf-8"))
        cls.markdown = (cls.folder / "chapter.md").read_text(encoding="utf-8")
        cls.work = ROOT / "tmp/textbook-tests"
        cls.work.mkdir(parents=True, exist_ok=True)

    def test_every_source_block_survives_markdown(self):
        nodes, figures, _ = read_markdown(self.folder / "chapter.md")
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

    def test_added_paragraphs_reach_the_pdf_and_paginate(self):
        additions = []
        for i in range(1, 19):
            value = f"追加検証{i:03d}：**編集したMarkdown**からも本文を生成します。" + "元の位置情報に依存せず、文章の量に合わせて改ページします。" * 5
            additions.append(f'::: {{#addition-{i:03d} .paragraph}}\n\n{value}\n\n:::\n')
        last = self.markdown.rfind(":::")
        path = self.work / "edited.md"
        path.write_text(self.markdown[:last] + "\n".join(additions) + "\n" + self.markdown[last:], encoding="utf-8")
        report = build("01", "flow", path, self.work / "edited")
        original = json.loads((ROOT / "output/pdf/textbook/chapter-01/checks.json").read_text(encoding="utf-8"))
        self.assertGreater(report["flow"]["pages"], original["flow"]["pages"])
        self.assertTrue(report["flow"]["native_text_complete"])
        pdf = fitz.open(self.work / "edited/chapter-flow.pdf")
        content = normalized("".join(p.get_text() for p in pdf))
        for i in range(1, 19):
            self.assertEqual(content.count(f"追加検証{i:03d}"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
