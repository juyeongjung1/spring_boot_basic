"""索引の参照先とPDFリンクを検証する。"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pymupdf as fitz

from book_index import append_index, collect_anchor_pages, read_index

SOURCE = """| 用語 | 読み | 原稿の参照先 |
| --- | --- | --- |
| 外部キー | がいぶきー | 02:relation |
| @Controller | | 01:intro 02:relation 02:caption |
| 開発環境 | かいはつかんきょう | 01:intro |
"""


class BookIndexTest(unittest.TestCase):
    def test_page_numbers_follow_chapter_offsets(self):
        anchors = {}
        collect_anchor_pages("01", [{"id": "intro", "edge": "start", "page": 1}], 2, anchors)
        collect_anchor_pages("02", [
            {"id": "relation", "edge": "end", "page": 3},
            {"id": "relation", "edge": "heading", "page": 2},
            {"id": "caption", "edge": "start", "page": 2},
        ], 4, anchors)
        with TemporaryDirectory() as folder, fitz.open() as book:
            path = Path(folder) / "index.md"
            path.write_text(SOURCE, encoding="utf-8")
            for _ in range(6):
                book.new_page()

            report = append_index(book, path, anchors)
            self.assertEqual(report["pages"], [7, 7])
            self.assertEqual(report["entries"], [
                {"term": "@Controller", "pages": [2, 5]},
                {"term": "開発環境", "pages": [2]},
                {"term": "外部キー", "pages": [5]},
            ])
            with fitz.open(stream=book.tobytes(), filetype="pdf") as final:
                page = final[6]
                self.assertIn("索引", page.get_text())
                links = page.get_links()
                self.assertTrue(all(link["kind"] == fitz.LINK_GOTO for link in links))
                self.assertEqual(sorted(link["page"] + 1 for link in links), [2, 2, 5, 5])
                for i, link in enumerate(links):
                    self.assertTrue(all((link["from"] & other["from"]).is_empty for other in links[:i]))

    def test_removed_anchor_is_reported(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "index.md"
            path.write_text(SOURCE, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "外部キー.*02:relation"):
                read_index(path, {"01:intro": 2})


if __name__ == "__main__":
    unittest.main()
