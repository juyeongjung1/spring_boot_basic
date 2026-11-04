"""Markdownから本文85ページを組版し、元PDFと比較する試作。"""
from pathlib import Path
from zipfile import ZipFile
import argparse
import hashlib
import json
import re
import subprocess

import pymupdf as fitz
import typst
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "output/pdf/prototype"
ASSETS = HERE / "assets"


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def plain(inlines):
    return "".join(i["c"] if i["t"] == "Str" else " " if i["t"] in ("Space", "SoftBreak") else plain(i["c"]) for i in inlines)


def build():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=ROOT / "JAC0177G-T1-04(260715).pdf")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    source = fitz.open(args.reference)
    reference = fitz.open()
    reference.insert_pdf(source, from_page=84, to_page=84)
    reference.save(OUT / "reference-page85.pdf")
    # スライドだけをベクター図版として保存。ページ全体の画像化はしない。
    source[84].set_cropbox(fitz.Rect(113.06, 114.62, 482.26, 389.81))
    if not (ASSETS / "findall-slide.svg").exists():
        (ASSETS / "findall-slide.svg").write_text(source[84].get_svg_image(text_as_path=True), encoding="utf-8")
    # 編集元のPowerPointスライドも失わないよう、Word内の原本を保存する。
    word = ROOT / "JAC0177G-T1-04(260715修正).docx"
    with ZipFile(word) as archive:
        if not (ASSETS / "findall-slide.sldx").exists():
            (ASSETS / "findall-slide.sldx").write_bytes(archive.read("word/embeddings/Microsoft_PowerPoint_Slide24.sldx"))

    parsed = subprocess.run(["pandoc", str(HERE / "page85.md"), "--from=markdown-implicit_figures", "--preserve-tabs", "--to=json"], check=True, capture_output=True, encoding="utf-8")
    doc = json.loads(parsed.stdout)
    headings = [plain(b["c"][2]) for b in doc["blocks"] if b["t"] == "Header"]
    image = next(i["c"][2][0] for b in doc["blocks"] if b["t"] == "Para" for i in b["c"] if i["t"] == "Image")
    code = next(b["c"] for b in doc["blocks"] if b["t"] == "CodeBlock")
    filename = dict(code[0][2])["filename"]
    lines = code[1].split("\n")
    assert len(lines) == 15, "試作テンプレートは元教材の15行を対象とします"
    header = plain(doc["meta"]["header"]["c"])
    page_number = plain(doc["meta"]["page"]["c"])
    header_parts = header.split(" ", 3)
    section_number, section_title = headings[0].split(" ", 1)
    work_marker, work_method, work_title = headings[1].split(" ", 2)
    instructions = [
        *[f'#label({x}, 55.08, {quote(part)})' for x, part in zip([240.41, 252.89, 261.65, 276.53], header_parts)],
        '#panel(83.664, 60, 428.11, 0.48, fill: black)',
        f'#label(292.13, 797.04, {quote(page_number)}, font: "Times New Roman", size: 11.04)',
        f'#label(85.104, 100.22, {quote(section_number)}, size: 14.04, weight: "bold")',
        f'#label(122.3, 100.22, {quote(section_title)}, size: 14.04, weight: "bold")',
        f'#at(113.06, 114.62, image({quote(image)}, width: 369.2pt, height: 275.19pt))',
        '#panel(83.664, 414.79, 428.11, 0.72, fill: black)',
        *[f'#label({x}, 446.95, {quote(part)}, font: "MS PGothic", size: 12, stroke: 0.25pt)' for x, part in zip([85.104, 165.5, 199.61], [work_marker, work_method, work_title])],
        '#panel(79.704, 493.87, 435.196, 270.53, fill: white, stroke: 0.48pt)',
        '#panel(83.664, 495.31, 427.27, 268.85, fill: rgb(100%, 98.4%, 94.1%))',
        '#panel(309.1, 468.85, 202.85, 23.4, fill: white)',
        '#panel(306.6, 466.35, 207.85, 28.4, fill: red)',
        '#panel(309.6, 469.35, 201.85, 22.4, fill: white)',
        '#panel(310.6, 470.35, 199.85, 20.4, fill: red)',
        '#panel(311.6, 471.35, 197.85, 18.4, fill: white)',
        f'#label(325.63, 485.11, {quote(filename)}, font: "MS PGothic", size: 11.04, stroke: 0.23pt, tracking: 0.021pt)',
    ]
    token = re.compile(r'"[^"\n]*"|\b(?:public|private|class|return)\b')
    baselines = [507.43, 525.43, 543.43, 561.43, 579.46, 597.46, 615.46, 633.46, 651.46, 669.46, 687.46, 705.46, 723.46, 741.48, 759.48]
    for number, (line, baseline) in enumerate(zip(lines, baselines), 1):
        instructions.append(f'#label({103.104 - 6 * len(str(number) + ":")}, {baseline}, "{number}:", font: "MS Gothic", size: 12)')
        # Wordのタブ位置を維持。第1・第2タブは元PDFで測定した値。
        tabs = len(line) - len(line.lstrip("\t"))
        x = [103.1, 130.94, 176.66][tabs]
        line = line.lstrip("\t")
        cursor = 0
        for match in list(token.finditer(line)) + [None]:
            end = match.start() if match else len(line)
            chunk = line[cursor:end]
            if chunk:
                instructions.append(f'#label({x + cursor * 6}, {baseline}, {quote(chunk)}, font: "MS Gothic", size: 12)')
            if match:
                is_string = match.group().startswith('"')
                color = 'rgb("800040")' if is_string else "blue"
                instructions.append(f'#label({x + match.start() * 6}, {baseline}, {quote(match.group())}, font: "MS Gothic", size: 12, fill: {color})')
                cursor = match.end()
    # コード上の注釈矢印。スライド内の矢印とは別に編集できるようにする。
    instructions.extend([
        '#at(318.16, 599, polygon((0.98pt, 0pt), (11.9pt, 54.65pt), (10.92pt, 54.84pt), (0pt, 0.2pt), fill: red, stroke: none))',
        '#at(326.43, 652.18, polygon((5.89pt, 0pt), (4.12pt, 6.47pt), (0pt, 1.17pt), fill: red, stroke: none))',
    ])
    (HERE / "generated.typ").write_text((HERE / "layout.typ").read_text(encoding="utf-8") + "\n" + "\n".join(instructions), encoding="utf-8")
    typst.compile(str(HERE / "generated.typ"), output=str(OUT / "page85.pdf"), root=str(HERE), font_paths=["C:/Windows/Fonts"])
    prototype = fitz.open(OUT / "page85.pdf")
    assert len(prototype) == 1
    assert 'prodRepo.findAll()' in prototype[0].get_text(), "コードが検索可能な文字として生成されていません"
    scale = 2
    images = []
    for pdf, name in [(reference, "reference"), (prototype, "prototype")]:
        pix = pdf[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.save(OUT / f"{name}.png")
        images.append(image)
    original, result = images
    overlay = Image.blend(original, result, 0.5)
    overlay.save(OUT / "overlay.png")
    difference = ImageChops.difference(original, result)
    # 差がある場所を黒で示す。白地の割合を一致率として報告しない。
    mask = difference.convert("L").point(lambda v: 255 if v > 20 else 0)
    ImageChops.invert(mask).save(OUT / "difference.png")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    sheet = Image.new("RGB", (original.width * 2 + 24, original.height + 48), "#e5e5e5")
    sheet.paste(original, (0, 48))
    sheet.paste(result, (original.width + 24, 48))
    draw = ImageDraw.Draw(sheet)
    draw.text((20, 10), "元PDF 85ページ", font=font, fill="black")
    draw.text((original.width + 44, 10), "Markdownから生成した試作", font=font, fill="black")
    sheet.save(OUT / "comparison.png")
    comparison = fitz.open()
    p = comparison.new_page(width=595.32 * 2 + 20, height=841.92 + 28)
    p.insert_text((20, 18), "Original PDF / page 85", fontsize=11)
    p.insert_text((635.32, 18), "Markdown + Pandoc + Typst / prototype", fontsize=11)
    p.show_pdf_page(fitz.Rect(0, 28, 595.32, 869.92), reference, 0)
    p.show_pdf_page(fitz.Rect(615.32, 28, 1210.64, 869.92), prototype, 0)
    comparison.save(OUT / "comparison.pdf")
    regions = {"slide": (113.06, 114.62, 482.26, 389.81), "code": (79.46, 493.63, 515.14, 764.64), "heading": (83, 84, 300, 106)}
    metrics = {}
    for key, box in regions.items():
        pixel_box = tuple(round(n * scale) for n in box)
        region_diff = difference.crop(pixel_box)
        metrics[key] = {"mean_absolute_rgb_error_0_255": round(sum(ImageStat.Stat(region_diff).mean) / 3, 3)}
    positions = []
    for title, pdf in [("reference", reference), ("prototype", prototype)]:
        for line in ["@Controller", "prodRepo.findAll()", "ProductController"]:
            found = pdf[0].search_for(line)
            positions.append({"document": title, "text": line, "bounds_pt": [list(rect) for rect in found]})
    report = {"reference_sha256": hashlib.sha256(args.reference.read_bytes()).hexdigest(), "source_page": 85, "render_dpi": 144, "metrics": metrics, "positions": positions, "note": "スライドは元PDFからベクター抽出。本文・コードはMarkdownから組版。ページ座標は試作専用で固定。"}
    (OUT / "comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
