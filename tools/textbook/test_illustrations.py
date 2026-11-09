"""小型挿絵の寸法・caption・元頁所属、過去の原文保全と今回の許可差分を検証する。"""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unittest

import pymupdf as fitz
from PIL import Image

from build import ROOT, read_markdown

CATALOG = ROOT / 'docs/textbook/illustrations.json'
APPROVED_EDITION = 'f16135f3cebb2e2f9ab481e9cfead35b05bd52d4'
FIGURE_REVISION_EDITION = '96a99882326d65ec048100b2f20fa0ed4aaa72d2'
REVIEW_EDITION = 'ac012ddc04163641c9fa3c865b11b00b0b6307d6'
SPACING_EDITION = '380e36fb9b1aae65f4f82405ab39f669e4c2f083'
TABLE_EDITION = 'ee2f9a455b14bbb85cec9e97e208bd948eaff8f2'
MODEL_EDITION = '0409a5379334731099867c078bc75a02e25a136d'
MODEL_APPROVED_EDITION = '39f5fef6a2b47de1d5a290820bce10f65dae459b'
MODEL_TRANSFER = 'illustration-2026-model-transfer'
MODEL_UNPACK = 'illustration-2026-model-moving-unpack'
MODEL_MOVING_PAGES = {MODEL_TRANSFER: 65, MODEL_UNPACK: 67}
REPOSITORY_PAGES = {'illustration-expansion-2026-repository-implementation': 90, 'revision-di-remote': 92}
DI_INTRO = 'illustration-figure-cards-2026-di-remote-intro'
MANAGED = 'illustration-expansion-2026-boot-managed-versions'
BEAN = 'illustration-expansion-2026-bean-auto-configuration'
REMOVED_MANAGED_ASSET = 'docs/textbook/chapters/01/assets/revision-ill-boot-managed-versions.png'
FORM = 'illustration-expansion-2026-form-name-binding'
REPOSITORY = 'illustration-2026-repository-results'
EACH = 'illustration-review-v4-each-variable-key'
REMOVED_REPOSITORY_ASSET = 'docs/textbook/chapters/03/assets/revision-ill-repository.png'


@lru_cache(maxsize=None)
def catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def chapter(name):
    folder = ROOT / 'docs/textbook/chapters' / name
    nodes, figures, pages = read_markdown(folder / 'chapter.md')
    config = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
    return folder, nodes, figures, pages, config


