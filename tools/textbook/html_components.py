"""Markdownのコード・表・構文解説をHTML/CSSから文字付きPDF部品へ変換する。"""
from collections import Counter, defaultdict
from hashlib import sha256
from html import escape
from pathlib import Path
import json
import os
import re
import subprocess
import textwrap
from urllib.parse import unquote

import pymupdf as fitz
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

from code_geometry import FILE_LABEL, code_geometries
from figure_numbers import figure_numbers
from table_styles import table_paint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = Path('C:/Users/jungj/.cache/codex-runtimes/codex-primary-runtime/dependencies')
SYMBOLS = str.maketrans({'◼': '■', '⚫': '●', '\uf09f': '•'})
LABELS = {'java': 'Java', 'html': 'HTML', 'xml': 'XML', 'css': 'CSS',
          'properties': 'Properties', 'sql': 'SQL', 'text': 'コンソール'}


def normalized(value):
    return re.sub(r'\s+|\u200b', '', value.translate(SYMBOLS))


def ids_attr(ids):
    return ' data-source-ids="' + escape(','.join(ids), quote=True) + '"' if ids else ''


def language(node, filename=''):
    name = filename.lower()
    for suffix, lang in (('.java', 'java'), ('.html', 'html'), ('.jsp', 'html'),
                         ('.xml', 'xml'), ('.css', 'css'), ('.properties', 'properties'), ('.sql', 'sql')):
        if name.endswith(suffix):
            return lang
    text = re.sub(r'^\s*\d+:', '', node['text'], flags=re.M).lstrip()
    if text.startswith(('spring.', '# MySQL', 'jakarta.validation.')):
        return 'properties'
    if re.match(r'<(?:\?xml|project|dependencies|dependency)\b', text):
        return 'xml'
    if text.startswith(('<', '<!')):
        return 'html'
    if text.startswith(('org.springframework.', 'java.lang.', 'Caused by:', 'Error ', 'Exception ')):
        return 'text'
    return node.get('language') if node.get('language') in LABELS else 'text'


def canonical(value):
    # Word由来の引用符を、コピーして使えるコードの引用符へ揃える。
    return value.translate(str.maketrans({'“': '"', '”': '"', '‘': "'", '’': "'"}))


def highlighted(value, lang, soft_breaks=False):
    output = []
    # JavaLexerは行末コメントの終端に改行を必要とする。補った1字だけ最後に除く。
    for token, text in lex(value+'\n', get_lexer_by_name(lang, stripnl=False, ensurenl=False)):
        kind = next((name for family, name in ((Token.Comment, 'comment'), (Token.Name.Decorator, 'annotation'), (Token.Keyword, 'keyword'),
            (Token.Literal.String, 'string'), (Token.Literal.Number, 'number'), (Token.Name.Class, 'type'),
            (Token.Name.Function, 'function'), (Token.Operator, 'operator'), (Token.Punctuation, 'punctuation'))
            if token in family), '')
        if lang == 'html' and token in Token.Name.Tag:
            kind = 'element'
        elif lang == 'html' and token in Token.Name.Attribute and text.startswith('th:'):
            kind = 'thymeleaf'
        fragments = text.split('\n')
        for i, fragment in enumerate(fragments):
            if fragment:
                safe = escape(fragment)
                if soft_breaks and token in Token.Punctuation:
                    safe = re.sub(r'([.,(])', r'\1<wbr>', safe)
                output.append(f'<span class="{kind}">{safe}</span>' if kind else safe)
            if i < len(fragments)-1:
                output.append('\n')
    return ''.join(output).removesuffix('\n')


def header(label, filenames=()):
    names = ''.join('<span class="file-item"' + ids_attr(ids) + '>' + escape(text) + '</span>'
                    for text, ids in filenames)
    return (f'<header class="card-header"><span class="language-badge">{escape(label)}</span>'
            f'<span class="filename">{names}</span><span class="continuation"></span></header>')


