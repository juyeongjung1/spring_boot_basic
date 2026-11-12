"""章ごとの照合済みPDFを統合し、出典の全ページと連番を検証する。"""
from pathlib import Path
from collections import Counter
import json
import re

import pymupdf as fitz
from build import normalized,read_markdown
from book_index import ANCHOR_EDGES,append_index,collect_anchor_pages

ROOT=Path(__file__).resolve().parents[2]
MARKED=re.compile(rb'(/(?:Span|Artifact)\s*<<(.*?)>>\s*BDC)(.*?)(EMC)',re.S)
TEXT_OBJECT=re.compile(rb'\bBT\b.*?\bET\b',re.S)


def marked_key(match):
    number=re.search(rb'/MCID\s+(\d+)',match[2])
    if number:return ('mcid',int(number[1]))
    if re.search(rb'/Subtype\s*/Footer\b',match[2]):return ('footer',0)


def remove_number_text(page,rectangles,expected):
    """一時コピーで番号を特定し、元の描画命令を再解釈せず文字だけ除く。

    apply_redactionsを実ページへ適用するとTypstの線幅命令が消えるため、
    消えたMCID/フッターのテキストオブジェクトだけ元ストリームから除く。
    """
    doc=page.parent
    original_text=Counter(normalized(page.get_text()))
    def marked(p):
        return {marked_key(m):m[3] for m in MARKED.finditer(p.read_contents()) if marked_key(m) is not None}
    before=marked(page)
    temp=fitz.open();temp.insert_pdf(doc,from_page=page.number,to_page=page.number)
    for rect in rectangles:temp[0].add_redact_annot(rect,fill=(1,1,1))
    temp[0].apply_redactions(images=0,graphics=0,text=0)
    after=marked(temp[0])
    removed={key for key,body in before.items() if TEXT_OBJECT.search(body) and not TEXT_OBJECT.search(after.get(key,b''))}
    assert removed,'番号のテキスト要素を特定できません'
    changed=set()
    def replace(match):
        key=marked_key(match)
        if key not in removed:return match[0]
        changed.add(key)
        return match[1]+TEXT_OBJECT.sub(b'',match[3])+match[4]
    for xref in page.get_contents():
        raw=doc.xref_stream(xref);new=MARKED.sub(replace,raw)
        if new!=raw:doc.update_stream(xref,new)
    assert changed==removed
    page=doc.reload_page(page)
    remaining=Counter(normalized(page.get_text()))
    assert original_text-remaining==Counter(normalized(expected)) and not remaining-original_text,'番号以外の文字に変化があります'
    return page


def update_contents(original,flow,collection,page_map,heading_map):
    """目次の体裁を保ち、組版後の見出し位置へ番号とリンクを更新する。"""
    updates=[]
    for source_page in collection['toc_pages']:
        page=flow[page_map[source_page]-1]
        changes=[]
        for block in original[source_page-1].get_text('rawdict')['blocks']:
            for line in block.get('lines',[]):
                chars=[dict(c,size=s['size']) for s in line['spans'] for c in s['chars']]
                text=''.join(c['c'] for c in chars)
                match=re.search(r'^(.*?)\.{2,}\s*(\d+)\s*$',text)
                if not match:continue
                label=match[1].strip();old=int(match[2])
                key=normalized(label).rstrip('：:')
                target=heading_map.get((old,key),page_map[old])
                digits=chars[match.start(2):match.end(2)]
                rect=fitz.Rect(digits[0]['bbox'])
                for c in digits[1:]:rect|=fitz.Rect(c['bbox'])
                changes.append((label,old,target,rect,digits[0]['origin'][1],digits[0]['size'],line['bbox']))
        page=remove_number_text(page,[r+(-0.1,0,0.1,0) for _,_,_,r,_,_,_ in changes],''.join(str(c[1]) for c in changes))
        font=fitz.Font(fontfile='C:/Windows/Fonts/msgothic.ttc')
        page.insert_font(fontname='contents-number',fontbuffer=font.buffer)
        for label,old,target,rect,baseline,size,bbox in changes:
            value=str(target);width=font.text_length(value,fontsize=size)
            page.insert_text((rect.x1-width,baseline),value,fontname='contents-number',fontsize=size)
            page.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(bbox),'page':target-1})
            actual=page.get_textbox(rect+(-0.3,-3,0.3,3)).strip()
            assert actual==value,(label,target,actual)
            updates.append({'title':label,'source_page':old,'flow_page':target})
    assert updates,'目次項目がありません'
    return updates