@lru_cache(maxsize=None)
def base_chapter(name, base=None):
    base = base or catalog()['base_commit']
    relative = 'docs/textbook/chapters/' + name + '/chapter.md'
    result = subprocess.run(['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show', base + ':' + relative],
                            cwd=ROOT, check=True, capture_output=True)
    path = ROOT / 'tmp/illustrations-tests/base' / base / (name + '.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.stdout)
    return read_markdown(path)


@lru_cache(maxsize=None)
def edition_json(relative, base=REVIEW_EDITION):
    result = subprocess.run(['git', '-c', 'safe.directory=' + ROOT.as_posix(),
        'show', base + ':' + relative], cwd=ROOT, check=True, capture_output=True)
    return json.loads(result.stdout)


def edition_chapter(name, edition):
    nodes, figures, pages = base_chapter(name, edition)
    return (ROOT/'docs/textbook/chapters'/name, nodes, figures, pages,
            edition_json('docs/textbook/chapters/' + name + '/source.json', edition))


def reviewed_chapter(name):
    # 過去の挿絵追加を全原文と照合する検査は、承認済み版で固定する。
    return edition_chapter(name, REVIEW_EDITION)


def image_size(record):
    folder = ROOT / 'docs/textbook/chapters' / record['chapter']
    with Image.open(folder / record['asset']) as image:
        width = float(record['width'])
        height = width * image.height / image.width
    if height > record['max_height']:
        width *= record['max_height'] / height
        height = record['max_height']
    return width, height


class IllustrationSourceTests(unittest.TestCase):
    def test_new_assets_and_existing_di_follow_print_limits(self):
        data = catalog()
        self.assertEqual(len(data['new']), 34)
        self.assertEqual(len(data['resized']), 1)
        self.assertEqual(data['resized'][0]['figure_id'], 'revision-di-remote')
        ids = [r['figure_id'] for r in data['new'] + data['resized']]
        self.assertEqual(len(ids), len(set(ids)))
        for record in data['new'] + data['resized']:
            with self.subTest(figure=record['figure_id']):
                folder = chapter(record['chapter'])[0]
                asset = folder / record['asset']
                self.assertTrue(asset.is_file())
                if record in data['new']:
                    self.assertIn('asset_sha256', record)
                    self.assertIn('image_pixels', record)
                if 'asset_sha256' in record:
                    self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), record['asset_sha256'])
                with Image.open(asset) as image:
                    if 'image_pixels' in record:
                        self.assertEqual(list(image.size), record['image_pixels'])
                        # 旧来の比率を保ち、引っ越しの2図は実寸を個別に検査する。
                        if record['figure_id'] in MODEL_MOVING_PAGES:
                            self.assertEqual(image.size, (1920, 819))
                        elif record['figure_id'].startswith('illustration-2026-'):
                            self.assertAlmostEqual(image.width / image.height, 2.4, delta=.04)
                width, height = image_size(record)
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)
                self.assertLessEqual(width, data['print_limits']['max_width'])
                self.assertLessEqual(height, data['print_limits']['max_height'])
                self.assertLessEqual(width, 260 if record in data['resized'] else 280)

    def test_figure_and_caption_are_adjacent_in_the_declared_source_page(self):
        for record in catalog()['new'] + catalog()['resized']:
            with self.subTest(figure=record['figure_id']):
                _, nodes, figures, pages, config = chapter(record['chapter'])
                owners = {ident: p['source_page'] for p in pages for ident in p['entries']}
                order = [ident for p in pages for ident in p['entries']]
                figure, caption = record['figure_id'], record['caption_id']
                self.assertEqual(figures[figure], record['asset'])
                self.assertEqual(owners[figure], record['source_page'])
                self.assertEqual(owners[caption], record['source_page'])
                self.assertEqual(order.index(caption), order.index(figure) + 1)
                options = config['illustrations'][figure]
                self.assertEqual(options['caption_id'], caption)
                self.assertEqual(options['width'], record['width'])
                self.assertEqual(options['max_height'], record['max_height'])
                if 'caption' in record:
                    self.assertEqual(nodes[caption]['text'], record['caption'])
                    self.assertEqual(order.index(figure), order.index(record['after_id']) + 1)
                    self.assertEqual(order.index(record['before_id']), order.index(caption) + 1)

    def test_original_text_code_and_id_order_are_unchanged(self):
        data = edition_json('docs/textbook/illustrations.json')
        additions = defaultdict(set)
        captions = defaultdict(set)
        for record in data['new']:
            additions[record['chapter']].add(record['figure_id'])
            captions[record['chapter']].add(record['caption_id'])
        original_count = current_count = 0
        for name in data['reviewed_chapters']:
            before_nodes, before_figures, before_pages = base_chapter(name)
            _, nodes, figures, pages, _ = reviewed_chapter(name)
            with self.subTest(chapter=name):
                self.assertEqual(set(nodes) - set(before_nodes), captions[name])
                self.assertEqual(set(figures) - set(before_figures), additions[name])
                self.assertFalse(set(before_nodes) - set(nodes))
                self.assertFalse(set(before_figures) - set(figures))
                for ident, node in before_nodes.items():
                    # 字下げなど表示用attrsは本文の文字や既存書式Spanと区別する。
                    self.assertEqual({k:v for k,v in node.items() if k != 'attrs'},
                                     {k:v for k,v in nodes[ident].items() if k != 'attrs'}, ident)
                for ident, path in before_figures.items():
                    self.assertEqual(figures[ident], path, ident)
                self.assertEqual([p['source_page'] for p in pages], [p['source_page'] for p in before_pages])
                for old, new in zip(before_pages, pages):
                    allowed = additions[name] | captions[name]
                    self.assertEqual([i for i in new['entries'] if i not in allowed], old['entries'])
            original_count += len(before_nodes) + len(before_figures)
            current_count += len(nodes) + len(figures)
        self.assertEqual(original_count, 2879)
        self.assertEqual(current_count, original_count + 66)

    def test_only_new_illustration_settings_are_added_since_the_approved_edition(self):
        data = edition_json('docs/textbook/illustrations.json')
        command = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show']
        previous = subprocess.run(command + [APPROVED_EDITION + ':docs/textbook/illustrations.json'],
            cwd=ROOT, check=True, capture_output=True)
        previous = json.loads(previous.stdout)
        previous_records = {r['figure_id']: r for r in previous['new']}
        current_records = {r['figure_id']: r for r in data['new']}
        self.assertEqual(len(current_records.keys() - previous_records.keys()), 24)
        for ident, record in previous_records.items():
            self.assertEqual(current_records[ident], record, ident)
        additions = defaultdict(set)
        for ident in current_records.keys() - previous_records.keys():
            additions[current_records[ident]['chapter']].add(ident)
        for name in data['reviewed_chapters']:
            with self.subTest(chapter=name):
                relative = 'docs/textbook/chapters/' + name + '/source.json'
                before = subprocess.run(command + [APPROVED_EDITION + ':' + relative],
                    cwd=ROOT, check=True, capture_output=True)
                before = json.loads(before.stdout)
                config = reviewed_chapter(name)[4]
                self.assertEqual({k:v for k,v in config.items() if k not in {'illustrations','pagination'}},
                                 {k:v for k,v in before.items() if k not in {'illustrations','pagination'}})
                old_options = before.get('illustrations', {})
                new_options = config.get('illustrations', {})
                self.assertEqual(set(new_options) - set(old_options), additions[name])
                for ident, options in old_options.items():
                    self.assertEqual(new_options[ident], options, ident)

    def test_original_baseline_layout_and_assets_are_unchanged(self):
        paths = []
        for name in catalog()['reviewed_chapters']:
            folder = 'docs/textbook/chapters/' + name
            paths += [folder+'/baseline.md', folder+'/source-layout.json', folder+'/assets']
        result = subprocess.run(['git', '-c', 'safe.directory='+ROOT.as_posix(), 'diff', '--name-only',
            '--no-renames', catalog()['base_commit'], '--', *paths], cwd=ROOT, check=True,
            capture_output=True, encoding='utf-8')
        allowed = {'docs/textbook/chapters/'+r['chapter']+'/'+r['asset'] for r in catalog()['new']+catalog()['resized']}
        allowed.add(REMOVED_MANAGED_ASSET)
        allowed.add(REMOVED_REPOSITORY_ASSET)
        self.assertTrue(set(result.stdout.splitlines()).issubset(allowed), result.stdout)

    def test_only_requested_di_bean_changes_follow_the_previous_edition(self):
        data = edition_json('docs/textbook/illustrations.json')
        command = ['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'show']
        previous = json.loads(subprocess.run(command +
            [FIGURE_REVISION_EDITION + ':docs/textbook/illustrations.json'],
            cwd=ROOT, check=True, capture_output=True).stdout)
        old_records = {r['figure_id']: r for r in previous['new'] + previous['resized']}
        records = {r['figure_id']: r for r in data['new'] + data['resized']}
        self.assertEqual(set(records) - set(old_records), {DI_INTRO})
        self.assertEqual(set(old_records) - set(records), {MANAGED})
        for ident, record in old_records.items():
            if ident not in {MANAGED, BEAN}:
                self.assertEqual(records[ident], record, ident)
        self.assertEqual(records[BEAN]['asset'], old_records[BEAN]['asset'])
        self.assertNotEqual(records[BEAN]['asset_sha256'], old_records[BEAN]['asset_sha256'])
        old_count = current_count = 0
        for name in data['reviewed_chapters']:
            before_nodes, before_figures, before_pages = base_chapter(name, FIGURE_REVISION_EDITION)
            _, nodes, figures, pages, config = reviewed_chapter(name)
            added = {DI_INTRO, DI_INTRO + '-caption'} if name == '01' else set()
            removed = {MANAGED, MANAGED + '-caption'} if name == '01' else set()
            moved = {BEAN, BEAN + '-caption'} if name == '01' else set()
            with self.subTest(chapter=name):
                old_ids, current_ids = set(before_nodes) | set(before_figures), set(nodes) | set(figures)
                self.assertEqual(current_ids - old_ids, added)
                self.assertEqual(old_ids - current_ids, removed)
                for ident, node in before_nodes.items():
                    if ident in removed or name == '01' and ident == BEAN + '-caption':
                        continue
                    self.assertEqual({k:v for k,v in node.items() if k != 'attrs'},
                                     {k:v for k,v in nodes[ident].items() if k != 'attrs'}, ident)
                for ident, path in before_figures.items():
                    if ident not in removed:
                        self.assertEqual(figures[ident], path, ident)
                self.assertEqual([p['source_page'] for p in pages], [p['source_page'] for p in before_pages])
                for old, new in zip(before_pages, pages):
                    ignored = added | removed | moved
                    self.assertEqual([i for i in old['entries'] if i not in ignored],
                                     [i for i in new['entries'] if i not in ignored])
                relative = 'docs/textbook/chapters/' + name + '/source.json'
                before_config = json.loads(subprocess.run(command + [FIGURE_REVISION_EDITION + ':' + relative],
                    cwd=ROOT, check=True, capture_output=True).stdout)
                current_config = dict(config)
                # 頁継続・小幅な図縮小はtest_paginationと専用監査で別に検査する。
                current_config.pop('pagination',None)
                current_options = dict(current_config.get('illustrations', {}))
                if name == '01':
                    old_options = before_config['illustrations']
                    old_options.pop(MANAGED)
                    current_options.pop(DI_INTRO)
                current_config['illustrations'] = current_options
                if 'illustrations' not in before_config:
                    current_config.pop('illustrations')
                self.assertEqual(current_config, before_config)
            old_count += len(before_nodes) + len(before_figures)
            current_count += len(nodes) + len(figures)
        self.assertEqual(old_count, 2945)
        self.assertEqual(current_count, old_count)
        _, _, _, pages, _ = reviewed_chapter('01')
        for ident, anchor, source in [(DI_INTRO, 'p020-b03', 20), (BEAN, 'p023-b02', 23)]:
            entries = next(p['entries'] for p in pages if p['source_page'] == source)
            position = entries.index(anchor)
            self.assertEqual(entries[position:position+3], [anchor, ident, ident + '-caption'])
            self.assertEqual(records[ident]['source_page'], source)
            self.assertEqual(records[ident]['after_id'], anchor)
        self.assertFalse((ROOT / REMOVED_MANAGED_ASSET).exists())
        allowed_assets = {REMOVED_MANAGED_ASSET,
            'docs/textbook/chapters/01/' + records[DI_INTRO]['asset'],
            'docs/textbook/chapters/01/' + records[BEAN]['asset']}
        asset_paths = ['docs/textbook/chapters/' + name + '/assets' for name in catalog()['reviewed_chapters']]
        changed_assets = subprocess.run(command[:-1] + ['diff', '--name-only', '--no-renames',
            FIGURE_REVISION_EDITION, REVIEW_EDITION, '--', *asset_paths], cwd=ROOT, check=True,
            capture_output=True, encoding='utf-8').stdout.splitlines()
        self.assertTrue(set(changed_assets).issubset(allowed_assets), changed_assets)

    def test_only_requested_content_changes_reached_the_approved_review_edition(self):
        data = edition_json('docs/textbook/illustrations.json', SPACING_EDITION)
        removed = {'02': {'p060-b09', 'p060-b10', 'p060-b11'},
            '03': {'p071-b06', 'p071-b07', 'p071-b08', REPOSITORY, REPOSITORY+'-caption'}}
        added = {'02': {'revision-login3-instruction'}, '03': {EACH, EACH+'-caption'}}
        codes = {'p083-b04', 'p084-b01', 'p085-b04', 'p086-b04', 'p086-b10',
                 'p087-b04', 'p092-b03', 'p092-b08', 'p109-b03'}
        changed = {'02': {'p061-b02', FORM, FORM+'-caption'},
                   '03': codes | {'p071-b05'}, 'ex04': {'p036-table01'}}
        annotations = {'Spring Controller で', 'model に格納した', 'キー名を右に。', '左は任意の変数名'}
        count = 0
        for name in data['reviewed_chapters']:
            _, old_nodes, old_figures, old_pages, old_config = reviewed_chapter(name)
            folder, nodes, figures, pages, config = edition_chapter(name, SPACING_EDITION)
            old_ids, ids = set(old_nodes) | set(old_figures), set(nodes) | set(figures)
            with self.subTest(chapter=name):
                self.assertEqual(old_ids - ids, removed.get(name, set()))
                self.assertEqual(ids - old_ids, added.get(name, set()))
                self.assertEqual([p['source_page'] for p in pages], [p['source_page'] for p in old_pages])
                for old, new in zip(old_pages, pages):
                    self.assertEqual([i for i in old['entries'] if i not in removed.get(name, set())],
                                     [i for i in new['entries'] if i not in added.get(name, set())])
                for ident in old_ids & ids:
                    if ident not in changed.get(name, set()):
                        self.assertEqual(nodes.get(ident), old_nodes.get(ident), ident)
                        self.assertEqual(figures.get(ident), old_figures.get(ident), ident)
                # 変換対象の外側は、Span・字下げ属性を含むMarkdown全字を保全する。
                previous = ROOT/'tmp/illustrations-tests/base'/REVIEW_EDITION/(name+'.md')
                current = ROOT/'tmp/illustrations-tests/base'/SPACING_EDITION/(name+'.md')
                texts = [previous.read_text(encoding='utf-8'), current.read_text(encoding='utf-8')]
                for index, text in enumerate(texts):
                    for ident in removed.get(name, set()) | added.get(name, set()) | changed.get(name, set()):
                        pattern = (r'^::: \{#'+re.escape(ident)+r'\b[^\n]*\}\n.*?^:::\n\n'
                                   r'|^!\[[^\n]*\]\([^\n]*\)\{#'+re.escape(ident)+r'\}\n\n')
                        text = re.sub(pattern, '', text, flags=re.M | re.S)
                    texts[index] = text
                self.assertEqual(texts[0], texts[1], name)
                expected = json.loads(json.dumps(old_config))
                if name == '03':
                    expected['illustrations'].pop(REPOSITORY)
                    expected['illustrations'][EACH] = {'caption_id': EACH+'-caption', 'width': 280, 'max_height': 140}
                self.assertEqual(config, expected, name)
                if name == '02':
                    self.assertEqual(nodes['p061-b02']['text'], 'http://localhost:8080/login3')
                    self.assertEqual(nodes['revision-login3-instruction']['text'], '社員番号と、パスワードを入力してください。')
                    self.assertEqual(nodes['p061-b02']['parts'], old_nodes['p061-b02']['parts'][:1])
                    self.assertEqual(nodes['revision-login3-instruction']['parts'], old_nodes['p061-b02']['parts'][2:])
                    self.assertEqual(nodes[FORM+'-caption']['text'],
                        'HTMLのname属性値をFormのフィールド名と対応させ、送信された値をまとめます。')
                    self.assertEqual(figures[FORM], old_figures[FORM])
                if name == '03':
                    for ident in codes:
                        before, after = old_nodes[ident], nodes[ident]
                        self.assertEqual({k:v for k,v in before.items() if k not in {'parts','text'}},
                                         {k:v for k,v in after.items() if k not in {'parts','text'}}, ident)
                        self.assertEqual([p[1] for p in before['parts']], [p[1] for p in after['parts']], ident)
                        lines = [line for line in before['text'].splitlines()
                                 if ident != 'p087-b04' or line.strip() not in annotations]
                        if ident == 'p092-b03':
                            lines = [line.replace('<!-— 省略 -->', '<!-- 省略 -->') for line in lines]
                        normalize = lambda line: re.sub(r'^(\d+:)\s*', r'\1', line.lstrip())
                        self.assertEqual([normalize(line) for line in lines],
                                         [normalize(line) for line in after['text'].splitlines()], ident)
                    rows = nodes['p071-b05']['rows']
                    self.assertEqual(rows[0], ['設定項目', '意味'])
                    self.assertEqual(len(rows), 5)
                    for ident, row in zip(['p071-b05','p071-b06','p071-b07','p071-b08'], rows[1:]):
                        self.assertEqual(''.join(old_nodes[ident]['text'].split()).replace('→',''),
                                         ''.join(''.join(row).split()), ident)
                    self.assertEqual(figures[EACH], 'assets/revision-ill-each-variable-key.png')
                    self.assertEqual(nodes[EACH+'-caption']['text'],
                        '「:」の右側はModelに格納したキー名、左側は繰り返しで使う任意の変数名です。')
                if name == 'ex04':
                    old_rows, new_rows = old_nodes['p036-table01']['rows'], nodes['p036-table01']['rows']
                    self.assertEqual(new_rows[0], old_rows[0])
                    self.assertEqual(new_rows[2:], old_rows[4:])
                    for column in range(3):
                        self.assertEqual(''.join(''.join(row[column] for row in old_rows[1:4]).split()),
                                         ''.join(new_rows[1][column].split()))
            count += len(ids)
        self.assertEqual(count, 2940)
        previous = edition_json('docs/textbook/illustrations.json')
        self.assertEqual({k:v for k,v in data.items() if k != 'new'},
                         {k:v for k,v in previous.items() if k != 'new'})
        old_records = {r['figure_id']: r for r in previous['new']}
        records = {r['figure_id']: r for r in data['new']}
        self.assertEqual(set(old_records)-set(records), {REPOSITORY})
        self.assertEqual(set(records)-set(old_records), {EACH})
        for ident in set(old_records) & set(records) - {FORM}:
            expected = dict(old_records[ident])
            if ident == 'illustration-expansion-2026-model-key-property':
                expected['before_id'] = 'p060-b12'
            self.assertEqual(records[ident], expected, ident)
        for ident, source, after, before in [(FORM,54,'p054-b03','p054-b04'), (EACH,87,'p087-b07','p088-b01')]:
            self.assertEqual([records[ident][k] for k in ('source_page','after_id','before_id')], [source,after,before])
        paths = ['docs/textbook/chapters/'+name+'/assets' for name in data['reviewed_chapters']]
        command = ['git','-c','safe.directory='+ROOT.as_posix()]
        changed_assets = subprocess.run(command+['diff','--name-only','--no-renames',REVIEW_EDITION,SPACING_EDITION,'--',*paths],
            cwd=ROOT,check=True,capture_output=True,encoding='utf-8').stdout.splitlines()
        self.assertEqual(set(changed_assets), {REMOVED_REPOSITORY_ASSET,
            'docs/textbook/chapters/02/assets/revision-ill-form-name-binding.png',
            'docs/textbook/chapters/03/assets/revision-ill-each-variable-key.png'})

    def test_only_requested_prose_and_spacing_changes_reached_the_approved_spacing_edition(self):
        review = ROOT/'output/verification/spacing-v5-2026'
        prose = json.loads((review/'prose/prose-changes.json').read_text(encoding='utf-8'))
        spacing = json.loads((review/'heading-spacing-plan.json').read_text(encoding='utf-8'))
        changes = {(r['chapter'],r['id']):r for r in prose['changes']}
        self.assertEqual(set(changes), {('02','p052-b07'),('02','p058-b01'),('02','p059-b06'),('02','p059-b10'),
            ('03','p069-b01'),('03','p078-b01'),('ex02','p015-b03'),('ex02','p015-b06'),('ex02','p015-b10'),('ex03','p020-b10')})
        accepted = {r['chapter']:r['accepted'] for r in spacing['chapters']}
        approved_catalog=edition_json('docs/textbook/illustrations.json',TABLE_EDITION)
        self.assertEqual(approved_catalog,edition_json('docs/textbook/illustrations.json',SPACING_EDITION))
        count, immutable = 0, ['docs/textbook/illustrations.json','tools/textbook/code_explanations.json','tools/textbook/filename_labels.json']
        for name in approved_catalog['reviewed_chapters']:
            folder, old_nodes, old_figures, old_pages, old_config = edition_chapter(name, SPACING_EDITION)
            _, nodes, figures, pages, config = edition_chapter(name, TABLE_EDITION)
            with self.subTest(chapter=name):
                self.assertEqual(set(nodes),set(old_nodes))
                self.assertEqual(figures,old_figures)
                self.assertEqual(pages,old_pages)
                for ident,node in old_nodes.items():
                    change=changes.get((name,ident))
                    if change is None:
                        self.assertEqual(nodes[ident],node,ident)
                    else:
                        self.assertEqual(node['text'],change['before'],ident)
                        self.assertEqual(nodes[ident]['text'],change['after'],ident)
                        self.assertEqual(json.loads(json.dumps(node['parts'])),change['before_parts'],ident)
                        self.assertEqual(json.loads(json.dumps(nodes[ident]['parts'])),change['after_parts'],ident)
                        self.assertEqual({k:v for k,v in node.items() if k not in {'parts','text'}},
                                         {k:v for k,v in nodes[ident].items() if k not in {'parts','text'}},ident)
                old_path=ROOT/'tmp/illustrations-tests/base'/SPACING_EDITION/(name+'.md')
                approved_path=ROOT/'tmp/illustrations-tests/base'/TABLE_EDITION/(name+'.md')
                texts=[old_path.read_text(encoding='utf-8'),approved_path.read_text(encoding='utf-8')]
                for index,text in enumerate(texts):
                    for chapter_name,ident in changes:
                        if chapter_name==name:
                            text=re.sub(r'^::: \{#'+re.escape(ident)+r'\b[^\n]*\}\n.*?^:::\n\n','',text,flags=re.M|re.S)
                    texts[index]=text
                self.assertEqual(texts[0],texts[1],name)
                expected=json.loads(json.dumps(old_config))
                if name=='02':
                    expected['pagination']['continue_before'].update({'51':'short-minor-heading','61':'short-minor-heading'})
                if accepted[name]:
                    expected['typography']={'minor_heading_extra_space':accepted[name]}
                self.assertEqual(config,expected,name)
            count+=len(nodes)+len(figures)
            prefix='docs/textbook/chapters/'+name+'/'
            immutable += [prefix+'baseline.md',prefix+'source-layout.json',prefix+'assets']
        self.assertEqual(count,2940)
        command=['git','-c','safe.directory='+ROOT.as_posix()]
        changed=subprocess.run(command+['diff','--name-only','--no-renames',SPACING_EDITION,TABLE_EDITION,'--',*immutable],
            cwd=ROOT,check=True,capture_output=True,encoding='utf-8').stdout
        self.assertFalse(changed,changed)

    def test_approved_table_revision_preserved_all_chapter_sources_settings_and_assets(self):
        immutable=['docs/textbook/illustrations.json','tools/textbook/code_explanations.json','tools/textbook/filename_labels.json']
        count=0
        for name in catalog()['reviewed_chapters']:
            _,old_nodes,old_figures,old_pages,old_config=edition_chapter(name,TABLE_EDITION)
            _,nodes,figures,pages,config=edition_chapter(name,MODEL_EDITION)
            with self.subTest(chapter=name):
                self.assertEqual(nodes,old_nodes)
                self.assertEqual(figures,old_figures)
                self.assertEqual(pages,old_pages)
                self.assertEqual(config,old_config)
                snapshot=ROOT/'tmp/illustrations-tests/base'/TABLE_EDITION/(name+'.md')
                approved=ROOT/'tmp/illustrations-tests/base'/MODEL_EDITION/(name+'.md')
                self.assertEqual(approved.read_text(encoding='utf-8'),snapshot.read_text(encoding='utf-8'))
            count+=len(nodes)+len(figures)
            prefix='docs/textbook/chapters/'+name+'/'
            immutable += [prefix+'baseline.md',prefix+'source-layout.json',prefix+'assets']
        self.assertEqual(count,2940)
        command=['git','-c','safe.directory='+ROOT.as_posix()]
        changed=subprocess.run(command+['diff','--name-only','--no-renames',TABLE_EDITION,MODEL_EDITION,'--',*immutable],
            cwd=ROOT,check=True,capture_output=True,encoding='utf-8').stdout
        self.assertFalse(changed,changed)

    def test_model_moving_revision_changes_only_the_two_declared_illustrations(self):
        placements=[(59,'p059-b03','revision-model-moving-pack',MODEL_TRANSFER,'p059-b04'),
                    (60,'p060-b03','revision-model-moving-unpack',MODEL_UNPACK,'p060-b04')]
        moved={MODEL_TRANSFER,MODEL_TRANSFER+'-caption'}
        added={row[2] for row in placements}|{MODEL_UNPACK,MODEL_UNPACK+'-caption'}
        edited_ids=moved|added

        _,old_nodes,old_figures,old_pages,old_config=edition_chapter('02',MODEL_EDITION)
        _,nodes,figures,pages,config=edition_chapter('02',MODEL_APPROVED_EDITION)
        self.assertEqual(set(nodes)|set(figures),set(old_nodes)|set(old_figures)|added)
        self.assertEqual(figures,old_figures|{MODEL_UNPACK:'assets/revision-ill-model-unpack.png'})
        self.assertEqual([dict(p,entries=[i for i in p['entries'] if i not in edited_ids]) for p in pages],
                         [dict(p,entries=[i for i in p['entries'] if i not in edited_ids]) for p in old_pages])
        for source,previous,intro,figure,following in placements:
            entries=next(p['entries'] for p in pages if p['source_page']==source)
            offset=entries.index(previous)
            self.assertEqual(entries[offset:offset+5],[previous,intro,figure,figure+'-caption',following])
            self.assertEqual(nodes[intro]['kind'],'paragraph')
            self.assertTrue(nodes[intro]['text'].strip())

        snapshots=ROOT/'tmp/illustrations-tests/base'
        texts=[(snapshots/edition/'02.md').read_text(encoding='utf-8')
               for edition in (MODEL_EDITION,MODEL_APPROVED_EDITION)]
        for ident in edited_ids:
            pattern=(r'^::: \{#'+re.escape(ident)+r'[ \t][^\n]*\}\n.*?^:::\n\n'
                     r'|^!\[[^\n]*\]\([^\n]*\)\{#'+re.escape(ident)+r'\}\n\n')
            texts=[re.sub(pattern,'',text,flags=re.M|re.S) for text in texts]
        self.assertEqual(texts[0],texts[1])

        def unchanged_settings(settings):
            return dict(settings,illustrations={k:v for k,v in settings['illustrations'].items()
                                               if k not in MODEL_MOVING_PAGES})
        self.assertEqual(unchanged_settings(config),unchanged_settings(old_config))
        old_catalog=edition_json('docs/textbook/illustrations.json',MODEL_EDITION)
        data=edition_json('docs/textbook/illustrations.json',MODEL_APPROVED_EDITION)
        self.assertEqual({k:v for k,v in data.items() if k!='new'},
                         {k:v for k,v in old_catalog.items() if k!='new'})
        self.assertEqual([r for r in data['new'] if r['figure_id'] not in MODEL_MOVING_PAGES],
                         [r for r in old_catalog['new'] if r['figure_id']!=MODEL_TRANSFER])

        paths=['docs/textbook/chapters','docs/textbook/illustrations.json',
               'tools/textbook/code_explanations.json','tools/textbook/filename_labels.json']
        command=['git','-c','safe.directory='+ROOT.as_posix()]
        result=subprocess.run(command+['diff','--name-only','--no-renames',MODEL_EDITION,MODEL_APPROVED_EDITION,'--',*paths],
            cwd=ROOT,check=True,capture_output=True,encoding='utf-8')
        prefix='docs/textbook/chapters/02/'
        allowed={prefix+p for p in ['chapter.md','source.json','assets/revision-ill-model.png','assets/revision-ill-model-unpack.png']}
        self.assertEqual(set(result.stdout.splitlines()),allowed|{'docs/textbook/illustrations.json'})

    def test_repository_revision_preserves_original_content(self):
        _,previous,old_figures,old_pages,old_config=edition_chapter('03',MODEL_APPROVED_EDITION)
        _,nodes,figures,pages,config=chapter('03')
        previous_catalog=edition_json('docs/textbook/illustrations.json',MODEL_APPROVED_EDITION)
        data=catalog()
        records=[r for key in ('new','resized') for r in data[key] if r['figure_id'] in REPOSITORY_PAGES]
        self.assertEqual({r['figure_id'] for r in records},set(REPOSITORY_PAGES))
        captions={r['caption_id'] for r in records}
        self.assertEqual(set(nodes),set(previous))
        self.assertEqual({ident for ident in nodes if nodes[ident]!=previous[ident]},captions)
        self.assertEqual((figures,pages,config),(old_figures,old_pages,old_config))

        def unaffected_catalog(data):
            return {key: [r for r in value if r['figure_id'] not in REPOSITORY_PAGES]
                    if key in ('new','resized') else value for key,value in data.items()}
        self.assertEqual(unaffected_catalog(data),unaffected_catalog(previous_catalog))

        paths=['docs/textbook/chapters','docs/textbook/illustrations.json',
               'tools/textbook/code_explanations.json','tools/textbook/filename_labels.json']
        command=['git','-c','safe.directory='+ROOT.as_posix()]
        changed=set()
        for query in (['diff','--name-only','--no-renames',MODEL_APPROVED_EDITION],['ls-files','--others','--exclude-standard']):
            result=subprocess.run(command+query+['--',*paths],cwd=ROOT,check=True,capture_output=True,encoding='utf-8')
            changed.update(result.stdout.splitlines())
        prefix='docs/textbook/chapters/03/'
        allowed={prefix+'chapter.md'}|{prefix+r['asset'] for r in records}
        self.assertEqual(changed,allowed|{'docs/textbook/illustrations.json'})


class IllustrationPdfTests(unittest.TestCase):
    def test_each_image_and_caption_stay_between_the_declared_pdf_anchors(self):
        contexts = {}
        data = catalog()
        for record in data['new'] + [r for r in data['resized'] if 'after_id' in r]:
            name = record['chapter']
            if name not in contexts:
                folder = ROOT / 'output/pdf/textbook' / ('chapter-' + name)
                checks = json.loads((folder / 'checks.json').read_text(encoding='utf-8'))
                pdf = fitz.open(folder / 'chapter-flow.pdf')
                self.addCleanup(pdf.close)
                contexts[name] = (checks['flow']['block_positions'], pdf)
            marks, pdf = contexts[name]

            def position(ident, edge):
                matches = [m for m in marks if m['id'] == ident and m['edge'] == edge]
                if edge == 'start':
                    matches += [m for m in marks if m['id'] == ident and m['edge'] == 'heading']
                if matches:
                    points = [(m['page'], round(m['y'], 2)) for m in matches]
                    return max(points) if edge == 'end' else min(points)
                # 見出し・手順には終端マーカーがないため、実PDFの文字の下端で確認する。
                heading = [m for m in marks if m['id'] == ident and m['edge'] == 'heading']
                self.assertTrue(edge == 'end' and len(heading) == 1, (ident, edge))
                mark = heading[0]
                rectangles = pdf[mark['page'] - 1].search_for(chapter(name)[1][ident]['text'])
                rectangles = [r for r in rectangles if abs(r.y0 - mark['y']) < 2]
                self.assertTrue(rectangles, ident)
                return mark['page'], round(max(r.y1 for r in rectangles), 2)

            with self.subTest(figure=record['figure_id']):
                anchors = [(record['after_id'], 'end'), (record['figure_id'], 'start'),
                           (record['figure_id'], 'end'), (record['caption_id'], 'start'),
                           (record['caption_id'], 'end'), (record['before_id'], 'start')]
                points = [position(ident, edge) for ident, edge in anchors]
                for index in range(len(points) - 1):
                    self.assertLessEqual(points[index], points[index + 1],
                        (anchors[index], points[index], anchors[index + 1], points[index + 1]))

    def test_image_dimensions_and_caption_are_kept_on_one_physical_page(self):
        assembly = json.loads((ROOT/'output/pdf/textbook/textbook/checks.json').read_text(encoding='utf-8'))
        chapter_starts = {p['chapter']:p['flow_pages'][0] for p in assembly['chapters']}
        expected_pages = MODEL_MOVING_PAGES | REPOSITORY_PAGES
        for record in catalog()['new'] + catalog()['resized']:
            with self.subTest(figure=record['figure_id']):
                folder = ROOT / 'output/pdf/textbook' / ('chapter-'+record['chapter'])
                checks = json.loads((folder/'checks.json').read_text(encoding='utf-8'))
                marks = checks['flow']['block_positions']
                figure = [m for m in marks if m['id'] == record['figure_id']]
                caption = [m for m in marks if m['id'] == record['caption_id']]
                self.assertEqual({m['edge'] for m in figure}, {'start','end'})
                self.assertEqual({m['edge'] for m in caption}, {'start','end'})
                self.assertEqual(len(figure), 2)
                self.assertEqual(len(caption), 2)
                self.assertEqual(len({m['page'] for m in figure+caption}), 1)
                start = next(m for m in figure if m['edge']=='start')
                end = next(m for m in figure if m['edge']=='end')
                cap_start = next(m for m in caption if m['edge']=='start')
                if record['figure_id'] in expected_pages:
                    physical_page = chapter_starts[record['chapter']] + start['page'] - 1
                    self.assertEqual(physical_page, expected_pages[record['figure_id']])
                self.assertGreaterEqual(cap_start['y'], end['y'] - .1)
                self.assertLessEqual(cap_start['y'] - end['y'], 30)
                expected_width, expected_height = image_size(record)
                with fitz.open(folder/'chapter-flow.pdf') as pdf:
                    images = pdf[start['page']-1].get_image_info()
                    matching = [fitz.Rect(i['bbox']) for i in images
                                if abs(i['bbox'][0]-start['x'])<.2 and abs(i['bbox'][1]-start['y'])<.2]
                    self.assertTrue(matching, (record['figure_id'],start,images))
                    rect = min(matching, key=lambda r: abs(r.width-expected_width)+abs(r.height-expected_height))
                    self.assertAlmostEqual(rect.width, expected_width, delta=.2)
                    self.assertAlmostEqual(rect.height, expected_height, delta=.2)
                    self.assertLessEqual(rect.width, 300.2)
                    self.assertLessEqual(rect.height, 140.2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