def source_rows(node, owner, start=1):
    lines = canonical(node['text']).split('\n')
    numbered = any(re.match(r'^\s*\d+:', line) for line in lines)
    rows = []
    for line in lines:
        match = re.match(r'^\s*(\d+):(.*)$', line)
        if match:
            rows.append({'number': int(match[1]), 'code': match[2], 'ids': [owner]})
        elif numbered and rows:
            rows[-1]['code'] += '\n' + line
        else:
            rows.append({'number': start+len(rows), 'code': line, 'ids': [owner]})
    return rows


def code_html(rows, lang, filenames, footer=''):
    source = '\n'.join(row['code'] for row in rows)
    tokens = highlighted(source, lang).split('\n')
    cursor, pieces = 0, []
    for row in rows:
        count = row['code'].count('\n')+1
        content = '\n'.join(tokens[cursor:cursor+count])
        cursor += count
        pieces.append('<div class="code-row" data-break-row' + ids_attr(row['ids']) + '>'
            + f'<div class="line-number">{row["number"]}</div><pre class="source-code" spellcheck="false">{content}</pre></div>')
    return '<section class="card code-card">'+header(LABELS[lang], filenames)+'<div class="card-content">'+''.join(pieces)+'</div><footer class="card-footer">'+footer+'</footer></section>'


def table_column_alignments(node):
    """元Wordの単一セルのずれを引き継がず、列の値の種類で整列する。"""
    body = node['rows'][1:] if node['has_header'] else node['rows']
    alignments = []
    for column in range(len(node['rows'][0])):
        values = [row[column].strip() for row in body if row[column].strip() not in {'', '-', '－'}]
        numeric = values and all(re.fullmatch(r'[+-]?\d[\d,.]*(?:\s*%)?', value) for value in values)
        alignments.append('right' if numeric else 'left')
    return alignments


def table_cell_html(parts, layout, header_cell, preserve_breaks):
    raw = ''.join(text for text, _, _ in parts)
    cursor, output = 0, []
    for text, style_id, underline in parts:
        safe = []
        for index, character in enumerate(text):
            if character != '\n':
                safe.append(escape(character.translate(SYMBOLS)))
            elif preserve_breaks:
                safe.append('<br>')
            else:
                position = cursor+index
                before = raw[position-1] if position else ''
                after = raw[position+1] if position+1 < len(raw) else ''
                if before and after and before.isascii() and after.isascii() and before.isalnum() and after.isalnum():
                    safe.append(' ')
        cursor += len(text)
        body = ''.join(safe)
        if style_id:
            style = layout['styles'][style_id]
            weight = 700 if header_cell or style.get('stroke', 0) or 'Bold' in style['font'] or style.get('flags',0)&16 else 400
            body = f'<span class="source-style" style="color:{style["color"]};font-weight:{weight};text-decoration:{"underline" if underline else "none"}">{body}</span>'
        output.append(body)
    return ''.join(output)


