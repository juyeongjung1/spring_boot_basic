# HTMLカード刷新に伴う回帰テスト

結果：pass。担当4スイート計31件。

| スイート | 件数 | 結果 |
| --- | ---: | --- |
| html-components | 9 | pass |
| pipeline | 8 | pass |
| pagination | 7 | pass |
| source-layout | 7 | pass |

## 変更箇所

- `test_html_components.py`：新設9件。46組/84行/163原稿IDの文字単位roundtrip、重複consume0、コード実行番号一致、filename画像5件、MD attrs、実HTML/PDF、行境界分割、コメント緑と太字、空行、過大行/横はみ出し停止。
- `test_pipeline.py`：HTML表ではTypst table-header markerが出ないため、manifestの各partの実PDFから列名/内容ヘッダーを検査。追加本文18件と表80行がそれぞれ一度だけ出ることも維持/追加。
- `test_source_layout.py`：許可済みJPA1/DI2/messages14/errors9の追加だけを認め、原文/図ID欠落を禁止。HTML manifestの変換対象だけ新カードの検査へ切替。対象外図版の元x/y/高さ、固定配置、スライド、動作確認見出しを維持。
- `test_pagination.py`：付録Bの許可されたrevision-errors9IDとp291-b06/b07/b08訂正だけを許容。他の既存原文/図ID・SVG外寸・版名以外の差分禁止を維持。
- `render_components.cjs`：th/td/pre.source-codeのscrollWidth > clientWidth+2pxを最終DOMで検出し、カードID/原稿ID付きエラーで停止。CSS変更なし。

## 旧検査から変更する根拠

- 追加IDをJPAの1件に限る旧条件は、今回許可されたDI図/説明・messages・errorsを誤検出するため厳密なID集合へ更新。
- 旧黄色背景#FFFBF0/黒枠0.48pt/旧赤ラベル枠を固定する条件は新しい白カードに適用できない。コードの元枠の左端・幅と紙面内収まり、右上filenameの実文字を確認する。
- 旧表フォント/原幅/0.65pt線の固定は、本文幅426.672pt・9.5ptの新表には不適切。原色/強調、列比率とJDBC中央、薄い可視境界を確認する。
- 長い識別子を元11.04ptで一行に限る旧条件は、Consolas10.5ptと折り返し可能な新コードには不適切。識別子全体・新コード書体を確認する。
- ファイル名5図とURL/変換注記2図は文字化のため旧図位置を除外。07の実行結果2図は元SVG参照を保持し同じコードカードへ所属することを確認。任意のconsume図を無条件に除外しない。

## 検出して修正した不具合

- 表trの原稿IDアンカー欠落を検出しrootが修正。
- Pygmentsが末尾改行なしのJavaコメントを黒で出す不具合を検出しrootが改行補完方式へ修正。先頭/末尾空行も保持。

## レンダラーの寸法

Chromeの物理紙面は1 CSS px=0.75pt以内の丸めを実測（例95.52→96.00pt）。DOMアンカーは拡大縮小せずptで返し、Python側がclipして合成。全文字・単頁検査は省略しない。

## 参考欄の短縮

04新規14IDだけを短縮しsettings/controllerをparagraphへ変更。標準/ja/en各2行・HTML1行の4カード、root目視で最新38頁の1ページ枠内に全14IDが収まった。既存本文は変更しない。

ログは同じtmp/modern-2026のregression-*.logへ保存。内容の一次資料とruntime13件の根拠はcontent-report.md/jsonへ記録。最終合冊・コミット・pushはroot担当。
