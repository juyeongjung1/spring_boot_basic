"""4種類の教材ページと、同じMarkdownから作る自動改ページ検証版。"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

import pymupdf as fitz
import typst
from PIL import Image, ImageChops, ImageStat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "output/pdf/prototype/extended"
WORK = ROOT / "tmp/extended-prototype"
FONTS = [str(WORK / "fonts")]


def q(value):
    return json.dumps(value, ensure_ascii=False)


def read_md(name):
    run = subprocess.run(["pandoc", str(HERE / name), "-f", "markdown-implicit_figures-citations", "--preserve-tabs", "-t", "json"], check=True, capture_output=True, encoding="utf-8")
    return json.loads(run.stdout)


def inline(nodes, flow=False):
    result = []
    for node in nodes:
        kind, value = node["t"], node.get("c")
        if kind == "Str":
            result.append(f'#text({q(value)})')
        elif kind in ("Space", "SoftBreak"):
            result.append(" ")
        elif kind == "LineBreak" or (kind == "RawInline" and value[1] == "<br>"):
            result.append("" if flow else "#linebreak()")
        elif kind == "Strong":
            result.append(f'#strong[{inline(value, flow)}]')
        elif kind == "Underline":
            result.append(f'#underline[{inline(value, flow)}]')
        elif kind == "Span":
            content = inline(value[1], flow)
            classes = value[0][1]
            if "underline" in classes:
                content = f'#underline[{content}]'
            if "red" in classes:
                content = f'#text(fill: red)[{content}]'
            result.append(content)
        elif kind == "Code":
            result.append(f'#text({q(value[1])})')
        else:
            raise ValueError(f"未対応のインライン要素: {kind}")
    return "".join(result)


def text(nodes):
    return "".join(n["c"] if n["t"] == "Str" else " " if n["t"] in ("Space", "SoftBreak", "LineBreak") else text(n["c"] if n["t"] == "Strong" else n["c"][1]) for n in nodes)


def blocks(doc, kind):
    return [b["c"] for b in doc["blocks"] if b["t"] == kind]


def cell(nodes, flow=False):
    return " ".join(inline(b["c"], flow) for b in nodes if b["t"] in ("Plain", "Para"))


def table_rows(doc):
    data = blocks(doc, "Table")[0]
    rows = data[3][1] + [row for body in data[4] for row in body[3]]
    return [[c[4] for c in row[1]] for row in rows]


def fixed_cell(nodes):
    """セル内の明示改行を保持し、各行をセル幅に収める。"""
    lines = [[]]
    def walk(items, red=False, underline=False):
        for node in items:
            kind, value = node["t"], node.get("c")
            if kind == "RawInline" and value[1] == "<br>":
                lines.append([])
            elif kind == "Span":
                walk(value[1], red or "red" in value[0][1], underline or "underline" in value[0][1])
            elif kind == "Underline":
                walk(value, red, True)
            elif kind in ("Str", "Space"):
                item = qcontent(value if kind == "Str" else " ")
                if underline:
                    item = f'#underline[{item}]'
                if red:
                    item = f'#text(fill: rgb("FF0000"))[{item}]'
                lines[-1].append(item)
            else:
                raise ValueError(kind)
    for block in nodes:
        walk(block["c"])
    return '#stack(dir: ttb, spacing: 7.44pt, ' + ', '.join('fit-line[' + ''.join(line) + ']' for line in lines) + ')'


def table(doc, flow=False, repeats=1):
    rows = table_rows(doc)
    header = rows[0]
    cells = [f'table.header(repeat: true, {", ".join("table.cell(align: center + horizon)[#text(weight: \"bold\")[" + cell(c, flow) + "]]" for c in header)})']
    for rep in range(repeats):
        for index, row in enumerate(rows[1:]):
            row_id = f"R{rep * 5 + index + 1:03d}"
            for col, content in enumerate(row):
                value = cell(content, flow) if flow else fixed_cell(content)
                if repeats > 1 and col == 0:
                    value = f'#text({q(row_id)})#linebreak()' + value
                if repeats > 1 and col == 2:
                    value += f'#linebreak()#text({q(row_id + "E")})'
                cells.append('table.cell(breakable: false)[' + value + ']')
    heights = "" if flow else "rows: (22.32pt, 75.96pt, 76.08pt, 57.96pt, 57.96pt, 58.32pt),"
    padding = "2pt" if flow else "0pt"
    return '''#block(width: 458.596pt)[
#set text(font: ("Segoe UI", "MS PGothic"), size: 10.56pt, fill: rgb("374151"), top-edge: 9.34pt, bottom-edge: 1.22pt)
#set par(leading: 7.44pt, spacing: 0pt)
#table(columns: (73.076pt, 191.09pt, 194.43pt), ''' + heights + '''
inset: (x: 2.4pt, y: ''' + padding + '''), align: left + horizon, stroke: 0.5pt + rgb("C8CBD5"),
''' + ",\n".join(cells) + ")\n]"


def fixed(name, doc):
    code = (HERE.parent / "layout.typ").read_text(encoding="utf-8") + "\n" + (HERE / "flow.typ").read_text(encoding="utf-8")
    heads = blocks(doc, "Header")
    paras = blocks(doc, "Para")
    lists = blocks(doc, "BulletList")
    commands = []
    if name == "chapter":
        number, title = text(heads[0][2]).split(" ", 1)
        commands += ['#panel(461.38, 0.12, 132.26, 127.7, fill: rgb(91.4%, 29.4%, 13.3%))', '#label(513.7, 88.46, "1", font: "Arial", weight: "black", size: 72, fill: white)', f'#label(92.064, 328.25, {q(number)}, size: 24, weight: "bold")', f'#label(164.06, 328.25, {q(title)}, size: 24, weight: "bold")', '#panel(83.664, 333.89, 428.11, 0.48, fill: black)', f'#label(85.104, 372.17, {q(text(heads[1][2]))}, size: 18, weight: "bold")']
        for i, item in enumerate(lists[0]):
            y = [401.69, 425.71, 449.71][i]
            commands += [f'#panel(97, {y - 9}, 7.5, 7.5, fill: black)', f'#label({127.7 if i < 2 else 127.1}, {y}, {q(text(item[0]["c"]))}, size: 14.04, weight: "bold")']
    else:
        header = text(doc["meta"]["header"]["c"])
        x, baseline, size = (207.53, 55.08, 9.96) if name == "body" else (240.41, 55.08, 9.96) if name == "table" else (235.73, 56.4, 11.04)
        commands += [f'#label({x}, {baseline}, {q(("  " if name == "body" else "") + header)}, size: {size})', f'#panel(83.664, {61.44 if name == "exercise" else 60}, 428.11, 0.48, fill: black)', f'#label(292.13, 797.04, {q(text(doc["meta"]["page"]["c"]))}, font: "Times New Roman", size: 11.04)']
        if name == "body":
            commands.append(f'#label(85.104, 98.42, {q(text(heads[0][2]))}, font: "MS PGothic", size: 12, stroke: 0.22pt)')
            for heading, y in zip(heads[1:], [146.06, 314.09, 440.11]):
                num, title = text(heading[2]).split(" ", 1)
                commands += [f'#at(96.144, {y}, body-style[{qcontent(num)}])', f'#at(118.1, {y}, body-style[{qcontent(title)}])']
            for i, (para, y) in enumerate(zip(paras, [170.06, 224.06, 248.09, 338.09, 464.11, 542.11, 584.14])):
                indent = "#h(2.76pt)" if i == 1 else "#h(11.04pt)"
                commands.append(f'#at(85.104, {y}, block(width: 450pt)[#body-style[{indent}{inline(para)}]])')
        elif name == "table":
            commands += ['#at(82.704, 104.8, ' + table(doc)[1:] + ')', f'#at(85.104, 497.35, block(width: 450pt)[#body-style[{inline(paras[0])}]])']
        else:
            commands.append(f'#at(85.104, 117.5, text(font: ("Arial", "MS PGothic"), size: 15.96pt, weight: "bold", stroke: 0.15pt, top-edge: 0pt, bottom-edge: 0pt)[{inline(heads[0][2])}])')
            for group, (heading, items, y) in enumerate(zip(heads[1:], lists, [165.98, 262.01, 382.01])):
                commands.append(f'#label(96.144, {y}, {q(text(heading[2]))}, font: "MS PGothic", size: 11.04, stroke: 0.22pt)')
                for i, item in enumerate(items):
                    yy = y + (24.02 if group == 2 else 24) + 24 * i
                    commands += [f'#at(102.1, {yy - 6.1}, circle(radius: 3.1pt, fill: black))', f'#at({123.62 if group == 2 else 123.5}, {yy}, body-style[{cell(item)}])']
    return code + "\n" + "\n".join(commands)


def qcontent(value):
    return f'#text({q(value)})'


def flow_base(title):
    return (HERE / "flow.typ").read_text(encoding="utf-8") + f'''
#set page(width: 595.32pt, height: 841.92pt, margin: (left: 83.664pt, right: 83.664pt, top: 90pt, bottom: 76pt),
  header: align(center, text(font: "Meiryo UI", size: 9.96pt)[{qcontent(title)}]),
  footer: align(center, context text(font: "Times New Roman", size: 11.04pt, counter(page).display())))
#show: body-style
#set text(top-edge: "ascender", bottom-edge: "descender")
#set par(leading: 6.96pt)
'''


def body_flow(doc, repeats=1):
    content = []
    paragraph_id = 0
    heading_id = 0
    for repeat in range(repeats):
        for b in doc["blocks"]:
            if b["t"] == "Header":
                heading_id += 1
                content.append(f'#flow-heading("H{heading_id:03d}", [{inline(b["c"][2], True)}])')
            elif b["t"] == "Para":
                paragraph_id += 1
                content.append(f'#flow-paragraph("P{paragraph_id:03d}", [{inline(b["c"], True)}])')
    return "\n".join(content)


def exercise_flow(doc, repeats=1):
    heads = blocks(doc, "Header")
    lists = blocks(doc, "BulletList")
    chunks = []
    for rep in range(repeats):
        for index, (heading, items) in enumerate(zip(heads[1:], lists)):
            ident = f"Q{rep * 3 + index + 1:03d}"
            chunks.append(f'#flow-question("{ident}", [{qcontent(ident)} {inline(heading[2], True)}], ({", ".join("[" + cell(item, True) + "]" for item in items)},))')
    return "\n".join(chunks)


def compile_pdf(name, content):
    path = WORK / f"{name}.typ"
    path.write_text(content, encoding="utf-8")
    output = OUT / f"{name}.pdf"
    typst.compile(str(path), output=str(output), root=str(ROOT), font_paths=FONTS, ignore_system_fonts=True)
    return fitz.open(output), path


def checkpoints(path):
    raw = typst.query(str(path), "<checkpoint>", field="value", format="json", root=str(ROOT), font_paths=FONTS, ignore_system_fonts=True)
    return json.loads(raw)


def no_overflow(pdf):
    errors = []
    for n, page in enumerate(pdf, 1):
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                x0, y0, x1, y1 = line["bbox"]
                value = "".join(s["text"] for s in line["spans"]).strip()
                if y1 < 76 or (y0 > 776 and value.isdigit()):
                    continue
                if x0 < 79 or x1 > 544 or y1 > 765.92:
                    errors.append({"page": n, "bbox": list(line["bbox"])})
    return errors


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "fonts").mkdir(exist_ok=True)
    # Windowsの静的フォントを明示。可変フォントの同名候補による字幅の変化を避ける。
    # 作業用フォルダーだけで使用し、フォントファイルをGit管理・配布しない。
    for filename in ["msgothic.ttc", "msmincho.ttc", "meiryo.ttc", "meiryob.ttc", "arial.ttf", "arialbd.ttf", "ariblk.ttf", "segoeui.ttf", "segoeuib.ttf", "times.ttf"]:
        target = WORK / "fonts" / filename
        if not target.exists():
            shutil.copyfile(Path("C:/Windows/Fonts") / filename, target)
    docs = {name: read_md(f"{name}.md") for name in ("chapter", "body", "table", "exercise")}
    sources = {"text": fitz.open(ROOT / "JAC0177G-T1-04(260715).pdf"), "exercise": fitz.open(ROOT / "JAC0177G-L1-04(260715).pdf")}
    combined, comparisons = fitz.open(), fitz.open()
    report = {"samples": [], "pagination": []}
    for name, source_kind, number in [("chapter", "text", 15), ("body", "text", 20), ("table", "text", 69), ("exercise", "exercise", 20)]:
        pdf, path = compile_pdf(name, fixed(name, docs[name]))
        assert len(pdf) == 1, (name, len(pdf))
        combined.insert_pdf(pdf)
        original = sources[source_kind]
        comparison = comparisons.new_page(width=1210.64, height=869.92)
        kind_label = {"chapter": "章扉", "body": "通常本文", "table": "表", "exercise": "演習"}[name]
        source_label = "本文" if source_kind == "text" else "演習ガイド"
        comparison.insert_text((20, 18), f"元PDF {source_label} {number}ページ", fontname="japan", fontsize=11)
        comparison.insert_text((635.32, 18), f"Markdownから生成した試作 {kind_label}", fontname="japan", fontsize=11)
        comparison.show_pdf_page(fitz.Rect(0, 28, 595.32, 869.92), original, number - 1)
        comparison.show_pdf_page(fitz.Rect(615.32, 28, 1210.64, 869.92), pdf, 0)
        imgs = []
        for page in [original[number - 1], pdf[0]]:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            imgs.append(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        Image.blend(*imgs, 0.5).save(OUT / f"{name}-overlay.png")
        diff = ImageChops.difference(*imgs)
        diff.convert("L").point(lambda v: 0 if v > 20 else 255).save(OUT / f"{name}-difference.png")
        comparison.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False).save(OUT / f"{name}-comparison.png")
        report["samples"].append({"kind": name, "source": source_kind, "source_page": number, "mean_absolute_rgb_error_0_255": round(sum(ImageStat.Stat(diff).mean) / 3, 3), "source_sha256": hashlib.sha256(Path(original.name).read_bytes()).hexdigest()})
    combined.save(OUT / "samples.pdf")
    comparisons.save(OUT / "comparisons.pdf")

    # 改行指示を外し、同じMarkdownの文章を自動折り返し・自動改ページする。
    normal = flow_base("通常本文の自動組版") + body_flow(docs["body"])
    pdf, _ = compile_pdf("body-flow", normal)
    report["pagination"].append({"case": "body-original", "pages": len(pdf), "overflow": no_overflow(pdf)})
    # 本文を4回繰り返し、見出しと直後の段落の分離を検査。
    pdf, path = compile_pdf("body-stress", flow_base("本文増量による改ページ検証") + body_flow(docs["body"], 4))
    marks = checkpoints(path)
    orphan = []
    for i, mark in enumerate(marks):
        if mark["edge"] == "heading":
            following = next((m for m in marks[i + 1:] if m["edge"] == "start"), None)
            if following and following["page"] != mark["page"]:
                orphan.append(mark)
    paragraphs = {}
    for m in marks:
        if m["id"].startswith("P"):
            paragraphs.setdefault(m["id"], []).append(m["page"])
    assert len(paragraphs) == 28
    report["pagination"].append({"case": "body-times4", "pages": len(pdf), "heading_orphans": orphan, "paragraph_count": len(paragraphs), "overflow": no_overflow(pdf)})
    long_text = " ".join(qcontent(f"長文{i:03d}") + inline(blocks(docs["body"], "Para")[0], True) for i in range(1, 21))
    pdf, path = compile_pdf("paragraph-stress", flow_base("長い段落の継続と文字欠落の検証") + f'#flow-paragraph("long", [{long_text}])')
    missing = [i for i in range(1, 21) if sum(len(p.search_for(f"長文{i:03d}")) for p in pdf) != 1]
    fragments = []
    actual_text = []
    for p in pdf:
        content_lines = [l for b in p.get_text("dict")["blocks"] for l in b.get("lines", []) if 76 < l["bbox"][1] < 770]
        ys = {round(l["bbox"][1], 1) for l in content_lines}
        actual_text.extend("".join(s["text"] for s in line["spans"]) for line in content_lines)
        fragments.append(len(ys))
    actual = re.sub(r"\s+|長文\d{3}", "", "".join(actual_text))
    expected = re.sub(r"\s+", "", text(blocks(docs["body"], "Para")[0])) * 20
    assert actual == expected, "長い段落に文字の欠落または重複があります"
    report["pagination"].append({"case": "long-paragraph-times20", "pages": len(pdf), "missing_text_ids": missing, "full_text_matches": actual == expected, "body_lines_per_page": fragments, "overflow": no_overflow(pdf)})
    assert len(pdf) > 1 and min(fragments) >= 2
    # 5行の比較表を12回、計60行にしてヘッダー反復と行の分離を検査。
    pdf, path = compile_pdf("table-stress", flow_base("表60行の改ページ検証") + table(docs["table"], True, 12))
    missing_headers, split_rows = [], []
    for n, page in enumerate(pdf, 1):
        if not all(word in page.get_text() for word in ["要素", "JDBC", "Spring Data JPA"]):
            missing_headers.append(n)
    for row in range(1, 61):
        ident = f"R{row:03d}"
        starts = [n for n, p in enumerate(pdf, 1) if ident in p.get_text().split()]
        ends = [n for n, p in enumerate(pdf, 1) if ident + "E" in p.get_text().split()]
        if len(starts) != 1 or starts != ends:
            split_rows.append(ident)
    report["pagination"].append({"case": "table-60rows", "pages": len(pdf), "missing_headers": missing_headers, "missing_or_split_rows": split_rows, "overflow": no_overflow(pdf)})
    # 3問を8回、計24問にして設問と箇条書きをまとめて移動することを検査。
    pdf, path = compile_pdf("exercise-stress", flow_base("演習24問の改ページ検証") + exercise_flow(docs["exercise"], 8))
    groups = {}
    for m in checkpoints(path):
        groups.setdefault(m["id"], []).append(m["page"])
    split_questions = [ident for ident, pages in groups.items() if len(pages) != 2 or pages[0] != pages[1]]
    assert len(groups) == 24
    report["pagination"].append({"case": "exercise-24questions", "pages": len(pdf), "split_questions": split_questions, "question_count": len(groups), "overflow": no_overflow(pdf)})
    # ページ末尾に収まらない図とキャプションが、一緒に次ページへ移ることを検査。
    before = body_flow(docs["body"])
    figure = '''#block(breakable: false, above: 12pt)[
#checkpoint("figure", "start")
#image("/docs/prototype/assets/findall-slide.svg", width: 369.2pt)
#v(6pt)
図の説明とスライドを同じページに配置する検証
#checkpoint("figure", "end")
]'''
    pdf, path = compile_pdf("figure-stress", flow_base("図と説明の改ページ検証") + before + figure)
    locs = [m["page"] for m in checkpoints(path) if m["id"] == "figure"]
    report["pagination"].append({"case": "figure-with-caption", "pages": len(pdf), "figure_pages": locs, "moved_together": len(locs) == 2 and locs[0] == locs[1] and locs[0] > 1, "overflow": no_overflow(pdf)})

    pagination = fitz.open()
    for case, name in zip(report["pagination"], ["body-flow", "body-stress", "paragraph-stress", "table-stress", "exercise-stress", "figure-stress"]):
        first = len(pagination) + 1
        pagination.insert_pdf(fitz.open(OUT / f"{name}.pdf"))
        case["combined_pages"] = [first, len(pagination)]
    pagination.save(OUT / "pagination.pdf")
    (OUT / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    for case in report["pagination"]:
        for key in ["overflow", "heading_orphans", "missing_headers", "missing_or_split_rows", "split_questions", "missing_text_ids"]:
            assert not case.get(key), (case["case"], key, case.get(key))
    assert report["pagination"][-1]["moved_together"]


if __name__ == "__main__":
    main()