def print_anchor(chapter, marks, reference):
    """印刷用に位置を指定した節の、章内ページ番号を求める。"""
    part, ident = reference.split(':', 1)
    if part != chapter:
        return None
    pages = [m['page'] for m in marks if m['id'] == ident and m['edge'] in ANCHOR_EDGES]
    if not pages:
        raise ValueError(f'印刷用の参照先がありません: {reference}')
    return min(pages)


def insert_blank(flow, before=None):
    position = -1 if before is None else before - 1
    rect = flow[position].rect
    return flow.new_page(pno=position, width=rect.width, height=rect.height).number + 1


def pad_before_odd_start(flow, blanks):
    if len(flow) % 2:
        blanks.append(insert_blank(flow))


def append_flow_part(flow, part, blanks, *, odd_start=False, introduction=None):
    if odd_start:
        pad_before_odd_start(flow, blanks)
    first = len(flow) + 1
    flow.insert_pdf(part)
    pages = list(range(first, len(flow) + 1))
    if introduction is not None and pages[introduction - 1] % 2 == 0:
        blanks.append(insert_blank(flow, before=pages[introduction - 1]))
        pages[introduction - 1:] = range(pages[introduction - 1] + 1, len(flow) + 1)
    return pages


def assemble(name, collection):
    out=ROOT/'output/pdf/textbook'/name
    out.mkdir(parents=True,exist_ok=True)
    reference=fitz.open();flow=fitz.open();comparison=fitz.open()
    original=fitz.open(ROOT/collection['pdf'])
    coverage=[];chapters=[];footer_pages=[];page_map={};heading_map={}
    anchor_pages={}
    print_layout=collection.get('print_layout')
    blanks=[]
    introduction_page=None
    colophon=fitz.open() if print_layout else None
    colophon_source=None
    for chapter in collection['parts']:
        folder=ROOT/'docs/textbook/chapters'/chapter
        config=json.loads((folder/'source.json').read_text(encoding='utf-8'))
        layout=json.loads((folder/'source-layout.json').read_text(encoding='utf-8'))
        generated=ROOT/'output/pdf/textbook'/f'chapter-{chapter}'
        checks=json.loads((generated/'checks.json').read_text(encoding='utf-8'))
        expected=list(range(config['first_page'],config['last_page']+1))
        assert [p['source_page'] for p in checks['reference']['page_checks']]==expected,chapter
        assert all(p['native_text_complete'] for p in checks['reference']['page_checks']),chapter
        assert checks['flow']['native_text_complete'],chapter
        for key in ['heading_orphans','split_figures','split_short_code','split_short_tables','split_instructions','overflow']:
            assert not checks['flow'].get(key), (chapter,key)
        part_ref=fitz.open(generated/'chapter-reference.pdf')
        part_flow=fitz.open(generated/'chapter-flow.pdf')
        part_comparison=fitz.open(generated/'comparison.pdf')
        assert len(part_ref)==len(expected)==len(part_comparison),chapter
        coverage+=expected
        ref_start=len(reference)+1
        reference.insert_pdf(part_ref);comparison.insert_pdf(part_comparison)
        marks=checks['flow']['block_positions']
        intro_local=print_anchor(chapter,marks,print_layout['introduction']) if print_layout else None
        colophon_local=print_anchor(chapter,marks,print_layout['colophon']) if print_layout else None
        if colophon_local is not None:
            assert chapter==collection['parts'][-1] and colophon_local==len(part_flow)>1, '奥付は最後の原稿ページに置いてください'
            colophon_source=expected[-1]
            colophon.insert_pdf(part_flow,from_page=colophon_local-1,to_page=colophon_local-1)
            part_flow.delete_page(colophon_local-1)
            marks=[mark for mark in marks if mark['page']<colophon_local]
        part_pages=append_flow_part(flow,part_flow,blanks,odd_start=bool(print_layout),introduction=intro_local)
        flow_start=part_pages[0]
        if intro_local is not None:
            introduction_page=part_pages[intro_local-1]
        if collection.get('index'):
            collect_anchor_pages(chapter,marks,part_pages,anchor_pages)
        nodes,_,_=read_markdown(folder/'chapter.md')
        local_positions={}
        for mark in marks:
            match=re.match(r'p(\d+)-',mark['id']) or re.match(r'__native-page-(\d+)',mark['id'])
            if match:
                p=int(match[1]);actual=part_pages[mark['page']-1]
                local_positions[p]=min(local_positions.get(p,actual),actual)
                if mark['id'] in nodes and mark['edge'] in ('start','heading'):
                    key=normalized(nodes[mark['id']]['text']).rstrip('：:')
                    heading_map.setdefault((p,key),actual)
        if config.get('cover_mode','classic')!='none':local_positions[expected[0]]=flow_start
        for p in reversed(expected):
            page_map[p]=local_positions.get(p,page_map.get(p+1,len(flow)))
        # 全体版では各章の元ページ開始番号を残さず、物理ページに連番を付ける。
        for i,n in enumerate(part_pages):
            if i==0 and config.get('cover_mode','classic')!='none':continue
            fixed=next((m for m in marks if m['edge']=='native-page' and m['page']==i+1),None)
            if fixed:
                source_number=int(fixed['id'].rsplit('-',1)[1])
                source_info=next(p for p in layout['pages'] if p['source_page']==source_number)
                if not any(r['text'].strip().isdigit() and r['bbox'][1]>784 for r in source_info['furniture']):continue
            footer_pages.append(n)
        chapters.append({'chapter':chapter,'title':config['title'],'source_pages':[expected[0],expected[-1]],'reference_pages':[ref_start,len(reference)],'flow_pages':[flow_start,len(flow)],'blocks':checks['blocks'],'figures':checks['figures'],'table_count':len(layout.get('tables',{}))})
    assert coverage==list(range(1,len(original)+1)),f'{name}: 出典ページの欠落または重複'
    bookmarks=[[1,c['title'],c['flow_pages'][0]] for c in chapters]
    index=None
    if collection.get('index'):
        if print_layout:
            pad_before_odd_start(flow,blanks)
        index=append_index(flow,ROOT/collection['index'],anchor_pages)
        bookmarks.append([1,'索引',index['pages'][0]])
    if print_layout:
        assert introduction_page and introduction_page%2==1 and len(colophon)==1, 'はじめに、または奥付の配置を確認してください'
        # 奥付が最終の偶数ページになるよう、必要な空白はその手前に入れる。
        if len(flow)%2==0:
            blanks.append(insert_blank(flow))
        flow.insert_pdf(colophon)
        page_map[colophon_source]=len(flow)
    contents=update_contents(original,flow,collection,page_map,heading_map)
    for n in footer_pages:
        page=flow[n-1]
        footer=fitz.Rect(240,786,355,817)
        old=page.get_textbox(footer).strip()
        assert old.isdigit(),(n,old)
        page=remove_number_text(page,[footer],old)
        font=page.insert_font(fontname='book-footer',fontfile='C:/Windows/Fonts/times.ttf')
        width=fitz.get_text_length(str(n),fontname='tiro',fontsize=11.04)
        page.insert_text((297.66-width/2,797.04),str(n),fontname='book-footer',fontsize=11.04)
        value=page.get_textbox(fitz.Rect(240,786,355,817)).strip()
        assert value==str(n),(n,value)
    reference.set_metadata({'title':collection['title']+' 元位置再現版'})
    flow.set_metadata({'title':collection['title']+' 自動組版版'})
    comparison.set_metadata({'title':collection['title']+' 元PDFとの比較'})
    flow.set_toc(bookmarks)
    flow.subset_fonts()
    reference.save(out/'reference.pdf',garbage=4,deflate=True)
    flow.save(out/'flow.pdf',garbage=4,deflate=True)
    comparison.save(out/'comparison.pdf',garbage=4,deflate=True)
    report={'title':collection['title'],'source_pages':len(original),'reference_pages':len(reference),'flow_pages':len(flow),'comparison_pages':len(comparison),'complete_source_coverage':True,'continuous_footer_numbers':True,'contents':contents,'chapters':chapters}
    if index:
        report['index']=index
    if print_layout:
        report['print_layout']={'introduction_page':introduction_page,'blank_pages':blanks,'colophon_page':len(flow)}
    (out/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('chapters','index')},ensure_ascii=False))
    return report


if __name__=='__main__':
    collections=json.loads((ROOT/'docs/textbook/collections.json').read_text(encoding='utf-8'))
    for name,collection in collections.items():assemble(name,collection)
