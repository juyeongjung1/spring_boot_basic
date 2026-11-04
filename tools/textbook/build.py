"""同じMarkdownから元位置再現版と自動組版版を生成し、元PDFと照合する。"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess

import pymupdf as fitz
import typst
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FONT_FILES = ["msgothic.ttc", "msmincho.ttc", "meiryo.ttc", "meiryob.ttc", "arial.ttf", "arialbd.ttf", "ariblk.ttf", "segoeui.ttf", "segoeuib.ttf", "times.ttf", "timesbd.ttf", "timesi.ttf", "cour.ttf", "courbd.ttf", "courbi.ttf"]


def q(value):
    return json.dumps(value, ensure_ascii=False)


def normalized(value):
    return re.sub(r"\s+", "", value)


def font_style(style):
    name = style["font"]
    families = [("MS-PMincho", "MS PMincho"), ("MS-PGothic", "MS PGothic"), ("MS-Gothic", "MS Gothic"), ("MeiryoUI", "Meiryo UI"), ("Meiryo", "Meiryo"), ("TimesNewRoman", "Times New Roman"), ("Arial", "Arial"), ("CourierNew", "Courier New"), ("SegoeUI", "Segoe UI"), ("Wingdings", "Meiryo UI")]
    family = next((v for k, v in families if k in name), None)
    if family is None:
        raise ValueError(f"未登録のフォント: {name}")
    return dict(style, font=family, weight="black" if "Black" in name else "bold" if "Bold" in name else "regular", slant="italic" if "Italic" in name else "normal")


def flatten(nodes, style=None):
    """Pandocのインライン要素を、編集された文字と書式の列にする。"""
    result = []
    for node in nodes:
        kind, value = node["t"], node.get("c")
        if kind == "Str":
            result.append((value, style))
        elif kind in ("Space", "SoftBreak"):
            result.append((" ", style))
        elif kind == "LineBreak":
            result.append(("\n", style))
        elif kind == "Span":
            classes = value[0][1]
            base = next((c for c in classes if c.startswith("s") and c[1:].isdigit()), None)
            prefix = style.rsplit(":", 1)[0] + ":" if style and ":" in style else ""
            result += flatten(value[1], prefix + base if base else style)
        elif kind in ("Strong", "Emph", "Underline"):
            result += flatten(value, kind.lower() + ":" + (style or ""))
        elif kind == "Link":
            result += flatten(value[1], style)
        elif kind == "Code":
            result.append((value[1], style))
        else:
            raise ValueError(f"未対応のMarkdown: {kind}")
    return result


def read_markdown(path):
    run = subprocess.run(["pandoc", str(path), "-f", "markdown-smart-citations-implicit_figures", "--preserve-tabs", "-t", "json"], check=True, capture_output=True, encoding="utf-8")
    doc = json.loads(run.stdout)
    nodes, figures, order = {}, {}, []
    for page in doc["blocks"]:
        if page["t"] == "RawBlock":
            continue
        if page["t"] != "Div":
            raise ValueError("章の最上位はsource-pageのDivにしてください")
        entries = []
        for block in page["c"][1]:
            if block["t"] == "Div":
                attrs, children = block["c"]
                if not attrs[0] or attrs[0] in nodes or attrs[0] in figures:
                    raise ValueError(f"ブロックIDの欠落または重複: {attrs[0]}")
                parts = []
                language = None
                for child in children:
                    if child["t"] == "CodeBlock":
                        parts.append((child["c"][1], None))
                        language = next(iter(child["c"][0][1]), None)
                    elif child["t"] in ("Para", "Plain"):
                        if parts:
                            parts.append(("\n\n", None))
                        parts += flatten(child["c"])
                    else:
                        raise ValueError(f"未対応のブロック: {child['t']}")
                nodes[attrs[0]] = {"kind": attrs[1][0], "parts": parts, "text": "".join(p[0] for p in parts), "language": language}
                entries.append(attrs[0])
            elif block["t"] == "Para" and len(block["c"]) == 1 and block["c"][0]["t"] == "Image":
                image = block["c"][0]["c"]
                if not image[0][0] or image[0][0] in figures or image[0][0] in nodes:
                    raise ValueError("図版IDの欠落または重複")
                figures[image[0][0]] = image[2][0]
                entries.append(image[0][0])
            else:
                raise ValueError(f"未対応のページ要素: {block['t']}")
        order.append({"id": page["c"][0][0], "entries": entries})
    return nodes, figures, order


def style_header(styles):
    entries = []
    for ident, raw in styles.items():
        s = font_style(raw)
        entries.append(f'{ident}: (font: {q(s["font"])}, size: {s["size"]}, weight: {q(s["weight"])}, slant: {q(s["slant"])}, color: {q(s["color"])}, stroke: {s["stroke"]})')
    return '#let styles = (' + ',\n'.join(entries) + ',)\n' + (HERE / "book.typ").read_text(encoding="utf-8")


def native_runs(runs):
    commands = []
    for run in runs:
        for char, x in zip(run["text"], run["positions"]):
            if not char.isspace():
                commands.append(f'#glyph({x}, {run["y"]}, {q(char)}, {q(run["style"])})')
    return commands


def source_layout(folder, layout, nodes, figures, markdown):
    if hashlib.sha256(markdown.read_text(encoding="utf-8").encode("utf-8")).hexdigest() != layout["markdown_sha256"]:
        raise ValueError("Markdownの変更を検出しました。編集後は--mode flowを使用してください。元位置版の座標を無断で流用しません。")
    commands = ['#set page(width: 595.32pt, height: 841.92pt, margin: 0pt)', '#set text(lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false)']
    figure_map = {f["id"]: f for f in layout["figures"]}
    for index, page in enumerate(layout["pages"]):
        if index:
            commands.append('#pagebreak(weak: false)')
        commands.append(f'#at(0, 0, image({q("/" + (folder / page["decoration"]).relative_to(ROOT).as_posix())}, width: 595.32pt, height: 841.92pt))')
        commands += native_runs(page["furniture"])
        for ident in page["entries"]:
            if ident in figure_map:
                fig = figure_map[ident]
                x0, y0, x1, y1 = fig["box"]
                path = "/" + (folder / figures[ident]).relative_to(ROOT).as_posix()
                commands.append(f'#at({x0}, {y0}, image({q(path)}, width: {x1-x0}pt, height: {y1-y0}pt))')
            else:
                group = layout["blocks"][ident]
                assert nodes[ident]["text"] == "\n".join(l["text"] for l in group["lines"]), ident
                for line in group["lines"]:
                    commands += native_runs(line["runs"])
    return "\n".join(commands)


def inline(parts):
    result = []
    for value, style in parts:
        if value == "\n":
            continue
        if value == "\n\n":
            result.append("#parbreak()")
            continue
        fields = (style or "").split(":")
        content = f'#styled({q(fields[-1])}, {q(value)})' if fields[-1] else f'#text({q(value)})'
        for modifier in reversed(fields[:-1]):
            content = f'#{modifier}[{content}]'
        result.append(content)
    return "".join(result)


def flow_layout(folder, config, layout, nodes, figures, order):
    commands = [f'''#set page(width: 595.32pt, height: 841.92pt, margin: (left: 85.104pt, right: 83.664pt, top: 86pt, bottom: 68pt),
header: context if here().page() > 1 {{stack(spacing: 3pt, align(center, text(font: "Meiryo UI", size: 9.96pt, {q(config["title"])})), line(length: 100%, stroke: 0.48pt))}},
footer: context if here().page() > 1 {{align(center, text(font: "Times New Roman", size: 11.04pt, counter(page).display()))}})
#set text(font: "MS PMincho", size: 11.04pt, lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false, top-edge: "ascender", bottom-edge: "descender")
#set par(leading: 6.96pt, spacing: 6pt)
#show strong: it => text(font: "MS PGothic", stroke: 0.31543pt, it.body)
#counter(page).update({config["first_page"]})''']
    cover_page = order[0]
    cover_nodes = [(ident, nodes[ident]["text"]) for ident in cover_page["entries"] if ident in nodes]
    number = next(value.strip() for _, value in cover_nodes if value.strip().isdigit())
    title = next(value for _, value in cover_nodes if value.startswith("第"))
    goal_title = next(value for _, value in cover_nodes if "目標" in value)
    goals = [value.lstrip("◼■ ") for _, value in cover_nodes if value.startswith("◼")]
    commands += [f'#cover({q(number)}, {q(title)}, {q(goal_title)}, ({", ".join(q(v) for v in goals)},))', '#pagebreak(to: "odd")']
    figure_map = {f["id"]: f for f in layout["figures"]}
    def render(ident):
        if ident in figures:
            fig = figure_map.get(ident, {"box": [0, 0, 426.672, 0]})
            path = "/" + (folder / figures[ident]).relative_to(ROOT).as_posix()
            return f'#illustration({q(ident)}, {q(path)}, {fig["box"][2]-fig["box"][0]})'
        node = nodes[ident]
        if node["kind"] == "code":
            values = ",".join(q(l) for l in node["text"].split("\n"))
            return f'#code-panel({q(ident)}, ({values},), {q(node["language"])})'
        method = {"heading": "section-heading", "step": "step", "paragraph": "paragraph"}.get(node["kind"])
        if method is None:
            raise ValueError(f'未対応のブロック種類: {node["kind"]}')
        return f'#{method}({q(ident)}, [{inline(node["parts"])}])'

    entries = [ident for page in order[1:] for ident in page["entries"]]
    i = 0
    while i < len(entries):
        ident = entries[i]
        if ident in nodes and nodes[ident]["kind"] == "step":
            end = i + 1
            while end < len(entries) and entries[end] in nodes and nodes[entries[end]]["kind"] == "paragraph":
                end += 1
            if end < len(entries) and entries[end] in figures:
                body = "\n".join(render(e) for e in entries[i:end + 1])
                commands.append(f'#instruction({q("instruction-" + ident)})[{body}]')
                i = end + 1
                continue
        commands.append(render(ident))
        i += 1
    return "\n".join(commands)


def compile_pdf(work, name, content, font_paths):
    source = work / f"{name}.typ"
    source.write_text(content, encoding="utf-8", newline="\n")
    result = typst.compile(str(source), root=str(ROOT), font_paths=font_paths, ignore_system_fonts=True)
    return fitz.open(stream=result, filetype="pdf"), source


def pdf_image(page, scale=1.5):
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def build(chapter="01", mode="all", markdown=None, output=None):
    folder = ROOT / "docs/textbook/chapters" / chapter
    work = ROOT / "tmp/textbook" / chapter
    out = Path(output) if output else ROOT / "output/pdf/textbook" / f"chapter-{chapter}"
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    font_dir = work / "fonts"
    font_dir.mkdir(exist_ok=True)
    for name in FONT_FILES:
        dest = font_dir / name
        if not dest.exists():
            shutil.copyfile(Path("C:/Windows/Fonts") / name, dest)
    font_paths = [str(font_dir)]
    config = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    layout = json.loads((folder / "source-layout.json").read_text(encoding="utf-8"))
    markdown = Path(markdown) if markdown else folder / "chapter.md"
    nodes, figures, order = read_markdown(markdown)
    expected_ids = set(layout["blocks"])
    if mode in ("all", "reference"):
        assert set(nodes) == expected_ids, "元位置版のブロックIDが元データと一致しません"
        assert set(figures) == {f["id"] for f in layout["figures"]}, "元位置版の図版IDが一致しません"
    for path in figures.values():
        assert (folder / path).is_file(), path
    header = style_header(layout["styles"])
    report = {"chapter": chapter, "source_pages": [config["first_page"], config["last_page"]], "blocks": len(nodes), "figures": len(figures), "source_coverage": [p["coverage"] for p in layout["pages"]]}
    if mode in ("all", "reference"):
        original = fitz.open(ROOT / config["pdf"])
        assert hashlib.sha256(Path(original.name).read_bytes()).hexdigest() == layout["source_sha256"], "元PDFが取り込み時から変わっています"
        pdf, _ = compile_pdf(work, "reference-layout", header + source_layout(folder, layout, nodes, figures, markdown), font_paths)
        assert len(pdf) == config["last_page"] - config["first_page"] + 1
        pdf.save(out / "chapter-reference.pdf", garbage=4, deflate=True)
        comparisons = fitz.open()
        pages = []
        for index, info in enumerate(layout["pages"]):
            expected = "".join(r["text"] for r in info["furniture"]) + "".join(nodes[ident]["text"] for ident in info["entries"] if ident in nodes)
            actual = pdf[index].get_text()
            matches = Counter(normalized(expected)) == Counter(normalized(actual))
            if not matches:
                missing = Counter(normalized(expected)) - Counter(normalized(actual))
                extra = Counter(normalized(actual)) - Counter(normalized(expected))
                raise AssertionError(f'元位置版 {info["source_page"]}ページの文字差: 不足{dict(missing)} 余分{dict(extra)}')
            before = original[info["source_page"] - 1]
            a, b = pdf_image(before), pdf_image(pdf[index])
            Image.blend(a, b, 0.5).save(out / f'p{info["source_page"]:03d}-overlay.png')
            diff = ImageChops.difference(a, b)
            diff.convert("L").point(lambda v: 0 if v > 20 else 255).save(out / f'p{info["source_page"]:03d}-difference.png')
            p = comparisons.new_page(width=1210.64, height=869.92)
            p.insert_text((20, 18), f'元PDF {info["source_page"]}ページ', fontname="japan", fontsize=11)
            p.insert_text((635.32, 18), "Markdownから生成した元位置再現版", fontname="japan", fontsize=11)
            p.show_pdf_page(fitz.Rect(0, 28, 595.32, 869.92), original, info["source_page"] - 1)
            p.show_pdf_page(fitz.Rect(615.32, 28, 1210.64, 869.92), pdf, index)
            pages.append({"source_page": info["source_page"], "native_text_complete": matches, "mean_absolute_rgb_error_0_255": round(sum(ImageStat.Stat(diff).mean) / 3, 4)})
        comparisons.save(out / "comparison.pdf", garbage=4, deflate=True)
        report["reference"] = {"pages": len(pdf), "page_checks": pages}
    if mode in ("all", "flow"):
        pdf, source = compile_pdf(work, "flow", header + flow_layout(folder, config, layout, nodes, figures, order), font_paths)
        pdf.save(out / "chapter-flow.pdf", garbage=4, deflate=True)
        marks = json.loads(typst.query(str(source), "<book-check>", field="value", format="json", root=str(ROOT), font_paths=font_paths, ignore_system_fonts=True))
        orphan = []
        split_figures = []
        split_short_code = []
        split_instructions = []
        for i, m in enumerate(marks):
            if m["edge"] == "heading":
                following = next((n for n in marks[i + 1:] if n["edge"] in ("start", "heading")), None)
                if following and following["page"] != m["page"]:
                    orphan.append(m)
        for ident in figures:
            locations = [m["page"] for m in marks if m["id"] == ident]
            if len(locations) != 2 or locations[0] != locations[1]:
                split_figures.append(ident)
        for ident, node in nodes.items():
            if node["kind"] == "code" and len(node["text"].split("\n")) <= 37:
                locations = [m["page"] for m in marks if m["id"] == ident]
                if len(locations) != 2 or locations[0] != locations[1]:
                    split_short_code.append(ident)
        instruction_ids = {m["id"] for m in marks if m["id"].startswith("instruction-")}
        for ident in instruction_ids:
            places = [m for m in marks if m["id"] == ident]
            if len(places) != 2 or places[0]["page"] != places[1]["page"] or places[-1]["y"] > 778:
                split_instructions.append(ident)
        overflow = []
        actual_body = []
        for index, page in enumerate(pdf):
            for b in page.get_text("dict")["blocks"]:
                for line in b.get("lines", []):
                    x0, y0, x1, y1 = line["bbox"]
                    content = "".join(s["text"] for s in line["spans"])
                    if index > 0 and (y1 < 78 or (y0 > 784 and content.strip().isdigit())):
                        continue
                    actual_body.append(content)
                    if index == 0:
                        continue
                    if x0 < 78 or x1 > 545 or y1 > 778:
                        overflow.append({"page": index + 1, "bbox": list(line["bbox"])})
        expected = Counter(normalized("".join(n["text"] for n in nodes.values())).replace("◼", "■"))
        actual = Counter(normalized("".join(actual_body)).replace("◼", "■"))
        complete = expected == actual
        if not complete:
            raise AssertionError(f"自動組版の文字差: 不足{dict(expected-actual)} 余分{dict(actual-expected)}")
        report["flow"] = {"pages": len(pdf), "native_text_complete": complete, "heading_orphans": orphan, "split_figures": split_figures, "split_short_code": split_short_code, "split_instructions": split_instructions, "instruction_groups": len(instruction_ids), "overflow": overflow, "block_positions": marks}
        assert not orphan and not split_figures and not split_short_code and not split_instructions and not overflow, report["flow"]
    (out / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"chapter": chapter, "blocks": len(nodes), "figures": len(figures), "reference_pages": report.get("reference", {}).get("pages"), "flow_pages": report.get("flow", {}).get("pages")}, ensure_ascii=False))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default="01")
    parser.add_argument("--mode", choices=["all", "reference", "flow"], default="all")
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    build(args.chapter, args.mode, args.markdown)
