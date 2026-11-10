"""小型挿絵の寸法・caption・元頁所属、過去の原文保全と今回の許可差分を検証する。"""
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unittest

import pymupdf as fitz
from PIL import Image

from build import ROOT, normalized, read_markdown

CATALOG = ROOT / 'docs/textbook/illustrations.json'
APPROVED_EDITION = 'f16135f3cebb2e2f9ab481e9cfead35b05bd52d4'
FIGURE_REVISION_EDITION = '96a99882326d65ec048100b2f20fa0ed4aaa72d2'
REVIEW_EDITION = 'ac012ddc04163641c9fa3c865b11b00b0b6307d6'
SPACING_EDITION = '380e36fb9b1aae65f4f82405ab39f669e4c2f083'
TABLE_EDITION = 'ee2f9a455b14bbb85cec9e97e208bd948eaff8f2'
MODEL_EDITION = '0409a5379334731099867c078bc75a02e25a136d'
MODEL_APPROVED_EDITION = '39f5fef6a2b47de1d5a290820bce10f65dae459b'
REPOSITORY_APPROVED_EDITION = '851c18e02f1d9144c99fb22948791f84a3adf34e'
SERVICE_APPROVED_EDITION = '9ccfcb292b2d261fc7e40318eaa9c506183d1805'
SESSION_APPROVED_EDITION = '066abc50787fe3f83fd9d7fcaf33451336ecb054'
PRODUCT_BOOTSTRAP_APPROVED_EDITION = '569a288195e4cfee9e8876f34cf485dd042b94f6'
LIST_LAYOUT_APPROVED_EDITION = '13db0fe4b975b3e4cc331525357da5e3d9d51315'
MODEL_TRANSFER = 'illustration-2026-model-transfer'
MODEL_UNPACK = 'illustration-2026-model-moving-unpack'
MODEL_MOVING_PAGES = {MODEL_TRANSFER: 65, MODEL_UNPACK: 67}
REPOSITORY_PAGES = {'illustration-expansion-2026-repository-implementation': 90, 'revision-di-remote': 92}
SERVICE_FIGURES = {'illustration-2026-service-'+name for name in
                   ('interface', 'implementation', 'dispatch', 'call-chain')}
