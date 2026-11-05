# 教材のMarkdown管理とPDF生成

本文教材の第1〜7章・前付・付録A/Bと、演習ガイドの全章・前付・奥付をMarkdownへ移しました。元PDFは本文296ページ、演習77ページです。本文と演習のコード・実習手順をJava 21・Spring Boot 4.0.2・Pleiades 2025向けに改訂しました。更新版プロジェクトはリポジトリ直下の `projects/` です。索引追加は次の工程です。

## 原稿と共通ルール

| ファイル | 用途 |
| --- | --- |
| `chapters/01`〜`07/chapter.md` | 本文教材の編集元 |
| `chapters/front`・`appendix-a`・`appendix-b` | 本文の前付・付録 |
| `chapters/ex01`〜`ex07/chapter.md` | 演習ガイドの編集元 |
| `chapters/ex-front`・`ex-back` | 演習の前付・奥付 |
| 各フォルダーの `assets/` | SVG図版、埋め込みPPT原本、元の線や枠 |
| 各フォルダーの `source.json` | 元教材・ページ・図版範囲・表の行列・固定配置ページ |
| 各フォルダーの `baseline.md` | 元の教材を比較するための改訂前原稿。編集しません |
| 各フォルダーの `source-layout.json` | 元の文字・書式・位置・図版内の文字起こし・出典対応 |
| `collections.json` | 二冊の章順と目次ページ |
| `../../tools/textbook/book.typ` | 全章共通の余白・書体・見出し・本文・表・コード・図版の組版規則 |

本文・見出し・手順・コード・通常の表は文字として保持しています。スライド、操作画面、図解はSVGへ切り出し、矢印・吹き出しを含めて保持しています。スライド内の表は図版の一部です。Wordに埋め込まれていた `.sldx` 原本も保存しています。

## 生成するPDF

全体版は `output/pdf/textbook/textbook/` と `output/pdf/textbook/exercise/` にあります。

| ファイル | 内容 |
| --- | --- |
| `reference.pdf` | 元位置再現版。baseline.mdから改訂前の文字位置を再現する比較用の版（記号は単色化） |
| `flow.pdf` | 改訂版。chapter.mdのJava 21・Boot 4.0.2向け本文を自動組版する版 |
| `comparison.pdf` | 左が元PDF、右が元位置再現版の全ページ比較 |
| `checks.json` | 収録範囲、章の対応、目次番号とリンク先の記録 |

章単位の成果物は `output/pdf/textbook/chapter-識別子/` にあります。三種類のPDF、全ページの重ね合わせ画像 `pNNN-overlay.png`、差分画像 `pNNN-difference.png`、文字・画素・改ページの `checks.json` を保存しています。

元位置再現版は `baseline.md` と取り込み時の位置情報から生成し、改訂版は `chapter.md` から生成します。本文全体を画像にしたものではありません。baselineはSHA256で検証し、改訂した文章へ古い位置情報を流用しません。同じコマンドで比較用の版と現在の改訂版を生成できます。

## 自動組版のルール

- 本文は元ページの境界を外し、文章量に応じて折り返し・改ページします。
- 見出しと次の要素、手順・説明・図は離れないように保持します。
- 図版は分断しません。縦長の図版は本文の高さに収まる大きさへ縮小します。
- 小さい表は一体で保持します。大きい表は行を壊さずに継続し、見出し行を再掲します。
- コードは空行・インデントを保持し、長い識別子も紙面内で折り返します。実寸600pt以内は一体保持、大きいコードは継続します。
- 箇条書きの360箇所を通常の■・●・•へ正規化し、MS Gothicで描画します。絵文字フォントへ代替しません。
- ファイルパスとコード冒頭を離さないようにします。Java・XML/HTML・CSSを共通テーマで色分けします。
- 複雑な前付・目次・章扉・奥付は固定配置を保持します。`cover_mode` と `native_pages` で指定しています。
- 全体版のページ番号は物理ページと一致させます。元に番号がない固定ページには追加しません。目次の番号とリンクは組版後の位置へ更新します。

自動版ではページ数・図の位置・コードの折り返しが変わります。コードに重なる注釈が直下へ移る例もあります。具体的な比較と制約は [検証報告](verification.md) に記録しています。

## 実行手順

Windowsのフォント、Python、Pandocが必要です。確認済みPandocは3.9.0.2です。フォントはWindowsから作業用フォルダーへ読み込み、Gitには登録しません。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools/textbook/requirements.txt

# 二冊の全章を生成・検証して合冊
.\.venv\Scripts\python.exe tools/textbook/build_all.py

# 本文だけ、または演習だけを処理
.\.venv\Scripts\python.exe tools/textbook/build_all.py --collection textbook
.\.venv\Scripts\python.exe tools/textbook/build_all.py --collection exercise

# 原稿編集後は自動版だけ更新・検証・合冊
.\.venv\Scripts\python.exe tools/textbook/build_all.py --mode flow

# 一章だけの生成／合冊だけの更新
.\.venv\Scripts\python.exe tools/textbook/build.py --chapter 03 --mode flow
.\.venv\Scripts\python.exe tools/textbook/assemble.py

# 往復照合・編集・改ページの回帰検証
.\.venv\Scripts\python.exe tools/textbook/test_pipeline.py
```

元位置再現版と比較版には、取り込み時と同じ元PDFが必要です。章ごとの自動組版だけなら元のWord・PDFの再読み込みは不要です。合冊には生成済みの章ごとの比較版も必要です。目次の位置照合には元PDFも参照します。

新しい取り込みでは `source.json` を用意し、図版・表の候補を検出してから目視で確認します。スライド内やコードの強調枠が表候補になるため、検出結果をそのまま採用しません。

```powershell
.\.venv\Scripts\python.exe tools/textbook/discover.py --chapter 02
.\.venv\Scripts\python.exe tools/textbook/import_source.py --chapter 02
```

取り込み済みの原稿は上書きしません。`--force` は元教材からchapter.md・baseline.md・位置情報・図版を作り直すため、改訂済み原稿を失う操作です。

## 原稿の編集と残る制約

`::: {#識別子 .paragraph}` の内側を編集します。`[文章]{.s009}` は元の書式です。識別子は既存の対応を保ち、重複させないでください。段落・見出し・手順・コード・表は `.paragraph`・`.heading`・`.step`・`.code`・`.table` です。

```markdown
::: {#追加した段落 .paragraph}

ここに**重要な説明**を追加します。

:::
```

`source-page` は元の出典を示し、自動版での強制改ページではありません。通常の表はMarkdownのパイプ表で編集できます。`${...}` は数式へ変換せず、Thymeleafの式として保持します。

固定配置の扉・前付・奥付を編集した場合は、再配置の確認が必要なため自動版でも停止します。これらの専用テンプレート化は今後の改訂対象です。本文・演習の通常ページは自動組版で更新できます。

スライドの改訂では、保存したPPT原本を編集し、表示用SVGを更新する必要があります。PowerPointからの自動SVG更新は未実装です。索引追加と本文中のページ参照の自動追従は、別の改訂工程です。Pleiadesの旧画面に含まれる古い設定値は現在の手順へ従い、付録Aのバージョン選択・新規作成・実行の図は改訂した設定図を参照してください。