def table_html(folder, layout, ident, node):
    info = layout.get('tables', {}).get(ident)
    paint = table_paint(folder, layout, info, node['rows']) if info else None
    headings = [re.sub(r'\s+', '', value) for value in node['rows'][0]] if node['has_header'] else []
    comparison = headings == ['要素', 'JDBC', 'SpringDataJPA']
    property_table = node['has_header'] and len(node['rows']) > 1 and len(node['rows'][0]) == 2 and all(row[0].strip().startswith('spring.') for row in node['rows'][1:])
    alignments = table_column_alignments(node)
    rows = []
    for i, row in enumerate(node['rows']):
        cells = []
        header_cell = i == 0 and node['has_header']
        for j, value in enumerate(row):
            tag = 'th' if header_cell else 'td'
            cell = paint[i][j] if paint else None
            parts = cell['parts'] if cell else [(value, None, False)]
            # 制約の併記や入力エラーの複数メッセージは行の対応を保つ。
            preserve = not header_cell and (headings and (headings[j] == '制約' or '出力メッセージ' in headings))
            body = table_cell_html(parts, layout, header_cell, preserve)
            if comparison and j:
                for term in ('mysql-connector-j.jar', 'application.properties', 'DriverManager.getConnection', 'SQLException', 'RuntimeException'):
                    body = body.replace(term, '<span class="table-term">'+term+'</span>')
            align = 'center' if comparison and header_cell and j else alignments[j]
            declarations = [f'text-align:{align}']
            if cell and cell['fill'].lower() not in {'#ffffff', '#fff', 'white'}:
                declarations.append(f'background:{cell["fill"]}')
            if align == 'right':
                declarations.append('white-space:nowrap')
            scope = ' scope="col"' if header_cell else ''
            cells.append(f'<{tag}{scope} style="'+ ';'.join(declarations)+'">'+body+f'</{tag}>')
        rows.append('<tr'+('' if header_cell else ' data-break-row'+ids_attr([ident]))+'>'+''.join(cells)+'</tr>')
    if node['has_header']:
        content = '<thead>'+rows[0]+'</thead><tbody>'+''.join(rows[1:])+'</tbody>'
    else:
        content = '<tbody>'+''.join(rows)+'</tbody>'
    widths = [25,37.5,37.5] if comparison else [43,57] if property_table else (
        [b-a for a,b in zip(info['xs'],info['xs'][1:])] if info else [1]*len(node['rows'][0]))
    if folder.name == '06' and ident in {'p197-table01', 'p200-table01'}:
        widths[2] += 8
        widths[5] -= 8
    columns = '<colgroup>'+''.join(f'<col style="width:{100*w/sum(widths):.5f}%">' for w in widths)+'</colgroup>'
    modifier = ' comparison-table' if comparison else ' property-table' if property_table else ''
    return '<section class="card table-card'+modifier+'"><div class="card-content"><table>'+columns+content+'</table></div></section>'


def explanation_label(value):
    value = re.sub(r'(\d+)\s*行(?!目)', r'\1行目', value)
    value = re.sub(r'(\d+)\s*行目', r'\1行目', value)
    value = re.sub(r'(\d+)(?:行目)?\s*[-～]\s*(\d+)行目', r'\1～\2行目', value)
    return value


def meaning_parts(row, nodes):
    """原文のoffsetでSpanを切り出し、部分強調やリンクを保持する。"""
    parts = []
    meaning_cursor = 0
    for fragment in row['source_fragments']:
        if fragment['role'] != 'meaning':
            continue
        ident = fragment['source_id']
        position = row['meaning'].find(fragment['text'], meaning_cursor)
        if position < 0 or row['meaning'][meaning_cursor:position].strip():
            raise ValueError('構文解説の原文断片が一致しません: '+ident)
        if position > meaning_cursor:
            parts.append((row['meaning'][meaning_cursor:position], None, ident))
        meaning_cursor = position+len(fragment['text'])
        source = nodes.get(ident)
        if source is None or 'start' not in fragment:
            parts.append((fragment['text'], None, ident))
            continue
        cursor = 0
        for text, style in source['parts']:
            start, end = max(0, fragment['start']-cursor), min(len(text), fragment['end']-cursor)
            if start < end:
                parts.append((text[start:end], style, ident))
            cursor += len(text)
    if meaning_cursor < len(row['meaning']) and not row['meaning'][meaning_cursor:].strip():
        parts.append((row['meaning'][meaning_cursor:], None, row['source_ids'][-1]))
    if ''.join(text for text, _, _ in parts) != row['meaning']:
        raise ValueError('構文解説の原文Spanが一致しません: '+str(row['source_ids']))
    return parts


def meaning_span(text, style_id, layout):
    safe = escape(text.translate(SYMBOLS)).replace('\n', '')
    if not style_id:
        return safe
    effects = style_id.split(':')
    style = layout.get('styles', {}).get(effects[-1])
    emphasized = 'strong' in effects or bool(style and (
        style.get('stroke', 0) or style.get('flags', 0)&16 or 'Bold' in style['font']))
    family = 'MS PGothic' if emphasized else 'MS PMincho'
    declarations = [f'font-family:"{family}"', f'font-weight:{700 if emphasized else 400}']
    if style:
        name = style['font']
        declarations += [f'font-size:{style["size"]}pt', f'color:{style["color"]}']
        if 'Italic' in name or style.get('flags', 0)&2:
            declarations.append('font-style:italic')
    if 'emph' in effects:
        declarations.append('font-style:italic')
    if 'underline' in effects:
        declarations.append('text-decoration:underline')
    classes = 'source-style prose-emphasis' if emphasized else 'source-style'
    body = '<span class="'+classes+'" style="'+escape(';'.join(declarations), quote=True)+'">'+safe+'</span>'
    link = next((effect[5:] for effect in effects if effect.startswith('link%')), None)
    return '<a href="'+escape(unquote(link), quote=True)+'">'+body+'</a>' if link else body


