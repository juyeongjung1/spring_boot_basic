"""演習の手順・箇条書き・補足を、原稿の文字と改行から区別する。"""
import re

STEP = re.compile(r'^[a-z]\.\s+')
HINT = re.compile(r'^(?:【ヒント】|ヒント)(?:\s|$)')
CHECK = re.compile(r'^[■◼]?\s*動作確認(?:[：:]|\s|$)')
ITEM = re.compile(r'^([■◼●⚫•\uf09f▪○]|[o・](?=\s)|[a-z]\))\s*')


def first_line(parts):
    end = next((i for i, (text, _) in enumerate(parts) if text.startswith('\n')), len(parts))
    return parts[:end], parts[end+1:]


def trim_prefix(parts, length):
    """書体・リンクを保って行頭のラベルと空白を取り除く。"""
    rest = []
    for text, style in parts:
        if len(text) > length:
            rest.append((text[length:], style))
        length = max(0, length - len(text))
    return rest


def items(parts, keep_lines=False):
    """項目内の折り返しと、次の箇条書きへ移る改行を区別する。"""
    rows = []
    current = []
    marker = ''
    line = []
    for text, style in [*parts, ('\n', None)]:
        if not text.startswith('\n'):
            line.append((text, style))
            continue
        raw = ''.join(value for value, _ in line)
        stripped = raw.lstrip()
        match = ITEM.match(stripped)
        if match:
            if current:
                rows.append((marker, current))
            marker = match[1]
            current = trim_prefix(line, len(raw) - len(stripped) + match.end())
        elif line:
            if keep_lines and current:
                current.append(('\n', None))
            current.extend(line)
        line = []
    if current or marker:
        rows.append((marker, current))
    return rows


def layout_info(nodes, order):
    intro = set()
    continuation = {}
    for page in order:
        entries = page['entries']
        if any(nodes.get(ident, {}).get('text', '').strip() in ('演習の目標', '予想所要時間')
               for ident in entries):
            intro.update(entries)
        for previous, following in zip(entries, entries[1:]):
            a = nodes.get(previous, {}).get('text', '').strip()
            b = nodes.get(following, {})
            next_text = b.get('text', '').strip()
            joined = b.get('attrs', {}).get('join-previous') == 'true'
            if (a and (STEP.match(a) or ITEM.match(a)) and not a.endswith(('。', '！', '？', '：', '!', '?', ':'))
                    and (b.get('kind') == 'heading' or joined)
                    and not re.match(r'^(?:演習|予想所要時間|[a-z]\.|[■◼●⚫•▪○\uf09f【<＜])', next_text)
                    and not HINT.match(next_text) and not CHECK.match(next_text)):
                continuation[previous] = following
    return intro, continuation
