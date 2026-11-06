# 難しい概念を補うイラスト24点の追加

2026年11月6日。本文364ページ、演習82ページ。前版の本文349ページから15ページ増えました。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [追加位置・画像・生成記録の一覧](illustrations.md)
- [正確な生成プロンプトと配置カタログ](illustrations.json)
- [最終独立監査](../../output/verification/illustrations-expansion-2026/final-audit.md)

## 追加内容

第1〜7章へ24点を追加し、前回9点と既存DI図を合わせて34点にしました。図は幅280pt（約9.9cm）・高さ140pt以内、DIは幅260ptです。短い大きなラベルで関係を示し、本文は書き換えず図と短いキャプションだけを追加しました。

| 章 | 追加数 | 主な内容 |
| --- | ---: | --- |
| 1 | 3 | 共通基盤、管理対象バージョン、Beanの自動設定 |
| 2 | 4 | リクエストと応答、GET/POST、nameとForm、Modelのキーとフィールド |
| 3 | 3 | Repositoryの宣言と実装、検索メソッド名、redirectの新規リクエスト |
| 4 | 3 | Model/Sessionの保持期間、入力エラーの再表示、null・空文字・空白 |
| 5 | 3 | th:text、動的URLとID、staticの保存先と公開URL |
| 6 | 5 | mappedBy/JoinColumn、null参照、表示名と送信値、JPQL、GROUP BY/DTO |
| 7 | 3 | CDN/static、margin/padding、container/row/colの包含 |

## 図の確認

生成には組み込みimage_genを使いました。全24点を原寸と印刷相当の560px表示で二重確認し、技術的な意味、綴り、数値、矢印、文字の可読性を確認しました。Form属性の引用符、Repositoryの文字サイズ、redirectの応答表示を調整し、商品の絵も配布DBへ合わせました。

- [生成画像の第二者レビュー](../../output/verification/illustrations-expansion-2026/second-review.md)
- [実PDFの全34図レビュー・比較画像](../../output/verification/illustrations-expansion-2026/final-visual-review.md)

原本の操作説明・画面・ページ区切りを優先し、元22pのバージョン管理図は本文24pの図中心の継続ページにしています。図の大きさは約99×41mmで、原本の説明と画面を分断していません。

## 改ページと原本保全

スライド上段の固定配置を維持し、本文用の図とキャプションはMarkdownの挿入順を保つようにしました。全33図の前後アンカー順も実PDFで検査します。コード導入の短いラベルと直後の説明は、最初のコード枠と同じページに保ちます。

- 回帰テスト65件が合格。全19章の文字照合・はみ出し・孤立見出し・図/表/短いコード/手順の分断検査も合格しました。
- 前版の2897 IDに、図24・キャプション24の48 IDだけを追加し、計2945 IDを確認しました。
- 元資材739点、baseline/layout38件、既存本文・コード・表・Span・図行・順序・元頁所属を保全しました。
- 原本373ページ、空白17ページ、合冊446ページのヘッダー・ページ境界、URI89件、章から合冊への全文一致を監査しました。
- 既存スライド65点は原位置と描画領域の全画素が前版と一致。固定配置の【】24組、コードの右上ファイル名も保持しました。

[全テスト記録](../../output/verification/illustrations-expansion-2026/regressions.json)と[最終PDFのSHA256](../../output/verification/illustrations-expansion-2026/summary.json)を保存しました。前回の括弧・太字・ファイル名の検証は[brackets-2026](../../output/verification/brackets-2026/final-audit.md)に保持しています。