def meaning_html(row, nodes, layout):
    parts = meaning_parts(row, nodes)
    meaning = row['meaning']
    paragraph_breaks = set(row.get('word_paragraph_breaks', []))
    if 'word_paragraph_breaks' not in row:
        paragraph_breaks.update(match.end() for match in re.finditer(r'\n\n+', meaning))
    paragraph_breaks.update(row.get('editor_paragraph_breaks', []))
    line_breaks = (set(row.get('word_line_breaks', []))
                   - set(row.get('editor_ignored_line_breaks', [])) - paragraph_breaks)
    if any(not isinstance(offset, int) or not 0 < offset < len(meaning)
           for offset in paragraph_breaks | line_breaks):
        raise ValueError('構文解説の段落・改行位置が本文にありません: '+str(row['source_ids']))
    cuts = sorted({0, len(meaning), *paragraph_breaks, *line_breaks})
    paragraphs, body, ids = [], [], []
    paragraph_start = 0
    for start, end in zip(cuts, cuts[1:]):
        cursor = 0
        for text, style, ident in parts:
            a, b = max(0, start-cursor), min(len(text), end-cursor)
            if a < b:
                body.append(meaning_span(text[a:b], style, layout))
                ids.append(ident)
            cursor += len(text)
        if end in line_breaks:
            body.append('<br>')
        if end in paragraph_breaks or end == len(meaning):
            if meaning[start:end].strip() or body:
                text = meaning[paragraph_start:end].lstrip()
                classes = 'explanation-paragraph'
                if re.match(r'^第\s*\d+\s*引数[：:]', text):
                    classes += ' explanation-argument-paragraph'
                elif text.startswith('※'):
                    classes += ' explanation-note-paragraph'
                paragraphs.append('<p class="'+classes+'" data-split-paragraph'+ids_attr(list(dict.fromkeys(ids)))+'>'+''.join(body)+'</p>')
            body, ids = [], []
            paragraph_start = end
    return ''.join(paragraphs)


def explanation_html(record, nodes, layout=None):
    lang = next((language(nodes[i]) for i in record['owner_code_ids'] if i in nodes), 'java')
    output = []
    for row in record['rows']:
        source_ids = list(dict.fromkeys(fragment['source_id'] for fragment in row['source_fragments']))
        prose = meaning_html(row, nodes, layout or {})
        keep = ' data-keep-next' if prose else ''
        output.append('<section class="explanation-item"><div class="explanation-code" data-break-row'+keep+ids_attr(source_ids)+'><div class="line-label">'+escape(explanation_label(row['line_label']))+'</div><pre class="source-code" spellcheck="false">'+highlighted(canonical(textwrap.dedent(row['code'])),lang,soft_breaks=True)+'</pre></div><div class="explanation-meaning">'+prose+'</div></section>')
    return '<section class="card explanation-card">'+header('コードの読み方')+'<div class="card-content">'+''.join(output)+'</div></section>'


