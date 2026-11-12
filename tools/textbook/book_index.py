"""索引の原稿から、組版済み本文へリンクする巻末ページを作る。"""
from collections import Counter
import json
from pathlib import Path
import re
from shutil import copyfile
from tempfile import TemporaryDirectory
import unicodedata

import pymupdf as fitz

from build import HERE, ROOT, compile_pdf

FULLWIDTH_INITIALS = str.maketrans(
    ".0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "．０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
)
SMALL_KANA = str.maketrans("ぁぃぅぇぉっゃゅょゎ", "あいうえおつやゆよわ")
ANCHOR_EDGES = {"start", "heading", "source-page", "native-page"}
LINK_PREFIX = "https://index.invalid/"


def collect_anchor_pages(chapter, marks, physical_pages, anchor_pages):
    for mark in marks:
        if mark["edge"] in ANCHOR_EDGES:
            anchor = f'{chapter}:{mark["id"]}'
            page = physical_pages[mark["page"] - 1]
            anchor_pages[anchor] = min(anchor_pages.get(anchor, page), page)


def sort_key(term, reading):
    if reading:
        folded = unicodedata.normalize("NFD", reading).translate(SMALL_KANA)
        primary = "".join(char for char in folded if not unicodedata.combining(char))
        if not re.fullmatch(r"[ぁ-ゖ][ぁ-ゖー]*", reading):
            raise ValueError(f"索引語の読みはひらがなで指定してください: {term}")
        return (1, primary, reading, term), primary[0]
    primary = re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKC", term).lower())
    if not primary or re.search(r"[^\x20-\x7e]", term):
        raise ValueError(f"索引語に読みを指定してください: {term}")
    initial = "." if term.startswith(".") else primary[0].upper()
    return (0, initial, primary, term), initial.translate(FULLWIDTH_INITIALS)


def read_index(path, anchor_pages):
    """Markdown表を読み、組版結果に基づいて索引語を分類する。"""
    entries = []
    terms = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        term, reading, refs = (value.strip() for value in line.strip("|").split("|"))
        if term == "用語" or term == "---":
            continue
        if not term or term in terms or not refs:
            raise ValueError(f"索引語の重複または参照先の欠落: {term}")
        missing = set(refs.split()) - anchor_pages.keys()
        if missing:
            raise ValueError(f"索引語 {term} の参照先が見つかりません: {', '.join(sorted(missing))}")
        order, section = sort_key(term, reading)
        pages = sorted({anchor_pages[ref] for ref in refs.split()})
        entries.append((order, section, {"term": term, "pages": pages}))
        terms.add(term)

    if not entries:
        raise ValueError("索引語がありません")
    groups = {}
    for _, section, entry in sorted(entries):
        groups.setdefault(section, []).append(entry)
    return [{"section": section, "entries": rows} for section, rows in groups.items()]


def append_index(flow, index_path, anchor_pages):
    groups = read_index(index_path, anchor_pages)
    entries = [entry for group in groups for entry in group["entries"]]
    first = len(flow) + 1
    expected = Counter(number for entry in entries for number in entry["pages"])

    work = ROOT / "tmp/textbook/index"
    work.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=work) as folder:
        folder = Path(folder)
        fonts = folder / "fonts"
        fonts.mkdir()
        for name in ("msmincho.ttc", "msgothic.ttc", "times.ttf"):
            copyfile(Path("C:/Windows/Fonts") / name, fonts / name)
        data = {"first_page": first, "groups": groups}
        (folder / "index-data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        part, _ = compile_pdf(folder, "index", (HERE / "index.typ").read_text(encoding="utf-8"),
                              [str(fonts)])

    flow.insert_pdf(part, links=False)
    actual = Counter()
    footer = fitz.Rect(240, 786, 355, 817)
    for index_page in part:
        number = first + index_page.number
        page = flow[number - 1]
        assert page.get_textbox(footer).strip() == str(number), number
        for link in index_page.get_links():
            uri = link.get("uri", "")
            assert uri.startswith(LINK_PREFIX), uri
            target = int(uri.removeprefix(LINK_PREFIX))
            assert 1 <= target < first, target
            # 索引の文字はベースラインに置くため、数字の上下までクリック領域を広げる。
            rect = link["from"] + (0, -9, 0, 2)
            page.insert_link({"kind": fitz.LINK_GOTO, "from": rect, "page": target - 1})
            actual[target] += 1
    assert actual == expected, "索引のページ番号とリンク先が一致しません"
    return {"pages": [first, len(flow)], "entry_count": len(entries),
            "internal_links": sum(actual.values()), "entries": entries}