DI_INTRO = 'illustration-figure-cards-2026-di-remote-intro'
MANAGED = 'illustration-expansion-2026-boot-managed-versions'
BEAN = 'illustration-expansion-2026-bean-auto-configuration'
REMOVED_MANAGED_ASSET = 'docs/textbook/chapters/01/assets/revision-ill-boot-managed-versions.png'
FORM = 'illustration-expansion-2026-form-name-binding'
REPOSITORY = 'illustration-2026-repository-results'
EACH = 'illustration-review-v4-each-variable-key'
REMOVED_REPOSITORY_ASSET = 'docs/textbook/chapters/03/assets/revision-ill-repository.png'
FORM_OBJECT = 'illustration-2026-form-object-binding'
NULL_BLANK = 'illustration-expansion-2026-null-blank-constraints'
REMOVED_NULL_BLANK_ASSET = 'docs/textbook/chapters/04/assets/revision-ill-null-blank-constraints.png'


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
        self.assertEqual(len(data['new']), 35+len(SERVICE_FIGURES))
        figure_ids = {r['figure_id'] for r in data['new']}
        self.assertTrue((SERVICE_FIGURES | {FORM_OBJECT}) <= figure_ids)
        self.assertNotIn(NULL_BLANK, figure_ids)
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
                        elif (record['figure_id'].startswith('illustration-2026-')
                              and record['figure_id'] not in SERVICE_FIGURES | {FORM_OBJECT}):
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
        allowed.update({REMOVED_REPOSITORY_ASSET, REMOVED_NULL_BLANK_ASSET})
        allowed.update({
            'docs/textbook/chapters/05/assets/p181-f13-template.svg',
            'docs/textbook/chapters/05/assets/p185-f16-template.svg',
            'docs/textbook/chapters/07/assets/p258-f16-clean.svg',
            'docs/textbook/chapters/appendix-b/assets/p294-f05.svg',
        })
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
        _,nodes,figures,pages,config=edition_chapter('03',REPOSITORY_APPROVED_EDITION)
        previous_catalog=edition_json('docs/textbook/illustrations.json',MODEL_APPROVED_EDITION)
        data=edition_json('docs/textbook/illustrations.json',REPOSITORY_APPROVED_EDITION)
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
        changed=subprocess.run(command+['diff','--name-only','--no-renames',MODEL_APPROVED_EDITION,
            REPOSITORY_APPROVED_EDITION,'--',*paths],cwd=ROOT,check=True,capture_output=True,encoding='utf-8')
        prefix='docs/textbook/chapters/03/'
        allowed={prefix+'chapter.md'}|{prefix+r['asset'] for r in records}
        self.assertEqual(set(changed.stdout.splitlines()),allowed|{'docs/textbook/illustrations.json'})


    def test_service_revision_preserves_unaffected_source_content(self):
        indentation_ids = set(('p091-b06 p094-b02 p096-b03 p096-b08 p097-b09 p100-b03 p100-b08 '
                               'p101-b05 p108-b04 p111-b02 p117-b03 p119-b03 p128-b06').split())

        def without_indent(value, continuation=False):
            value = re.sub(r'(?m)^[ \t]*(\d+:)?[ \t]*', lambda m: m[1] or '', value)
            return re.sub(r'\n(?!\d+:)', ' ', value) if continuation else value

        for name in ('02', '03'):
            _, old_nodes, old_figures, old_pages, _ = edition_chapter(name, REPOSITORY_APPROVED_EDITION)
            _, nodes, figures, pages, _ = edition_chapter(name, SERVICE_APPROVED_EDITION)
            expected_ids = set(old_nodes) - ({'p115-b05'} if name=='03' else set())
            self.assertEqual(set(old_nodes) & set(nodes), expected_ids)
            for ident in expected_ids:
                if name=='03' and ident in indentation_ids:
                    before, after = old_nodes[ident], nodes[ident]
                    self.assertEqual({k:v for k,v in before.items() if k not in {'text','parts'}},
                                     {k:v for k,v in after.items() if k not in {'text','parts'}}, ident)
                    continuation = ident=='p101-b05'
                    self.assertEqual([(without_indent(value, continuation), style) for value,style in before['parts']],
                                     [(without_indent(value, continuation), style) for value,style in after['parts']], ident)
                elif name!='03' or ident not in {'p115-b04','p126-b16','p131-b04'}:
                    self.assertEqual(nodes[ident], old_nodes[ident], ident)
            allowed_figures = SERVICE_FIGURES if name=='03' else set()
            self.assertEqual(set(figures) - set(old_figures), allowed_figures)
            self.assertEqual({i: figures[i] for i in old_figures}, old_figures)
            existing_ids = expected_ids | set(old_figures)
            source_order = lambda order: {p['source_page']:[i for i in p['entries'] if i in existing_ids]
                                          for p in order}
            expected_order = source_order(old_pages)
            if name=='02':
                moved = ['p059-b04','p059-b05','p059-b06']
                index = expected_order[58].index('p058-b05') + 1
                expected_order[58][index:index] = moved
                for ident in moved:
                    expected_order[59].remove(ident)
            else:
                merged = old_nodes['p115-b04']['text']+old_nodes['p115-b05']['text']
                self.assertEqual(re.sub(r'\s+', '', merged), re.sub(r'\s+', '', nodes['p115-b04']['text']))
                self.assertEqual(nodes['p126-b16']['text'], old_nodes['p126-b16']['text'])
                self.assertEqual(nodes['p131-b04']['kind'], 'heading')
            self.assertEqual(source_order(pages), expected_order, name)

        path = 'docs/textbook/illustrations.json'
        previous = edition_json(path, REPOSITORY_APPROVED_EDITION)
        expected_records = [dict(r, before_id='p059-b07') if r['figure_id']==MODEL_TRANSFER else r
                            for r in previous['new']]
        approved_catalog = edition_json(path, SERVICE_APPROVED_EDITION)
        self.assertEqual({**approved_catalog, 'new': [r for r in approved_catalog['new'] if r['figure_id'] not in SERVICE_FIGURES]},
                         {**previous, 'new': expected_records})

        path = 'tools/textbook/code_explanations.json'

        def without_explanation_indent(data):
            for record in data:
                if record['chapter']!='03':
                    continue
                for row in record['rows']:
                    sources = row['code_line_sources']
                    if any(line['code_id'] in indentation_ids for line in sources):
                        row['code'] = without_indent(row['code'])
                        for line in sources:
                            if line['code_id'] in indentation_ids:
                                line['text'] = without_indent(line['text'])
            return data

        current_explanations = deepcopy(edition_json(path, SERVICE_APPROVED_EDITION))
        split = next(i for i,record in enumerate(current_explanations)
                     if (record['chapter'], record['anchor_id'])==('03', 'p129-b01'))
        first, second = current_explanations[split:split+2]
        self.assertEqual(first['consume_ids'], [f'p129-b{i:02d}' for i in range(1,6)])
        self.assertEqual(second['consume_ids'], [f'p129-b{i:02d}' for i in range(6,10)])
        self.assertEqual(second['anchor_id'], 'p129-b06')
        for key in ('chapter', 'owner_code_ids', 'source_pages'):
            self.assertEqual(first[key], second[key], key)
        current_explanations[split:split+2] = [dict(
            first, consume_ids=first['consume_ids']+second['consume_ids'],
            rows=first['rows']+second['rows'], source_texts=first['source_texts']|second['source_texts'])]
        self.assertEqual(without_explanation_indent(current_explanations),
                         without_explanation_indent(deepcopy(edition_json(path, REPOSITORY_APPROVED_EDITION))))

        paths = ['docs/textbook/chapters','docs/textbook/illustrations.json',path,'tools/textbook/filename_labels.json']
        command = ['git','-c','safe.directory='+ROOT.as_posix()]
        result = subprocess.run(command+['diff','--name-only','--no-renames',REPOSITORY_APPROVED_EDITION,
            SERVICE_APPROVED_EDITION,'--',*paths],cwd=ROOT,check=True,capture_output=True,encoding='utf-8')
        changed = set(result.stdout.splitlines())
        required = {'docs/textbook/chapters/'+n+'/chapter.md' for n in ('02','03')}
        required.update('docs/textbook/chapters/03/'+r['asset'] for r in approved_catalog['new'] if r['figure_id'] in SERVICE_FIGURES)
        required.update({'docs/textbook/illustrations.json',path})
        configs = {'docs/textbook/chapters/'+n+'/source.json' for n in approved_catalog['reviewed_chapters']}
        self.assertTrue(required<=changed<=required|configs, changed^required)

        for relative in changed & configs:
            current = deepcopy(edition_json(relative, SERVICE_APPROVED_EDITION))
            previous = deepcopy(edition_json(relative, REPOSITORY_APPROVED_EDITION))
            for settings in (current, previous):
                typography = settings.get('typography',{})
                typography.pop('minor_heading_extra_space',None)
                if not typography:
                    settings.pop('typography',None)
            if relative == 'docs/textbook/chapters/03/source.json':
                for ident in SERVICE_FIGURES:
                    self.assertIn(ident, current['illustrations'])
                    current['illustrations'].pop(ident)
                continuations = current['pagination']['continue_before']
                self.assertEqual(continuations.pop('87'), 'short-minor-heading')
                self.assertIn(continuations.pop('129', None), (None, 'continued-prose'))
            self.assertEqual(current, previous, relative)


    def test_session_revision_preserves_unaffected_source_content(self):
        from html_components import source_rows

        _, old_nodes, old_figures, old_pages, _ = edition_chapter('03', SERVICE_APPROVED_EDITION)
        _, nodes, figures, pages, _ = edition_chapter('03', SESSION_APPROVED_EDITION)
        expected_caption = old_nodes['revision-di-caption']['text'].split('テレビが替わっても')[0].rstrip()
        self.assertEqual(nodes['revision-di-caption']['text'], expected_caption)
        self.assertEqual({k:v for k,v in nodes.items() if k!='revision-di-caption'},
                         {k:v for k,v in old_nodes.items() if k!='revision-di-caption'})
        self.assertEqual((figures,pages), (old_figures,old_pages))

        _, old_nodes, old_figures, old_pages, _ = edition_chapter('04', SERVICE_APPROVED_EDITION)
        _, nodes, figures, pages, _ = edition_chapter('04', SESSION_APPROVED_EDITION)
        codes = {'p147-b04','p149-b05','p150-b03','p151-b03','p151-b07','p155-b08','p156-b02','p156-b04'}
        credentials = {'p141-b04','p146-b04'}
        removed = {NULL_BLANK+'-caption'} | {'revision-messages-'+name for name in
                   ('settings','settings-note','java','controller')}
        self.assertEqual(set(old_nodes)-set(nodes), removed)
        self.assertEqual(set(nodes)-set(old_nodes), {FORM_OBJECT+'-caption'})
        session_figure = 'illustration-expansion-2026-model-session-lifetime'
        edited = codes | credentials | {'p152-b07','p152-b08','p152-b09',session_figure+'-caption'}
        ignored = edited | removed | {i for i in old_nodes if i.startswith('revision-messages-')}
        self.assertEqual({i:nodes[i] for i in old_nodes if i not in ignored},
                         {i:old_nodes[i] for i in old_nodes if i not in ignored})
        for ident in credentials:
            self.assertEqual(nodes[ident]['text'], old_nodes[ident]['text'], ident)
            self.assertEqual(nodes[ident]['attrs'], {**old_nodes[ident]['attrs'], 'keep-lines':'true'}, ident)
        for ident in codes:
            before, after = [source_rows(record,ident) for record in (old_nodes[ident],nodes[ident])]
            self.assertEqual([r['number'] for r in before], [r['number'] for r in after], ident)
            tokens = lambda rows: re.findall(r'"(?:\\.|[^"\\])*"|\w+|[^\w\s]',
                                            '\n'.join(r['code'] for r in rows))
            self.assertEqual(tokens(before), tokens(after), ident)
        self.assertEqual({k:v for k,v in figures.items() if k!=FORM_OBJECT},
                         {k:v for k,v in old_figures.items() if k!=NULL_BLANK})
        movable = removed | {NULL_BLANK,FORM_OBJECT,FORM_OBJECT+'-caption'} | {
                  i for i in old_nodes if i.startswith('revision-messages-')}
        order = lambda values: [(p['source_page'], [i for i in p['entries'] if i not in movable])
                                for p in values]
        self.assertEqual(order(pages), order(old_pages))


    def test_product_and_bootstrap_revision_preserves_other_source_content(self):
        indents = {'05': ('p172-b01','p174-b02'), '06': ('p205-b04','p214-b05'), '07': ()}
        line_breaks = {
            '05': (),
            '06': ('p204-b05','p204-b07','p215-b02','p215-b03','p225-b06','p225-b07',
                   'p225-b08','p226-b06','p226-b07','p226-b08'),
            '07': ('p240-b03','p240-b04','p240-b05'),
        }
        other_edits = {
            '05': {'p189-b01'},
            '06': {'p197-table01','p197-table02','p200-b04','p200-b05','p230-b01','p235-b05'},
            '07': {'p243-b08'},
        }
        final_note = 'revision-product-final-note'
        for name in indents:
            with self.subTest(chapter=name):
                _, old_nodes, old_figures, old_pages, old_config = edition_chapter(name, SESSION_APPROVED_EDITION)
                _, nodes, figures, pages, config = edition_chapter(name, PRODUCT_BOOTSTRAP_APPROVED_EDITION)
                expected_pages, expected_config = deepcopy(old_pages), deepcopy(old_config)
                added, removed = set(), set()
                if name=='05':
                    expected_config['pagination']['continue_before'].update({'177':'continued-prose','189':'continued-code'})
                    self.assertEqual(nodes['p189-b01'],dict(old_nodes['p189-b01'],language='css'))
                if name=='06':
                    added = {final_note}
                    obsolete = next(p for p in expected_pages if p['source_page']==232)
                    removed.update(obsolete['entries'])
                    obsolete['entries'].clear()
                    entries = next(p['entries'] for p in expected_pages if p['source_page']==200)
                    pos = entries.index('p200-b04')+1
                    entries.insert(pos,final_note)
                    expected_config['pagination']['omit_blank_pages'] = [232]
                    self.assertRegex(nodes['p200-b05']['text'],r'Integer[ \u00a0]categoryId')
                    self.assertEqual(normalized(nodes['p200-b05']['text']),normalized(old_nodes['p200-b05']['text']))
                    self.assertEqual(nodes['p230-b01']['text'],'【参考】'+old_nodes['p230-b01']['text'])
                    self.assertEqual(nodes['p235-b05'],dict(old_nodes['p235-b05'],kind='heading'))
                    for ident,attribute in [('p197-table01','highlight-row'),('p197-table02','highlight-column')]:
                        attrs = {**old_nodes[ident]['attrs'],attribute:'4'}
                        self.assertEqual(nodes[ident],dict(old_nodes[ident],attrs=attrs),ident)
                    original_code = old_nodes['p200-b04']['text']
                    supplemented = nodes['p200-b04']['text']
                    self.assertTrue(supplemented.startswith(original_code+'\n'))
                    snippet = supplemented[len(original_code):].lstrip('\n')
                    self.assertTrue(all(line.startswith('//') for line in snippet.splitlines() if line))
                    for value in ('@ManyToOne','insertable = false, updatable = false','private Category category;',
                                  '@Column(name = "category_id")','private Integer categoryId;'):
                        self.assertIn(value,snippet)
                    self.assertIn('作業手順⑤',nodes[final_note]['text'])
                if name=='07':
                    old_css = 'color: white;\n        padding: 10px 20px;\n        border: none;\n        border-radius: 5px;'
                    short_css = 'color: white; /* ほかに padding や border などを指定 */'
                    self.assertEqual(nodes['p243-b08']['text'],old_nodes['p243-b08']['text'].replace(old_css,short_css))
                self.assertEqual((figures,pages,config),(old_figures,expected_pages,expected_config))
                self.assertEqual(set(nodes)-set(old_nodes),added)
                self.assertEqual(set(old_nodes)-set(nodes),removed)
                bullets = {i for i in old_nodes if name in ('06','07') and '•' in old_nodes[i]['text']}
                edited = set(indents[name]) | set(line_breaks[name]) | other_edits[name] | bullets
                self.assertEqual({i for i in set(old_nodes)&set(nodes) if nodes[i]!=old_nodes[i]},edited)
                for ident in indents[name]:
                    prior = old_nodes[ident]['text'].replace('prodRepo..findById','prodRepo.findById')
                    without_indent = lambda value: [line.lstrip() for line in value.splitlines()]
                    self.assertEqual(without_indent(nodes[ident]['text']),without_indent(prior),ident)
                for ident in bullets | set(line_breaks[name]):
                    text = old_nodes[ident]['text'].replace('•','●')
                    attrs = old_nodes[ident]['attrs']
                    if ident in line_breaks[name]:
                        attrs = {**attrs,'keep-lines':'true'}
                    self.assertEqual(normalized(nodes[ident]['text']),normalized(text),ident)
                    self.assertEqual(nodes[ident]['attrs'],attrs,ident)
                    self.assertNotIn('•',nodes[ident]['text'],ident)


    def test_list_layout_revision_preserves_other_source_content(self):
        numbered = {'p242-b09','p242-b10','p242-b11','p242-b12'}
        bootstrap_breaks = {
            'p251-b02','p252-b03','p254-b03','p255-b01','p255-b04','p257-b02','p257-b03',
            'p259-b03','p260-b04','p261-b03','p262-b04','p275-b07','p275-b08',
            'p276-b05','p276-b06','p276-b07','p276-b08',
        }
        for name, edited, removed in (
            ('06', {'p217-b05'}, set()),
            ('07', numbered | bootstrap_breaks | {'p242-b08'}, {'p242-b13'}),
        ):
            with self.subTest(chapter=name):
                _, old_nodes, old_figures, old_pages, old_config = edition_chapter(name, PRODUCT_BOOTSTRAP_APPROVED_EDITION)
                _, nodes, figures, pages, config = edition_chapter(name, LIST_LAYOUT_APPROVED_EDITION)
                expected_pages = deepcopy(old_pages)
                for page in expected_pages:
                    page['entries'] = [i for i in page['entries'] if i not in removed]
                if name=='07':
                    old_config = deepcopy(old_config)
                    old_config['pagination']['continue_before']['277'] = 'short-minor-heading'
                    old_config['pagination']['figure_scales']['p260-f18'] = .95
                self.assertEqual((figures,pages,config),(old_figures,expected_pages,old_config))
                self.assertEqual(set(nodes),set(old_nodes)-removed)
                self.assertEqual({i for i in nodes if nodes[i]!=old_nodes[i]},edited)
                for ident in edited:
                    node, prior = nodes[ident], old_nodes[ident]
                    self.assertEqual(node['kind'],'paragraph',ident)
                    if name=='06':
                        self.assertEqual(node['attrs'],prior['attrs'],ident)
                        self.assertNotIn('\n',node['text'])
                        self.assertLess(len(node['text']),len(prior['text']))
                        continue
                    if ident=='p242-b08':
                        self.assertEqual(node['parts'],[(text,'s015') for text,_ in prior['parts']])
                        self.assertEqual(node['attrs'],prior['attrs'])
                        continue
                    expected_text = prior['text']
                    if ident in numbered:
                        lead, _, body = prior['text'].partition('\n')
                        if ident=='p242-b12':
                            body = old_nodes['p242-b13']['text']
                        expected_text = lead.rstrip(':：')+'\n'+body
                        self.assertEqual({style for text, style in node['parts'] if text.strip()},
                                         {'s009','s015'},ident)
                    self.assertEqual(normalized(node['text']),normalized(expected_text),ident)
                    self.assertEqual(node['attrs'],{**prior['attrs'],'keep-lines':'true'},ident)


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

    def test_previously_approved_figures_keep_their_recorded_page_numbers(self):
        assembly = edition_json('output/pdf/textbook/textbook/checks.json', REPOSITORY_APPROVED_EDITION)
        chapter_starts = {p['chapter']: p['flow_pages'][0] for p in assembly['chapters']}
        for name, expected_pages in [('02', MODEL_MOVING_PAGES), ('03', REPOSITORY_PAGES)]:
            checks = edition_json(f'output/pdf/textbook/chapter-{name}/checks.json', REPOSITORY_APPROVED_EDITION)
            starts = {m['id']: m['page'] for m in checks['flow']['block_positions'] if m['edge']=='start'}
            for ident, expected in expected_pages.items():
                self.assertEqual(chapter_starts[name]+starts[ident]-1, expected, ident)

    def test_image_dimensions_and_caption_are_kept_on_one_physical_page(self):
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
