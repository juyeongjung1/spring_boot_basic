# 教材のMarkdown管理とPDF生成

本文教材の第1〜7章・前付・付録A/Bと、演習ガイドの全章・前付・奥付をMarkdownへ移しました。元PDFは本文296ページ、演習77ページです。本文と演習のコード・実習手順をJava 21・Spring Boot 4.0.2・Pleiades 2025向けに改訂しました。更新版プロジェクトはリポジトリ直下の `projects/` です。

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
| `collections.json` | 二冊の章順・目次ページと、本文の索引・印刷配置の設定 |
| `index.md` | 巻末索引の用語・読み・参照する原稿のブロックID |
| `../../tools/textbook/book.typ` | 全章共通の余白・書体・見出し・本文・表・コード・図版の組版規則 |
| `../../tools/textbook/html_components.py` | コード・表・構文解説のHTML作成と文字付きPDF部品の合成 |
| `../../tools/textbook/components.css` | 白基調のコード・表・構文解説の共通CSS |
| `../../tools/textbook/render_components.cjs` | Edge/Playwrightによる実測・行境界分割・PDF生成 |
| `../../tools/textbook/code_explanations.json` | 行番号付き解説と元文章・該当コード・出典IDの対応 |
| `../../tools/textbook/filename_labels.json` | 画像だけのファイル名を文字ヘッダーへ統合する対応 |

本文・見出し・手順・コード・通常の表は文字として保持しています。スライド、操作画面、図解はSVGへ切り出し、矢印・吹き出しを含めて保持しています。スライド内の表は図版の一部です。Wordに埋め込まれていた `.sldx` 原本も保存しています。

## 生成するPDF

全体版は `output/pdf/textbook/textbook/` と `output/pdf/textbook/exercise/` にあります。

| ファイル | 内容 |
| --- | --- |
| `reference.pdf` | 元位置再現版。baseline.mdから改訂前の文字位置を再現する比較用の版（記号は単色化） |
| `flow.pdf` | 改訂版。chapter.mdのJava 21・Boot 4.0.2向け本文を自動組版する版。本文教材には巻末索引を収録 |
| `comparison.pdf` | 左が元PDF、右が元位置再現版の全ページ比較 |
| `checks.json` | 収録範囲、章の対応、目次・索引の番号とリンク先の記録 |

章単位の成果物は `output/pdf/textbook/chapter-識別子/` にあります。三種類のPDF、全ページの重ね合わせ画像 `pNNN-overlay.png`、差分画像 `pNNN-difference.png`、文字・画素・改ページの `checks.json` を保存しています。

元位置再現版は `baseline.md` と取り込み時の位置情報から生成し、改訂版は `chapter.md` から生成します。本文全体を画像にしたものではありません。baselineはSHA256で検証し、改訂した文章へ古い位置情報を流用しません。同じコマンドで比較用の版と現在の改訂版を生成できます。

## 自動組版のルール