def prepare(folder, config, layout, nodes, figures, order):
    chapter = folder.name
    fixed = set(config.get('native_pages',[]))
    pages = {ident:page['source_page'] for page in order for ident in page['entries']}
    numbered_figures = figure_numbers(config, layout, nodes, figures, order)
    explanations = [r for r in json.loads((HERE/'code_explanations.json').read_text(encoding='utf-8')) if r['chapter']==chapter and pages[r['anchor_id']] not in fixed]
    for record in explanations:
        for ident, original in record['source_texts'].items():
            if ident not in nodes or nodes[ident]['text'] != original:
                raise ValueError('構文解説の対応データをMarkdownに合わせて更新してください: '+ident)
        for row in record['rows']:
            for line in row['code_line_sources']:
                source = {part['number']:part['code'] for part in source_rows(nodes[line['code_id']], line['code_id'])}
                if source.get(line['line_number']) != canonical(line['text']):
                    raise ValueError('構文解説の行番号をコードに合わせて更新してください: '+line['code_id'])
    explanation_ids = {i for r in explanations for i in r['consume_ids']}
    filenames = [r for r in json.loads((HERE/'filename_labels.json').read_text(encoding='utf-8')) if r['chapter']==chapter]
    geometries = code_geometries(folder,layout,nodes)
    groups = defaultdict(list)
    for ident,node in nodes.items():
        if node['kind']!='code' or ident in explanation_ids or pages[ident] in fixed:
            continue
        geometry = geometries.get(ident)
        key = (pages[ident],tuple(geometry['frame'])) if geometry else (pages[ident],ident)
        groups[key].append(ident)
    specs = []
    def add(ident, anchor, consume, html, width=426.672, offset=0, kind='code'):
        specs.append({'id':chapter+'-'+ident, 'anchor':anchor, 'consume':list(dict.fromkeys(consume)),
            'html':html, 'width':width, 'offset':offset, 'kind':kind})
    for group in groups.values():
        ident = group[0]
        geo = geometries.get(ident)
        width = geo['frame'][2]-geo['frame'][0] if geo else (410.672 if ident.startswith('revision-messages-') else 426.672)
        offset = geo['frame'][0]-85.104 if geo else 0
        caption_ids = list(dict.fromkeys(i for g in group for i in geometries.get(g,{}).get('caption_ids',[]) if FILE_LABEL.fullmatch(nodes[i]['text'].strip())))
        names = [(nodes[i]['text'].strip(),[i]) for i in caption_ids]
        if nodes[ident].get('attrs',{}).get('filename'):
            names = [(nodes[ident]['attrs']['filename'],[])]
        label_figures = [r for r in filenames if r['code_id'] in group]
        for label in label_figures:
            if not names:
                names.append((label['text'],[label['figure_id']]))
            else:
                names[0][1].append(label['figure_id'])
        lang = language(nodes[ident], names[0][0] if names else '')
        rows = []
        for g in group:
            if rows:
                rows.append({'number':rows[-1]['number']+1,'code':'','ids':[]})
            rows += source_rows(nodes[g],g,rows[-1]['number']+1 if rows else 1)
        attached = list(dict.fromkeys(i for g in group for i in geometries.get(g,{}).get('figure_ids',[])))
        footer = ''
        if 'p071-f08' in attached:
            footer = '<div'+ids_attr(['p071-f08'])+'>接続URL：<code>jdbc:mysql://[サーバーURL]/[データベース名]?[その他設定]</code></div>'
        for image_id in attached:
            if image_id in {r['figure_id'] for r in label_figures} or image_id=='p071-f08':
                continue
            if image_id=='p113-f50':
                footer += '<div class="conversion-note"'+ids_attr([image_id])+'>ProductForm → Product</div>'
            else:
                import base64
                data=base64.b64encode((folder/figures[image_id]).read_bytes()).decode()
                f=next(f for f in layout['figures'] if f['id']==image_id)
                number = numbered_figures.get(image_id, {}).get('number')
                footer += '<figure class="code-figure"'+ids_attr([image_id])+'>'
                if number:
                    footer += '<figcaption class="code-figure-label">'+escape(number)+'</figcaption>'
                footer += '<img alt="実行結果の例" style="width:'+str(f['box'][2]-f['box'][0])+'pt" src="data:image/svg+xml;base64,'+data+'"></figure>'
        consume = group+caption_ids+attached+[r['figure_id'] for r in label_figures]
        add(ident,ident,consume,code_html(rows,lang,names,footer),width,offset)
    for ident,node in nodes.items():
        if node['kind']=='table' and pages[ident] not in fixed:
            info=layout.get('tables',{}).get(ident)
            # 表は共通の本文幅へ揃え、数値や短い列名の不自然な折り返しを避ける。
            width=426.672
            offset=0
            add(ident,ident,[ident],table_html(folder,layout,ident,node),width,offset,'table')
    for index,record in enumerate(explanations):
        add('explanation-'+str(index+1),record['anchor_id'],record['consume_ids'],explanation_html(record,nodes,layout),kind='explanation')
    consume = {}
    for spec in specs:
        for ident in spec['consume']:
            if ident in consume:
                raise ValueError('HTML部品の二重取り込み: '+ident)
            consume[ident]=spec['id']
    _render(specs,chapter)
    parts, anchors, expected = {}, {}, []
    for spec in specs:
        rendered = spec['result']['parts']
        occurrences=defaultdict(list)
        for index,part in enumerate(rendered):
            for ident in part['anchors']:
                occurrences[ident].append(index)
        missing=set(spec['consume'])-set(occurrences)
        # 画像の文字ラベル化などで残るIDは、カードの末尾へ所属させる。
        for ident in missing:
            rendered[-1]['anchors'][ident]={'x0':0,'y0':rendered[-1]['height']-1,'x1':1,'y1':rendered[-1]['height']}
            occurrences[ident]=[len(rendered)-1]
        tokens=[]
        for index,part in enumerate(rendered):
            token=spec['id']+'-part'+str(index+1)
            events=[]
            for ident,box in part['anchors'].items():
                first,last=occurrences[ident][0],occurrences[ident][-1]
                kind=nodes.get(ident,{}).get('kind')
                if ident in figures:
                    # 繰り返されるファイル名ヘッダーの図版IDは、最初の出現に所属させる。
                    if index==first:
                        events += [{'id':ident,'edge':'start','x':box['x0'],'y':box['y0']},
                                   {'id':ident,'edge':'end','x':box['x1'],'y':box['y1']}]
                    continue
                if kind=='heading' or ident in [i for i in spec['consume'] if i in nodes and FILE_LABEL.fullmatch(nodes[i]['text'].strip())]:
                    if index==first:events.append({'id':ident,'edge':'heading','x':box['x0'],'y':box['y0']})
                else:
                    if index==first:
                        if kind in ('code','table'):events.append({'id':ident,'edge':('short-' if first==last else 'long-')+('code' if kind=='code' else 'table'),'x':box['x0'],'y':box['y0']})
                        events.append({'id':ident,'edge':'start','x':box['x0'],'y':box['y0']})
                    if index==last:events.append({'id':ident,'edge':'end','x':box['x1'],'y':box['y1']})
            parts[token]={**part,'events':events,'offset':spec['offset'],'kind':spec['kind']}
            expected.append(part['pdf_text'])
            tokens.append(token)
        anchors[spec['anchor']]=tokens
    return {'parts':parts,'anchors':anchors,'consume':set(consume),'expected_text':''.join(expected),'specs':specs}


