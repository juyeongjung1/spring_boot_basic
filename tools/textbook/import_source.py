"""元PDFの本文をMarkdownへ移し、図版と再現用の位置情報を分離する。"""
from pathlib import Path
from zipfile import ZipFile
import argparse
import hashlib
import json
import re
from bisect import bisect_right

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def escape(text):
    text = re.sub(r"([\\`*{}\[\]<>#!_])", r"\\\1", text)
    text = re.sub(r"^(\d+)\.", r"\1\\.", text)
    text = re.sub(r"^ +", lambda m: "&#32;" * len(m[0]), text)
    text = re.sub(r" +$", lambda m: "&#32;" * len(m[0]), text)
    text = re.sub(r" {2,}", lambda m: "&#32;" * len(m[0]), text)
    return text


def color(value):
    if value is None:
        return "none"
    return "#" + "".join(f"{round(v * 255):02x}" for v in value)


def decorations(page, figures):
    paths = []
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        if any(fitz.Rect(f["box"]).contains(rect) for f in figures):
            continue
        parts = []
        last = None
        for item in drawing["items"]:
            kind = item[0]
            if kind == "re":
                r, direction = item[1:]
                points = [r.tl, r.tr, r.br, r.bl] if direction == 1 else [r.tl, r.bl, r.br, r.tr]
                parts.append("M" + " L".join(f"{p.x:g},{p.y:g}" for p in points) + "Z")
                last = None
            elif kind in ("l", "c"):
                start = item[1]
                if last != start:
                    parts.append(f"M{start.x:g},{start.y:g}")
                points = item[2:]
                parts.append(("L" if kind == "l" else "C") + " ".join(f"{p.x:g},{p.y:g}" for p in points))
                last = points[-1]
            elif kind == "qu":
                quad = item[1]
                parts.append("M" + " L".join(f"{p.x:g},{p.y:g}" for p in [quad.ul, quad.ur, quad.lr, quad.ll]) + "Z")
            else:
                raise ValueError(f"未対応の図形: {kind}")
        if drawing.get("closePath"):
            parts.append("Z")
        paths.append(f'<path d="{" ".join(parts)}" fill="{color(drawing.get("fill"))}" fill-opacity="{drawing.get("fill_opacity", 1) or 1}" stroke="{color(drawing.get("color"))}" stroke-width="{drawing.get("width") or 0}" fill-rule="{"evenodd" if drawing.get("even_odd") else "nonzero"}"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="595.32" height="841.92" viewBox="0 0 595.32 841.92">' + "".join(paths) + "</svg>\n"


def import_chapter(folder, force=False):
    config = json.loads((folder / "source.json").read_text(encoding="utf-8"))
    if (folder / "chapter.md").exists() and not force:
        raise ValueError("chapter.mdは既に存在します。編集内容を守るため、再取り込みには--forceが必要です。")
    assets = folder / "assets"
    assets.mkdir(exist_ok=True)
    source = ROOT / config["pdf"]
    pdf = fitz.open(source)
    styles = {}
    style_ids = {}
    layout = {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "styles": styles, "pages": [], "blocks": {}, "figures": [], "tables": {}}
    md = [f'<!-- 元PDF {config["first_page"]}〜{config["last_page"]}ページ。本文の改訂はまだ行っていません。 -->', ""]
    figure_count = 0

    def style(span, stroke):
        key = (span["font"], round(span["size"], 4), span["color"], span.get("flags", 0), round(stroke, 5))
        if key not in style_ids:
            ident = f"s{len(styles) + 1:03d}"
            style_ids[key] = ident
            styles[ident] = {"font": key[0], "size": key[1], "color": f"#{key[2]:06x}", "flags": key[3], "stroke": key[4]}
        return style_ids[key]

    for number in range(config["first_page"], config["last_page"] + 1):
        page = pdf[number - 1]
        # Wordが行ごとに分けたベージュの塗りを、元のコード枠へまとめる。
        code_frames=[]
        bands=sorted((d['rect'] for d in page.get_drawings() if d.get('fill') and all(abs(a-b)<0.003 for a,b in zip(d['fill'],(1,0.984,0.941))) and d['rect'].width>300),key=lambda r:(r.y0,r.x0))
        bands=[b for b in bands if not any(o!=b and o.contains(b) for o in bands)]
        for band in bands:
            if code_frames and abs(code_frames[-1].x0-band.x0)<2 and abs(code_frames[-1].x1-band.x1)<2 and band.y0-code_frames[-1].y1<1:
                code_frames[-1]|=band
            else:code_frames.append(fitz.Rect(band))
        strokes = {}
        for trace in page.get_texttrace():
            if trace["type"] == 1:
                for char in trace["chars"]:
                    strokes[(round(char[2][0], 2), round(char[2][1], 2), trace["font"])] = trace["linewidth"]
        figures = []
        tables = []
        for index, spec in enumerate([s for s in config.get('tables', []) if s['page'] == number], 1):
            table = dict(spec, id=f'p{number:03d}-table{index:02d}', role='table', source_page=number, runs=[])
            table['glyphs'] = [[[] for _ in spec['xs'][:-1]] for _ in spec['ys'][:-1]]
            tables.append(table)
        for spec in [s for s in config["figures"] if s["page"] == number]:
            figure_count += 1
            ident = f"p{number:03d}-f{figure_count:02d}"
            path = f"assets/{ident}.svg"
            x0, y0, x1, y1 = spec["box"]
            roi = fitz.Rect(x0 - 0.8, y0 - 0.8, x1 + 0.8, y1 + 0.8)
            cropped = fitz.open()
            cropped.insert_pdf(pdf, from_page=number - 1, to_page=number - 1)
            for box in spec.get('remove_text_boxes',[]):
                cropped[0].add_redact_annot(fitz.Rect(box),fill=False)
            if spec.get('remove_text_boxes'):
                cropped[0].apply_redactions(images=0,graphics=1 if spec.get('remove_contained_graphics') else 0,text=0)
            cropped[0].set_cropbox(roi)
            (folder / path).write_text(cropped[0].get_svg_image(text_as_path=True), encoding="utf-8", newline="\n")
            transcript = page.get_textbox(roi)
            figure = dict(spec, box=list(roi), id=ident, path=path, transcript=transcript)
            if spec.get("slide"):
                target = assets / f"{ident}.sldx"
                with ZipFile(ROOT / config["word"]) as word:
                    target.write_bytes(word.read("word/embeddings/" + spec["slide"]))
                figure["editable_source"] = target.relative_to(folder).as_posix()
            figures.append(figure)
            layout["figures"].append(figure)
        decoration = f"assets/p{number:03d}-decorations.svg"
        (folder / decoration).write_text(decorations(page, figures), encoding="utf-8", newline="\n")
        furniture = []
        lines = []
        covered = {"body": 0, "figure": 0, "furniture": 0, "table": 0}
        for block in page.get_text("rawdict")["blocks"]:
            for line in block.get("lines", []):
                spans = []
                for span in line["spans"]:
                    chars = span["chars"]
                    value = "".join(c["c"] for c in chars)
                    if not value.strip():
                        continue
                    bbox = fitz.Rect(span["bbox"])
                    center = (bbox.tl + bbox.br) / 2
                    tab = next((t for t in tables if fitz.Rect(t['box']).contains(center)), None)
                    first_is_cover = config.get('cover_mode', 'classic') != 'none'
                    category = "figure" if any(fitz.Rect(f["box"]).contains(center) for f in figures) else "table" if tab else "furniture" if ((number != config["first_page"] or not first_is_cover) and (bbox.y1 < 80 or bbox.y0 > 784)) else "body"
                    covered[category] += len(re.sub(r"\s", "", value))
                    if category == "figure":
                        continue
                    key = (round(chars[0]["origin"][0], 2), round(chars[0]["origin"][1], 2), span["font"])
                    record = {"text": value, "x": chars[0]["origin"][0], "y": chars[0]["origin"][1], "style": style(span, strokes.get(key, 0)), "bbox": list(bbox), "positions": [round(c["origin"][0], 4) for c in chars]}
                    if category == 'table':
                        tab['runs'].append(record)
                        for char in chars:
                            cb=fitz.Rect(char['bbox']); cx=(cb.x0+cb.x1)/2; cy=(cb.y0+cb.y1)/2
                            col=max(0,min(len(tab['xs'])-2,bisect_right(tab['xs'],cx)-1))
                            row=max(0,min(len(tab['ys'])-2,bisect_right(tab['ys'],cy)-1))
                            tab['glyphs'][row][col].append((char['origin'][1],char['origin'][0],char['c']))
                    elif category == "furniture":
                        furniture.append(record)
                    else:
                        spans.append(record)
                if spans:
                    lines.append({"runs": spans, "y": spans[0]["y"], "x": spans[0]["x"]})
        # PDFの描画順に依存せず、紙面の上から順に本文をまとめる。
        lines.sort(key=lambda l: (round(l["y"], 1), l["x"]))
        merged = []
        for line in lines:
            if merged and abs(merged[-1]["y"] - line["y"]) < 0.6:
                merged[-1]["runs"].extend(line["runs"])
                merged[-1]["runs"].sort(key=lambda r: r["x"])
            else:
                merged.append(line)
        groups = []
        overview='演習の目標' in page.get_text() or '予想所要時間' in page.get_text()
        overview_section=None
        for line in merged:
            mono = all("MS-Gothic" in styles[r["style"]]["font"] for r in line["runs"])
            frame=next((i for i,r in enumerate(code_frames) if r.contains(fitz.Point(line['x'],line['y']-5))),None)
            line['code_frame']=frame
            max_size = max(styles[r["style"]]["size"] for r in line["runs"])
            value = "".join(r["text"] for r in line["runs"]).strip()
            numbered = re.match(r"^\d+\.", value)
            bold = styles[line["runs"][0]["style"]]["stroke"] > 0
            caption = re.match(r"^[＜<].*[＞>]$|^【(?:参考|作業手順|補足|注意)", value)
            role = "code" if mono or frame is not None else "heading" if max_size >= 14 or caption or (max_size >= 12 and all("Gothic" in styles[r["style"]]["font"] for r in line["runs"])) or (numbered and bold) else "step" if numbered else "paragraph"
            if overview:
                if value in ('演習の目標','演習の概要','予想所要時間'):overview_section=value
                elif role=='heading':
                    if overview_section in ('演習の目標','演習の概要') or re.match(r'^演習\d+\.\d+.*分',value):role='paragraph'
                    else:overview_section=None
            continuation = groups and groups[-1]["role"] == "step" and role == "paragraph" and line["x"] > 100
            same_frame=groups and role=='code' and groups[-1]['role']=='code' and frame is not None and frame==groups[-1]['lines'][-1].get('code_frame')
            if groups and (role == groups[-1]["role"] or continuation) and role != "heading" and (same_frame or 0 < line["y"] - groups[-1]["lines"][-1]["y"] <= 19):
                groups[-1]["lines"].append(line)
            else:
                groups.append({"role": role, "lines": [line]})
        entries = []
        for index, group in enumerate(groups, 1):
            ident = f"p{number:03d}-b{index:02d}"
            group["id"] = ident
            group["source_page"] = number
            for line in group["lines"]:
                # 離れた番号と本文の間には編集可能な空白を補う。
                parts = []
                for i, run in enumerate(line["runs"]):
                    if i and not parts[-1]["text"].endswith(" ") and run["x"] - parts[-1]["bbox"][2] > 2:
                        parts[-1]["text"] += " "
                        parts[-1]["positions"].append(parts[-1]["bbox"][2])
                    parts.append(run)
                if parts:
                    parts[-1]["text"] = parts[-1]["text"].rstrip()
                line["text"] = "".join(r["text"] for r in parts)
            if group["role"] == "code":
                starts = [min(x for run in line["runs"] for c, x in zip(run["text"], run["positions"]) if not c.isspace()) for line in group["lines"]]
                base = min(starts)
                for line, start in zip(group["lines"], starts):
                    pitch = styles[line["runs"][0]["style"]]["size"] / 2
                    indent = max(0, round((start - base) / pitch))
                    line["text"] = " " * indent + line["text"].lstrip()
                spaced=[]
                for line in group['lines']:
                    if spaced and line.get('code_frame') is not None:
                        gap=round((line['y']-spaced[-1]['y'])/18)-1
                        for _ in range(max(0,gap)):
                            spaced.append({'text':'','runs':[],'y':spaced[-1]['y']+18,'x':base})
                    spaced.append(line)
                group['lines']=spaced
            layout["blocks"][ident] = group
            entries.append((group["lines"][0]["y"], "text", ident))
        for figure in figures:
            entries.append((figure.get('order_y',figure["box"][1]), "figure", figure["id"]))
        for table in tables:
            rows=[]
            for row in table.pop('glyphs'):
                cells=[]
                for glyphs in row:
                    lines=[];last=None
                    for y,x,c in sorted(glyphs,key=lambda g:(round(g[0],1),g[1])):
                        if last is None or abs(y-last)>2:lines.append('');last=y
                        lines[-1]+=c
                    cells.append('\n'.join(v.strip() for v in lines).strip())
                rows.append(cells)
            table['rows']=rows
            layout['tables'][table['id']]=table
            entries.append((table['box'][1],'table',table['id']))
        entries.sort()
        page_data = {"source_page": number, "decoration": decoration, "furniture": furniture, "entries": [entry[2] for entry in entries], "coverage": covered}
        layout["pages"].append(page_data)
        md += [f'::: {{#page-{number} .source-page}}', ""]
        for _, kind, ident in entries:
            if kind == "figure":
                fig = next(f for f in figures if f["id"] == ident)
                md += [f'![{fig["name"]}]({fig["path"]}){{#{ident}}}', ""]
                continue
            if kind == 'table':
                table=layout['tables'][ident]; rows=table['rows']; has_header=table.get('has_header',True)
                md += [f'::: {{#{ident} .table has-header="{str(has_header).lower()}"}}','']
                escaped=[[escape(c).replace('|','\\|').replace('\n','<br>') for c in row] for row in rows]
                header=escaped[0] if has_header else ['']*len(escaped[0])
                md += ['| '+' | '.join(header)+' |','| '+' | '.join(['---']*len(header))+' |']
                md += ['| '+' | '.join(row)+' |' for row in (escaped[1:] if has_header else escaped)]
                md += ['', ':::','']
                continue
            group = layout["blocks"][ident]
            md += [f'::: {{#{ident} .{group["role"]}}}', ""]
            if group["role"] == "code":
                code = "\n".join(l["text"] for l in group["lines"])
                language='xml' if re.match(r'\s*(?:\d+:)?\s*<',code) else 'css' if re.search(r'(?:color|margin|padding|font-size|background)\s*:',code) else 'java'
                md += ["```" + language, code, "```", ""]
            else:
                for i, line in enumerate(group["lines"]):
                    value = "".join(f'[{escape(r["text"])}]{{.{r["style"]}}}' for r in line["runs"] if r["text"])
                    md.append(value + ("\\" if i < len(group["lines"]) - 1 else ""))
                md.append("")
            md += ["::: ", ""]
        md += ["::: ", ""]
    (folder / "chapter.md").write_text("\n".join(line.rstrip() for line in md).rstrip() + "\n", encoding="utf-8", newline="\n")
    layout["markdown_sha256"] = hashlib.sha256((folder / "chapter.md").read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    write_json(folder / "source-layout.json", layout)
    print(json.dumps({"pages": len(layout["pages"]), "blocks": len(layout["blocks"]), "figures": len(layout["figures"]), "styles": len(styles)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", default="01")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    import_chapter(ROOT / "docs/textbook/chapters" / args.chapter, args.force)
