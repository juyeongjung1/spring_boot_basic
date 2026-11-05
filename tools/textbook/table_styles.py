"""保存済みSVG/座標から、表セルの背景・元文字書式を復元する。"""
from bisect import bisect_right
from collections import Counter
from functools import lru_cache
from pathlib import Path
import re
from statistics import median
import xml.etree.ElementTree as ET

import pymupdf as fitz


@lru_cache(maxsize=128)
def _decoration_fills(svg_path):
    """import_sourceが原本座標で保存した塗り矩形を、SVG描画順で読む。"""
    fills = []
    for element in ET.parse(svg_path).getroot():
        color = element.get("fill", "none")
        if color == "none" or float(element.get("fill-opacity", "1")) == 0:
            continue
        path = element.get("d", "")
        if re.search(r"[A-KN-Yac-z]", path):
            continue
        coordinates = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", path)]
        if len(coordinates) != 8:
            continue
        points = list(zip(coordinates[::2], coordinates[1::2]))
        xs, ys = set(coordinates[::2]), set(coordinates[1::2])
        if len(xs) == len(ys) == 2 and set(points) == {(x, y) for x in xs for y in ys}:
            fills.append((fitz.Rect(min(xs), min(ys), max(xs), max(ys)), color.lower()))
    return fills


def _source_cells(table):
    xs, ys = table["xs"], table["ys"]
    cells = [[[] for _ in xs[1:]] for _ in ys[1:]]
    for run in table["runs"]:
        center_y = (run["bbox"][1] + run["bbox"][3]) / 2
        row = bisect_right(ys, center_y) - 1
        if len(run["text"]) != len(run["positions"]):
            raise ValueError(f"表の文字座標数が一致しません: {table['id']}")
        for character, x in zip(run["text"], run["positions"]):
            column = bisect_right(xs, x + .02) - 1
            if 0 <= row < len(cells) and 0 <= column < len(cells[0]):
                cells[row][column].append((run["y"], x, character, run["style"]))
    for row in cells:
        for index, cell in enumerate(row):
            lines = []
            for character in sorted(cell):
                if not lines or abs(character[0] - lines[-1][0][0]) > 2:
                    lines.append([character])
                else:
                    lines[-1].append(character)
            row[index] = [character for line in lines for character in sorted(line, key=lambda value: value[1])]
    return cells


def table_geometry(layout, table):
    """元セル内の文字位置から揃え方、最小行高、代表行送りを取得する。"""
    xs, ys = table["xs"], table["ys"]
    source = _source_cells(table)
    bounds = [[None for _ in xs[1:]] for _ in ys[1:]]
    for run in table["runs"]:
        row = bisect_right(ys, (run["bbox"][1] + run["bbox"][3]) / 2) - 1
        for index, (character, x) in enumerate(zip(run["text"], run["positions"])):
            column = bisect_right(xs, x + .02) - 1
            if not character.strip() or character == "\u200b" or not (0 <= row < len(bounds) and 0 <= column < len(bounds[0])):
                continue
            right = run["positions"][index + 1] if index + 1 < len(run["positions"]) else run["bbox"][2]
            box = fitz.Rect(x, run["bbox"][1], right, run["bbox"][3])
            bounds[row][column] = box if bounds[row][column] is None else bounds[row][column] | box
    cells, pitches, insets, sizes = [], [], [], Counter()
    for row, source_row in enumerate(source):
        cell_row = []
        for column, characters in enumerate(source_row):
            box = bounds[row][column]
            align, valign = "left", "top"
            if box is not None:
                left, right = box.x0 - xs[column], xs[column + 1] - box.x1
                top, bottom = box.y0 - ys[row], ys[row + 1] - box.y1
                centered = abs(left - right) <= max(2, (xs[column + 1] - xs[column]) * .03)
                if centered and (min(left, right) > 4 or row == 0 and table.get("has_header")):
                    align = "center"
                elif right <= 4 and left > right + 4:
                    align = "right"
                if abs(top - bottom) <= max(2.5, (ys[row + 1] - ys[row]) * .04):
                    valign = "horizon"
                elif bottom <= 4 and top > bottom + 4:
                    valign = "bottom"
                if align == "left":
                    insets.append(max(0, left))
            baselines = []
            for baseline, _, character, style in characters:
                if character.strip() and character != "\u200b":
                    sizes[layout["styles"][style]["size"]] += 1
                    if not baselines or baseline - baselines[-1] > 2:
                        baselines.append(baseline)
            pitches += [round((b - a) * 4) / 4 for a, b in zip(baselines, baselines[1:])]
            cell_row.append({"align": align, "valign": valign})
        cells.append(cell_row)
    return {"cells": cells, "row_heights": [b - a for a, b in zip(ys, ys[1:])],
            "pitch": Counter(pitches).most_common(1)[0][0] if pitches else None,
            "font_size": sizes.most_common(1)[0][0] if sizes else None,
            "inset": median(insets) if insets else None}


def table_paint(folder, layout, table, rows):
    """`fill` と `parts: [(文字列, 元style ID, 下線), ...]` のセル行列を返す。

    partsは既存Typstのstyled(style, body)へ渡せる。原文一致セルは文字単位の
    書式を保持し、編集セルは背景と元セル先頭の基本書式で描画する。
    """
    source = _source_cells(table)
    geometry = table_geometry(layout, table)
    page = next(page for page in layout["pages"] if page["source_page"] == table["source_page"])
    fills = _decoration_fills(str((Path(folder) / page["decoration"]).resolve()))
    result = []
    for row_index, text_row in enumerate(rows):
        output_row = []
        source_row = min(row_index, len(source) - 1)
        for column, text in enumerate(text_row):
            source_column = min(column, len(source[source_row]) - 1)
            characters = source[source_row][source_column]
            rectangle = fitz.Rect(table["xs"][source_column], table["ys"][source_row], table["xs"][source_column + 1], table["ys"][source_row + 1])
            fill = "#ffffff"
            for painted, color in fills:
                if painted.contains((rectangle.tl + rectangle.br) / 2) and (painted & rectangle).get_area() >= rectangle.get_area() * .8:
                    fill = color
            meaningful = [character for character in characters if character[2].strip() and character[2] != "\u200b"]
            original_text = "".join(character[2] for character in meaningful)
            default_style = meaningful[0][3] if meaningful else next(iter(layout["styles"]))
            cell = {"fill": fill, **geometry["cells"][source_row][source_column]}
            if re.sub(r"\s+|\u200b", "", text) != original_text:
                output_row.append({**cell, "parts": [[text, default_style, False]]})
                continue
            parts, offset = [], 0
            previous = (default_style, False)
            for character in text:
                if character.strip() and character != "\u200b":
                    baseline, x, _, style = meaningful[offset]
                    offset += 1
                    color = layout["styles"][style]["color"].lower()
                    underline = any(
                        painted.height <= 1.5 and painted.width > 2 and painted.x0 - .3 <= x <= painted.x1 + .3
                        and .1 <= (painted.y0 + painted.y1) / 2 - baseline <= 3
                        and all(abs((painted.y0 + painted.y1) / 2 - y) > 1.2 for y in table["ys"])
                        and paint_color == color for painted, paint_color in fills
                    )
                    previous = (style, underline)
                style, underline = previous
                if parts and parts[-1][1:] == [style, underline]:
                    parts[-1][0] += character
                else:
                    parts.append([character, style, underline])
            output_row.append({**cell, "parts": parts})
        result.append(output_row)
    return result