- 原本のsource-pageごとの開始位置を保持します。次ページから始まる内容を前ページへ繰り上げません。文章量が増えた場合はその教材単位の続きページを設け、次の単位は新しいページから開始します。
- 見出しと次の要素、手順・説明・図は離れないように保持します。本文の行送りは18pt、段落境界は24pt（段落下の空き12.96pt）、小見出しの前後は18/12pt、リストの1行項目間は24pt・続き行は18pt、図・表・コードの後は12ptへ統一します。見出しを説明・図と一体にする場合も、上余白18ptを外側で確保します。
- 通常の本文は段落頭を、その先頭書体の全角1文字分下げます。原稿に全角空白を重ねず、組版側で単独段落にも適用します。見出し、箇条書き、時間一覧、URL、注記、前の文章の続きは区別します。挿絵のキャプションは9.5pt・左揃えです。
- 追加挿絵33点と既存DI図の全34点は幅300pt・高さ140pt以内に収め、図とキャプションを同一ページに保持します。配置と生成プロンプトは `illustrations.json`、紙面上の寸法は各章 `source.json` の `illustrations` で管理します。
- スライド65点の上段は原本の位置・幅・高さを保持し、原本にある説明前の罫線も復元します。説明本文は下段から組版します。通常の図版も原本の左端・幅・高さを保持し、中央寄せや本文幅への縮小を加えません。
- 本文用の小型挿絵とキャプションはMarkdownで指定した文章の間へ置き、スライドのあるページでも末尾へ並べ替えません。図の前後関係も実PDFの座標で検査します。
- 通常の表はHTML/CSSで本文幅に揃え、元の背景・文字色・太字・下線・横揃え・列幅の比率を保持します。文字は9.5pt、セル余白は5ptとし、数値の途中改行を防ぎます。スライド内の表は図版の一部です。
- コードは白背景のHTML/CSSカードへ統一し、左上に言語名、右上にファイル名、左側に行番号を配置します。ファイル名はMeiryoの実太字・濃青・下線・淡青ラベルで強調します。元のコード枠の幅・左端と、同一枠の複数code IDのまとまりは保持します。空行・インデントを保持し、コメントは緑 #008000 にします。画像だけのファイル名5件も文字へ統合します。接続URLとModelMapperの変換方向は注記へ整理し、旧画像の文字をコードに重ねません。
- 行番号付きの構文解説は、行番号と該当コードを全幅の枠に置き、その下へ元の説明文を通常の段落で表示します。本文はP明朝、元からの強調箇所はPゴシックの太字に統一します。字号・色とWordの段落・明示改行を保持し、先頭文への自動強調は加えません。Edgeが印刷時に落とす擬似太字は、文字を重複させずPDFの文字描画で補います。
- Javaのアノテーションは赤、HTMLの要素名は青、Thymeleafの`th:`属性は紫で表示します。コメントは緑、ファイル名は右上の太字・下線付き表示を保ちます。
- スライド以外の独立図は番号と枠で区切り、挿絵の説明文も同じ枠内へ収めます。本文の図番号は「章.節.連番」、付録・演習は識別用の接頭辞を付けます。元の画面図の左端と画像幅は保持します。
- HTML部品はEdgeで実測し、620ptを超える場合はコード行・表の行・説明項目の境界で分割します。続きの部品にもファイル名・見出しを再掲します。1行が高さに収まらない場合やセル内で文字が横にはみ出す場合は生成を停止します。
- 箇条書きの360箇所を通常の■・●・•へ正規化し、MS Gothicで描画します。絵文字フォントへ代替しません。
- 本文の「」・『』・全角（）は全角幅の書体で組みます。【】は元の比例書体の字送りを保ち、括弧だけ別の書体や全角幅へ置換しません。内側の手動空白は書式の境界をまたいで整理し、外側の空白は保持します。元位置の固定描画では、単字の【に幅・高さ0の非文字要素を前置して行頭約物の圧縮を防ぎ、文字や空白を加えず原本の字位置を維持します。
- 表の罫線は0.6pt・#d7dde5へ統一します。URLは折り返し先も同じ宛先のPDFリンクとなり、Markdownの名前付きリンクも保持します。
- 12pt・ゴシック・太字の独立した小見出しは `.heading` とします。「動作確認」のような独立ラベルも見出しとして前18ptの余白を確保し、本文内の部分強調やファイルパスと区別します。
- 小小見出しに分類された12pt以下のMS PGothicで、太字が欠けている部分は共通処理で補強します。既存の太字と大見出しはそのまま保ち、説明文の続きは補強しません。
- ファイルパスとコード冒頭を離さないようにします。Java・XML/HTML・CSSを共通テーマで色分けします。
- 「■」や丸数字で始まる短いコード導入ラベルと直後の説明は、最初のコード枠と同じページに保持します。
- 複雑な前付・目次・章扉・奥付は固定配置を保持します。`cover_mode` と `native_pages` で指定しています。
- ヘッダーは原本の表記を使い、管理用の章名を紙面へ出しません。空白ページは既定で保持します。全体版のページ番号は物理ページと一致させます。元に番号がない固定ページには追加しません。目次の番号とリンクは組版後の位置へ更新します。
- 本文教材の「はじめに」・各章・付録・索引は奇数ページから始めます。合冊時に必要な空白ページを入れ、奥付を最終の偶数ページに配置します。
- 索引は奥付の前に置き、英数字とかな一文字ごとの見出し、二段組み、点線のリーダーで組みます。参照先は `index.md` の章IDとブロックIDで指定し、合冊時に実ページ番号とPDF内リンクを生成します。

