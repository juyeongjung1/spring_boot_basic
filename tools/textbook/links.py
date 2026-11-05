"""表示中のURLへリンクを付ける。折り返したURLは各行から同じ宛先へ飛ばす。"""
import re

import pymupdf as fitz


URL = re.compile(r'https?://[A-Za-z0-9:/?#@!$&()*+,;=._~%+\-\[\]]+')


def visible_urls(nodes):
    urls = set()
    for node in nodes.values():
        text = node['text'] if node['kind'] == 'code' else ''.join(v for v, _ in node['parts'] if v != '\n')
        for match in URL.finditer(text):
            value = match[0].rstrip('.,;:!')
            while value and ((value.endswith(')') and value.count(')') > value.count('('))
                             or (value.endswith(']') and value.count(']') > value.count('['))):
                value = value[:-1]
            if value:
                urls.add(value)
    return sorted(urls, key=len, reverse=True)


def add_url_links(pdf, nodes):
    targets = visible_urls(nodes)
    annotations = []
    for number, page in enumerate(pdf):
        chars = []
        for block in page.get_text('rawdict')['blocks']:
            for line_number, line in enumerate(block.get('lines', [])):
                row = (block['number'], line_number)
                for span in line['spans']:
                    chars.extend((c['c'], fitz.Rect(c['bbox']), row) for c in span['chars']
                                 if not c['c'].isspace() and c['c'] != '\u200b')
        text = ''.join(c for c, _, _ in chars)
        occupied = set()
        existing = page.get_links()
        for target in targets:
            start = text.find(target)
            while start >= 0:
                end = start + len(target)
                if not occupied.intersection(range(start, end)):
                    boxes = {}
                    for _, rect, row in chars[start:end]:
                        boxes[row] = boxes[row] | rect if row in boxes else rect
                    for rect in boxes.values():
                        duplicate = any(link.get('uri') == target and (fitz.Rect(link['from']) & rect).get_area() >= rect.get_area() * .9
                                        for link in existing)
                        if not duplicate:
                            page.insert_link({'kind': fitz.LINK_URI, 'from': rect, 'uri': target})
                        annotations.append({'page': number + 1, 'uri': target, 'rect': list(rect)})
                    occupied.update(range(start, end))
                start = text.find(target, end)
    return annotations