def _render(specs, chapter):
    cache=ROOT/'tmp/html-components'
    cache.mkdir(parents=True,exist_ok=True)
    version=(HERE/'components.css').read_bytes()+(HERE/'render_components.cjs').read_bytes()+Path(__file__).read_bytes()
    pending=[]
    for spec in specs:
        key=sha256(version+json.dumps({k:spec[k] for k in ('id','width','html')},ensure_ascii=False).encode()).hexdigest()
        spec['cache_key']=key
        path=cache/(key+'.json')
        if path.exists():
            spec['result']=json.loads(path.read_text(encoding='utf-8'))
        else:pending.append(spec)
    if pending:
        out=cache/('render-'+chapter)
        request=cache/('request-'+chapter+'.json')
        request.write_text(json.dumps({'output_dir':str(out),'cards':[{k:s[k] for k in ('id','width','html')} for s in pending]},ensure_ascii=False),encoding='utf-8')
        env=dict(os.environ)
        if not env.get('NODE_PATH'):env['NODE_PATH']=str(RUNTIME/'node/node_modules')
        process = subprocess.run(['node',str(HERE/'render_components.cjs'),str(request)],env=env,capture_output=True,text=True,encoding='utf-8')
        if process.returncode:
            raise RuntimeError(process.stderr or process.stdout)
        results=json.loads((out/'results.json').read_text(encoding='utf-8'))
        for spec,result in zip(pending,results['cards']):
            for index,part in enumerate(result['parts']):
                target=cache/(spec['cache_key']+'-'+str(index+1)+'.pdf')
                target.write_bytes(Path(part['pdf']).read_bytes())
                part['pdf']=str(target)
                doc=fitz.open(stream=target.read_bytes(), filetype='pdf')
                if len(doc)!=1:raise ValueError('HTML部品が単頁ではありません: '+spec['id'])
                if finish_prose_emphasis(doc, spec['html']):
                    target.write_bytes(doc.tobytes(garbage=4, deflate=True))
                # Chromeの紙寸法の丸めを除き、DOMと同じpt座標で合成する。
                part['pdf_text']=doc[0].get_text()
                if Counter(normalized(part['text']))!=Counter(normalized(part['pdf_text'])):
                    raise ValueError('HTML/PDFの文字差: '+spec['id']+' '+str(Counter(normalized(part['text']))-Counter(normalized(part['pdf_text']))))
                doc.close()
            spec['result']=result
            (cache/(spec['cache_key']+'.json')).write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
    preview=ROOT/'output/html/textbook'
    preview.mkdir(parents=True,exist_ok=True)
    css=(HERE/'components.css').read_text(encoding='utf-8')
    body='\n'.join('<article><p class="preview-id">'+escape(spec['id'])+'</p><div style="width:'+str(spec['width'])+'pt">'+spec['html']+'</div></article>' for spec in specs)
    (preview/(chapter+'.html')).write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><title>'+escape(chapter)+' 教材部品プレビュー</title><style>'+css+'body{padding:24px;background:#eef2f6}article{margin:0 auto 28px;width:max-content;max-width:100%}.preview-id{font:12px sans-serif;color:#475569}</style><body>'+body+'</body></html>',encoding='utf-8')


def finish_prose_emphasis(doc, html):
    """Edgeが印刷時に落とす解説の擬似太字を、単一の文字描画で仕上げる。"""
    sizes = {float(value) for value in re.findall(
        r'class="source-style prose-emphasis" style="[^\"]*font-size:([\d.]+)pt', html)}
    if not sizes:
        return 0
    changed = 0
    for page in doc:
        fonts = {font[4].encode() for font in page.get_fonts() if font[3].endswith('+MS-PGothic')}
        def finish(match):
            nonlocal changed
            body = match[1]
            uses = re.findall(rb'/([^\s]+)\s+([\d.]+)\s+Tf\b', body)
            if len(uses) != 1 or uses[0][0] not in fonts or b'2 Tr' in body:
                return match[0]
            size = float(uses[0][1])
            # Chromiumの文字サイズはCSS px、紙面上はその3/4pt。
            if not any(abs(size*.75 - value) < .01 for value in sizes):
                return match[0]
            changed += 1
            # 通常本文のPゴシック強調と同じ size/35。文字列・位置・色は動かさない。
            return b'q\n'+str(size/35).encode()+b' w\nBT\n2 Tr\n'+body+b'\n0 Tr\nET\nQ'
        for xref in page.get_contents():
            original = doc.xref_stream(xref)
            updated = re.sub(rb'\bBT\s(.*?)\bET\b', finish, original, flags=re.S)
            if updated != original:
                doc.update_stream(xref, updated)
    return changed


def embed(pdf, modern, marks):
    positioned={m['id']:m for m in marks if m['edge']=='html-component'}
    for token,part in modern['parts'].items():
        mark=positioned[token]
        page=pdf[mark['page']-1]
        rect=fitz.Rect(mark['x'],mark['y'],mark['x']+part['width'],mark['y']+part['height'])
        with fitz.open(part['pdf']) as component:
            clip=fitz.Rect(0,0,part['width'],part['height'])&component[0].rect
            page.show_pdf_page(rect,component,clip=clip,keep_proportion=False)
