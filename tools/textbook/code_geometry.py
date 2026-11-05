"""既存decoration SVGと文字座標だけから、原本のコード枠を復元する。"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET


NUMBER = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"
FILE_LABEL = re.compile(r"^[\w./\\…:\-\s]+\.(?:java|html?|xml|properties|css|js|json|ya?ml|sql|txt)$", re.I)


def _union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)]


def _contains(outer, inner, tolerance=0):
    return (outer[0]-tolerance <= inner[0] and outer[1]-tolerance <= inner[1]
            and outer[2]+tolerance >= inner[2] and outer[3]+tolerance >= inner[3])


def _intersection(a, b):
    return max(0, min(a[2], b[2])-max(a[0], b[0])) * max(0, min(a[3], b[3])-max(a[1], b[1]))


def _contours(data):
    if re.search(r"[CcQqAaSsTtHhVv]", data):
        return []
    result = []
    for part in re.split(r"(?=M)", data):
        values = [float(v) for v in re.findall(NUMBER, part)]
        if len(values) < 8 or len(values) % 2:
            continue
        points = list(zip(values[::2], values[1::2]))
        if points[-1] == points[0]:
            points.pop()
        if len(points) != 4 or len({p[0] for p in points}) != 2 or len({p[1] for p in points}) != 2:
            continue
        if any(a[0] != b[0] and a[1] != b[1] for a, b in zip(points, points[1:]+points[:1])):
            continue
        area = sum(a[0]*b[1]-a[1]*b[0] for a, b in zip(points, points[1:]+points[:1]))
        result.append(([min(p[0] for p in points), min(p[1] for p in points),
                        max(p[0] for p in points), max(p[1] for p in points)], area))
    return result


def _shapes(path):
    result = []
    for index, node in enumerate(ET.parse(path).getroot().iter()):
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "rect":
            x, y = float(node.get("x", 0)), float(node.get("y", 0))
            contours = [([x, y, x+float(node.get("width", 0)), y+float(node.get("height", 0))], 1)]
        elif tag == "path":
            contours = _contours(node.get("d", ""))
        else:
            continue
        fill, stroke = node.get("fill", "none").lower(), node.get("stroke", "none").lower()
        width = float(node.get("stroke-width", 0))
        i = 0
        while i < len(contours):
            rect, direction = contours[i]
            # Wordの二重赤枠は、逆向きの矩形を重ねた塗りリングである。
            if (fill != "none" and i+1 < len(contours) and _contains(rect, contours[i+1][0])
                    and (direction*contours[i+1][1] < 0 or node.get("fill-rule") == "evenodd")):
                inner = contours[i+1][0]
                thicknesses = [inner[0]-rect[0], inner[1]-rect[1], rect[2]-inner[2], rect[3]-inner[3]]
                if min(thicknesses) > 0 and max(thicknesses)-min(thicknesses) < .03:
                    thickness = sum(thicknesses)/4
                    center = [rect[0]+thickness/2, rect[1]+thickness/2, rect[2]-thickness/2, rect[3]-thickness/2]
                    result.append({"rect": center, "fill": "none", "stroke": fill,
                                   "stroke_width": thickness, "_id": (index, i)})
                    i += 2
                    continue
            result.append({"rect": rect, "fill": fill, "stroke": stroke, "stroke_width": width, "_id": (index, i)})
            i += 1
    return result


def _backgrounds(shapes):
    bands = sorted({tuple(s["rect"]) for s in shapes if s["fill"] == "#fffbf0"
                    and s["rect"][2]-s["rect"][0] > 300}, key=lambda r: (r[1], r[0]))
    bands = [b for b in bands if not any(o != b and _contains(o, b) for o in bands)]
    frames = []
    for band in bands:
        if (frames and abs(frames[-1][0]-band[0]) < 2 and abs(frames[-1][2]-band[2]) < 2
                and band[1]-frames[-1][3] < 1):
            frames[-1] = _union([frames[-1], band])
        else:
            frames.append(list(band))
    return frames


def _outer_frame(background, shapes):
    black = [s for s in shapes if s["fill"] in ("#000000", "black") or s["stroke"] in ("#000000", "black")]
    rectangles = []
    for shape in black:
        r, width = shape["rect"], shape["stroke_width"]
        if shape["stroke"] in ("#000000", "black") and r[2]-r[0] > 300 and r[3]-r[1] > 2:
            actual = [r[0]-width/2, r[1]-width/2, r[2]+width/2, r[3]+width/2]
            if (_contains(actual, background, 1) and abs(actual[0]-background[0]) < 14
                    and abs(actual[2]-background[2]) < 14 and background[1]-actual[1] < 90
                    and actual[3]-background[3] < 5):
                rectangles.append((actual, {shape["_id"]}))
    vertical = [s for s in black if s["fill"] in ("#000000", "black")
                and s["rect"][2]-s["rect"][0] <= 2 and s["rect"][3]-s["rect"][1] > 5
                and s["rect"][1] <= background[1]+2 and s["rect"][3] >= background[3]-2]
    left = [s for s in vertical if background[0]-14 <= s["rect"][0] <= background[0]+1]
    right = [s for s in vertical if background[2]-1 <= s["rect"][2] <= background[2]+14]
    horizontal = [s for s in black if s["fill"] in ("#000000", "black")
                  and s["rect"][3]-s["rect"][1] <= 2 and s["rect"][2]-s["rect"][0] > 300]
    for a in left:
        for b in right:
            if abs(a["rect"][1]-b["rect"][1]) > 2 or abs(a["rect"][3]-b["rect"][3]) > 2:
                continue
            relevant = [s for s in horizontal if abs(s["rect"][0]-a["rect"][2]) < 3
                        and abs(s["rect"][2]-b["rect"][0]) < 3]
            top = [s for s in relevant if abs(s["rect"][3]-a["rect"][1]) < 2]
            bottom = [s for s in relevant if abs(s["rect"][1]-a["rect"][3]) < 2]
            if top and bottom:
                borders = [a, b, min(top, key=lambda s: abs(s["rect"][3]-a["rect"][1])),
                           min(bottom, key=lambda s: abs(s["rect"][1]-a["rect"][3]))]
                actual = _union([s["rect"] for s in borders])
                if _contains(actual, background, 1):
                    rectangles.append((actual, {s["_id"] for s in borders}))
    if rectangles:
        rect, members = min(rectangles, key=lambda item: (item[0][2]-item[0][0])*(item[0][3]-item[0][1]))
        return rect, members, True
    return list(background), set(), False


def _text_box(block):
    runs = [r for line in block["lines"] for r in line.get("runs", []) if r.get("bbox")]
    return _union([r["bbox"] for r in runs]) if runs else None


def _paint(shape):
    return {k: shape[k] for k in ("rect", "fill", "stroke", "stroke_width")}


def code_geometries(folder, layout, nodes):
    """code IDをキーに、原本ページ座標の枠・文字・付属要素を返す。"""
    folder = Path(folder)
    pages = {}
    for page in layout["pages"]:
        shapes = _shapes(folder/page["decoration"])
        pages[page["source_page"]] = (shapes, _backgrounds(shapes), page["entries"])
    result = {}
    border_members = {}
    for ident, node in nodes.items():
        if (node["kind"] != "code" or ident not in layout["blocks"]
                or layout["blocks"][ident]["role"] != "code"):
            continue
        block = layout["blocks"][ident]
        text_box = _text_box(block)
        if text_box is None:
            continue
        runs = [r for line in block["lines"] for r in line.get("runs", [])]
        shapes, backgrounds, order = pages[block["source_page"]]
        indices = sorted({line["code_frame"] for line in block["lines"] if line.get("code_frame") is not None})
        anchors = [[line["x"], line["y"]-5, line["x"], line["y"]-5]
                   for line in block["lines"] if line.get("runs")]
        # 図版内の背景はdecorationから除かれるため、元PDFのindexがずれる頁がある。
        selected = [backgrounds[i] for i in indices if i < len(backgrounds)
                    and any(_contains(backgrounds[i], point, 1) for point in anchors)]
        if not selected and indices:
            selected = [b for b in backgrounds if any(_contains(b, point, 1) for point in anchors)]
        background = _union(selected) if selected else list(text_box)
        frame, borders, framed = _outer_frame(background, shapes) if selected else (list(text_box), set(), False)
        result[ident] = {"source_page": block["source_page"], "frame": frame, "background": background,
                         "text_x": min(r["x"] for r in runs), "text_top": text_box[1], "text_bottom": text_box[3],
                         "framed": framed, "code_frame_indices": indices, "has_background": bool(selected),
                         "background_indices_used": [backgrounds.index(b) for b in selected],
                         "caption_ids": [], "figure_ids": [], "caption_shapes": [], "underlay_shapes": []}
        border_members[ident] = borders

    # 各付属要素は一つのコードへだけ所属させ、flowでの二重表示を防ぐ。
    captions, figures = {}, {}
    for ident, geometry in result.items():
        frame, page = geometry["frame"], geometry["source_page"]
        for member, block in layout["blocks"].items():
            if member not in nodes or block["source_page"] != page or nodes[member]["kind"] == "code":
                continue
            text = "\n".join(line["text"] for line in block["lines"]).strip()
            r = _text_box(block)
            if (r and FILE_LABEL.fullmatch(text) and r[3] >= frame[1]-36 and r[1] <= geometry["background"][1]+1
                    and r[1] <= geometry["text_top"] and r[2] > frame[0] and r[0] < frame[2]):
                score = abs(frame[1]-r[3])
                if member not in captions or score < captions[member][0]:
                    captions[member] = (score, ident)
        for figure in layout["figures"]:
            if figure["page"] != page:
                continue
            area = _intersection(frame, figure["box"])
            if area > 0 and (figure["id"] not in figures or area > figures[figure["id"]][0]):
                figures[figure["id"]] = (area, ident)
    for member, (_, owner) in captions.items():
        result[owner]["caption_ids"].append(member)
    for member, (_, owner) in figures.items():
        result[owner]["figure_ids"].append(member)
    for ident, geometry in result.items():
        shapes, _, order = pages[geometry["source_page"]]
        label_boxes = [_text_box(layout["blocks"][i]) for i in geometry["caption_ids"]]
        for member, block in layout["blocks"].items():
            if member not in nodes or nodes[member]["kind"] != "heading" or block["source_page"] != geometry["source_page"]:
                continue
            r = _text_box(block)
            if r and len("".join(line["text"] for line in block["lines"])) <= 100 and any(min(r[3], b[3])-max(r[1], b[1]) > 0 for b in label_boxes):
                geometry["caption_ids"].append(member)
        geometry["caption_ids"] = sorted(set(geometry["caption_ids"]), key=lambda i: order.index(i))
        caption_boxes = [_text_box(layout["blocks"][i]) for i in geometry["caption_ids"]]
        for shape in shapes:
            if shape["_id"] in border_members[ident] or shape["fill"] == "#fffbf0":
                continue
            r = shape["rect"]
            frame = geometry["frame"]
            if (shape["fill"] in ("#000000", "black") and _contains(frame, r, .03)
                    and (r[2]-r[0] <= 2 or r[3]-r[1] <= 2)
                    and (r[0] <= frame[0]+2 or r[2] >= frame[2]-2
                         or r[1] <= frame[1]+2 or r[3] >= frame[3]-2)):
                continue
            if any(_contains(r, b, 1) and r[3]-r[1] < 60 for b in caption_boxes):
                geometry["caption_shapes"].append(_paint(shape))
            elif _intersection(r, geometry["frame"]) > 0 and shape["fill"] != "#ffffff":
                geometry["underlay_shapes"].append(_paint(shape))
    return result