改訂版では追加量によってページ数・コードの折り返しが変わります。原本のページ開始とスライド上段の位置は保持します。具体的な比較と制約は [検証報告](verification.md) に記録しています。各章の生成時に `output/html/textbook/章ID.html` へ部品のブラウザープレビューも出力します。これはコード・表・構文解説の確認用で、教材全ページのHTMLではありません。

## 実行手順

Windowsのフォント、Python、Pandoc、Node.js 20以上、Node版Playwright、Microsoft Edgeが必要です。確認済みPandocは3.9.0.2です。フォントはWindowsから作業用フォルダーへ読み込み、Gitには登録しません。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools/textbook/requirements.txt
npm ci --prefix tools/textbook

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
.\.venv\Scripts\python.exe tools/textbook/test_book_index.py
.\.venv\Scripts\python.exe tools/textbook/test_pipeline.py
.\.venv\Scripts\python.exe tools/textbook/test_pagination.py
.\.venv\Scripts\python.exe tools/textbook/test_symbols.py
.\.venv\Scripts\python.exe tools/textbook/test_remaining.py
.\.venv\Scripts\python.exe tools/textbook/test_fidelity.py
.\.venv\Scripts\python.exe tools/textbook/test_source_layout.py
.\.venv\Scripts\python.exe tools/textbook/test_html_components.py
.\.venv\Scripts\python.exe tools/textbook/test_illustrations.py
.\.venv\Scripts\python.exe tools/textbook/test_bracket_headings.py
.\.venv\Scripts\python.exe tools/textbook/test_figure_frames.py
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

`source-page` は原本のページ対応を示します。通常は改ページしますが、続き本文と、前のページが半分以下の場合の小小見出しだけは、`source.json` の `pagination.continue_before` に確認済みの元頁を指定して同じページへ続けます。節・項の見出し、スライド、固定ページ、空白ページの開始は保持します。 確認済みの空白ページは、`pagination.omit_blank_pages` に元頁番号を指定して自動組版から省けます。

同じ文が元頁の境界で切れている場合は `pagination.paragraph_continuations` に隣接IDの組を指定し、表示時に1段落へ戻します。少量の続きが次頁へ押し出される図だけは `pagination.figure_scales` に元図IDと倍率を指定します。倍率は原寸の85%以上、相似縮小とし、画像資材・左端・本文字号は保ちます。指定のない箇所は従来どおりに組版します。通常の表はMarkdownのパイプ表で編集できます。`${...}` は数式へ変換せず、Thymeleafの式として保持します。

固定配置の扉・前付・奥付を編集した場合は、再配置の確認が必要なため自動版でも停止します。これらの専用テンプレート化は今後の改訂対象です。本文・演習の通常ページは自動組版で更新できます。

スライドの内容を大きく改訂する場合は、保存したPPT原本の編集と表示用SVGの更新を行います。版名・年・囲み・コメント色の局所修正は、元図を保全して別SVGへ反映しています。PowerPointからの自動SVG更新は未実装です。本文の文章中に記載したページ参照は手動で更新します。付録Bの原291ページには依頼されたエラー調査の説明を追加し、このページだけ自動組版へ変更しています。画面図は原画像の表示を局所補正したもので、実画面の再撮影ではありません。元SVGは保持しています。

第4章の固定文言・多言語化の参考欄に加え、全19章で小型挿絵34点を利用しています。第1章のDI導入図は倉庫からAクラスへリモコンを渡す関係、Bean図は倉庫に準備されたリモコン本体を示します。管理対象ライブラリの図とそのキャプションは削除しました。[挿絵の一覧](illustrations.md) と [正確な生成プロンプト・配置カタログ](illustrations.json) に保存記録があります。元DI図の生成記録は [こちら](di-illustration-prompt.txt) です。

構文解説を編集するときは、Markdownと `code_explanations.json` の該当行を一緒に更新します。出典断片の全文一致をテストし、対応が古い場合は停止します。`word_paragraph_breaks`・`word_line_breaks`は原Wordの段落境界・明示改行の文字位置です。元のページ所属と原文IDを保ち、見た目の変更で説明が抜けないようにします。
