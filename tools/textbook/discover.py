"""図版枠、操作画面、罫線表を検出して章設定へ記録する。検出後は画像で確認する。"""
from pathlib import Path
import argparse
import json
import math
from zipfile import ZipFile
from io import BytesIO
import xml.etree.ElementTree as ET

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]


def merge_values(values, tolerance=2.6):
    groups = []
    for value in sorted(values):
        if groups and value - groups[-1][-1] <= tolerance:
            groups[-1].append(value)
        else:
            groups.append([value])
    return [sum(g) / len(g) for g in groups]


def near(a, b, gap=3):
    a = fitz.Rect(a)
    a = fitz.Rect(a.x0-gap, a.y0-gap, a.x1+gap, a.y1+gap)
    return a.intersects(fitz.Rect(b))


def components(rectangles, gap=3):
    groups = []
    for rect in rectangles:
        current = fitz.Rect(rect)
        changed = True
        while changed:
            changed = False
            for i, other in enumerate(groups):
                if near(current, other, gap):
                    current |= other
                    groups.pop(i)
                    changed = True
                    break
        groups.append(current)
    return groups


def slide_boxes(page):
    images = page.get_image_info()
    logos = [fitz.Rect(i['bbox']) for i in images if 12 < i['bbox'][2]-i['bbox'][0] < 22 and 12 < i['bbox'][3]-i['bbox'][1] < 22 and i['bbox'][0] > 350]
    lines = [d['rect'] for d in page.get_drawings() if 300 < d['rect'].width < 400 and d['rect'].height < 2 and 90 < d['rect'].x0 < 140]
    result = []
    for logo in logos:
        top = [r for r in lines if logo.y0-25 < r.y0 < logo.y0 and r.x1 > logo.x1]
        if not top:
            continue
        t = max(top, key=lambda r:r.y0)
        bottoms = [r for r in lines if 230 < r.y0-t.y0 < 300 and abs(r.x0-t.x0)<2]
        if bottoms:
            b = min(bottoms,key=lambda r:abs(r.y0-t.y0-275))
            result.append(fitz.Rect(t.x0,t.y0,b.x1,b.y1))
    return result


def table_boxes(page, excluded):
    edges = []
    for d in page.get_drawings():
        r = d['rect']
        if any(fitz.Rect(e).contains(r) for e in excluded):
            continue
        if r.y0 < 80 or r.y1 > 783:
            continue
        if (r.width < 2 and r.height > 12) or (r.height < 2 and r.width > 20):
            edges.append(r)
        for item in d['items']:
            if item[0]=='re' and d.get('fill') is None:
                box=item[1]
                if box.width>20 and box.height>12:
                    edges.extend([fitz.Rect(box.x0,box.y0,box.x1,box.y0+.1),fitz.Rect(box.x0,box.y1-.1,box.x1,box.y1),fitz.Rect(box.x0,box.y0,box.x0+.1,box.y1),fitz.Rect(box.x1-.1,box.y0,box.x1,box.y1)])
    result=[]
    for box in components(edges,2.5):
        local=[r for r in edges if box.contains(r)]
        xs=merge_values([r.x0+r.width/2 for r in local if r.width<2])
        ys=merge_values([r.y0+r.height/2 for r in local if r.height<2])
        if len(xs)>=3 and len(ys)>=3 and box.width>90 and box.height>25:
            result.append({'box':list(box),'xs':xs,'ys':ys,'has_header':True})
    return result


def detect_page(page):
    slides=slide_boxes(page)
    pictures=[]
    for image in page.get_image_info():
        r=fitz.Rect(image['bbox'])
        if r.width<8 or r.height<8 or any(s.contains((r.tl+r.br)/2) for s in slides):
            continue
        if r.y1>80 and r.y0<783:
            pictures.append(r)
    pics=components(pictures,5)
    # 画面と接している注釈線・吹き出しも含める。本文を含む大きな背景は除く。
    for _ in range(3):
        for pic in pics:
            for d in page.get_drawings():
                r=d['rect']
                if r.y0<80 or r.y1>783 or r.get_area()>120000 or r.width>480 or r.height>400:
                    continue
                if near(pic,r,1) and r.get_area()>2 and r.height>2:
                    pic |= r
    pics=components(pics,2)
    figures=[{'name':'スライド','box':list(r),'slide_candidate':True} for r in slides]
    figures += [{'name':'操作画面・図解','box':list(r)} for r in pics if not any(s.contains(r) for s in slides)]
    tables=table_boxes(page,[f['box'] for f in figures])
    return figures,tables


def slide_sources(word):
    a='{http://schemas.openxmlformats.org/drawingml/2006/main}t'
    result=[]
    with ZipFile(word) as z:
        for name in z.namelist():
            if name.startswith('word/embeddings/') and name.endswith('.sldx'):
                with ZipFile(BytesIO(z.read(name))) as slide:
                    text=''.join(n.text or '' for f in slide.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml') for n in ET.fromstring(slide.read(f)).iter(a))
                result.append((Path(name).name,text))
    return result


def discover(folder):
    config=json.loads((folder/'source.json').read_text(encoding='utf-8'))
    pdf=fitz.open(ROOT/config['pdf'])
    sources=slide_sources(ROOT/config['word'])
    figures=[];tables=[]
    for n in range(config['first_page'],config['last_page']+1):
        fs,ts=detect_page(pdf[n-1])
        for fig in fs:
            fig['page']=n
            if fig.pop('slide_candidate',False):
                text=''.join(pdf[n-1].get_textbox(fitz.Rect(fig['box'])).split())
                scored=sorted([(sum(1 for c in set(s) if c in text)/max(1,len(set(s))),name) for name,s in sources],reverse=True)
                if scored and scored[0][0]>.65:fig['slide']=scored[0][1]
            figures.append(fig)
        for table in ts:table['page']=n;tables.append(table)
    config['figures']=figures;config['tables']=tables
    (folder/'source.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(folder.name,'図版',len(figures),'表',len(tables))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--chapter',required=True);args=p.parse_args()
    discover(ROOT/'docs/textbook/chapters'/args.chapter)
