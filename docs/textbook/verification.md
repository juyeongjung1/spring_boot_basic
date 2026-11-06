# 商標確認・本文字下げ・小型挿絵の追加

2026年11月6日。本文349ページ、演習82ページ。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [最終独立監査](../../output/verification/illustrations-2026/final-audit.md)
- [挿絵と生成プロンプトの一覧](illustrations.md)

## 商標

IIBA®・BABOK®の指定文言は、本文・演習の両冊2ページ目で、CiscoとIntelの間に既に1回ずつありました。原稿・原本情報・実PDF・ページPNGを照合し、通常書体と®/™を確認しました。重複追加は不要でした。

## 本文の字下げ

通常の段落頭を、その先頭書体の全角1文字分下げます。設定だけでは単独段落へ効いていなかった問題を、共通paragraphの明示的な終端で修正しました。行送り18pt・段落境界24ptは維持します。原稿中の手動空白は表示時だけ整理し、二重字下げを防ぎます。

見出し・箇条書き・URL・注記・演習時間一覧・図のキャプションは区別します。演習の確定した3つの継続断片は、元の文字とIDを保って、表示上だけ前の文と同じ段落へつなぎます。例えば「プ」「ログラム」が別段落にならないようにしています。

- [全章の実測記録](../../output/verification/illustrations-2026/indent-audit.md)
- [商標確認記録](../../output/verification/illustrations-2026/trademark-audit.md)

## 挿絵

全19章と既存図を調べ、Maven・Model・Repository・セッション・入力チェック・共通レイアウト・外部キー・レスポンシブ配置・エラー調査に新規9図を挿入しました。既存DI図も縮小しています。新図は幅280pt（約9.9cm）、DIは260pt、全て高さ140pt以内です。図と9.5ptのキャプションは同一ページに保持します。

| 図 | 原本頁 | 現在の本文PDF頁 | 変更前後の画像 |
| --- | ---: | ---: | --- |
| pom.xmlの指定から必要なライブラリをそろえる | 28 | 28 | [表示](../../output/verification/illustrations-2026/pages/maven-libraries-comparison.png) |
| Modelを使ったデータの受け渡し | 58 | 63 | [表示](../../output/verification/illustrations-2026/pages/model-transfer-comparison.png) |
| Repositoryの返り値はリストと0/1件で異なる | 90 | 106 | [表示](../../output/verification/illustrations-2026/pages/repository-results-comparison.png) |
| 識別IDとサーバー側のセッション保存 | 142 | 170 | [表示](../../output/verification/illustrations-2026/pages/session-separation-comparison.png) |
| 入力チェックの成功とエラーの分岐 | 148 | 177 | [表示](../../output/verification/illustrations-2026/pages/validation-branch-comparison.png) |
| 共通レイアウトと画面ごとの内容を組み合わせる | 181 | 217 | [表示](../../output/verification/illustrations-2026/pages/layout-reuse-comparison.png) |
| DBの外部キー値とJavaのオブジェクト参照 | 201 | 241 | [表示](../../output/verification/illustrations-2026/pages/foreign-key-reference-comparison.png) |
| 横幅によって左右配置から上下配置へ切り替わる | 269 | 316 | [表示](../../output/verification/illustrations-2026/pages/responsive-switch-comparison.png) |
| 外側の例外から原因と自分のコードをたどる | 291 | 343 | [表示](../../output/verification/illustrations-2026/pages/error-cause-chain-comparison.png) |
| 依存性の注入 | 80 | 93 | [表示](../../output/verification/illustrations-2026/pages/di-remote-comparison.png) |

## 最終検証

- 回帰テスト57件が合格。全19章の文字照合・はみ出し・孤立見出し・図/コード/手順の分断検査も合格。
- 原本373ページ、空白17ページ、既存2879 IDを保ち、新規図とキャプション18 IDを加えた2897 IDを独立監査。既存本文・コード・表・書式Span・図の参照・順序は不変。
- 合冊後の全431ページのヘッダー・元頁所属・章別からの本文一致、URI89件を照合。
- 新9図とDIの全10図を実PDFで目視し、寸法・キャプション同頁・小型表示の可読性を確認。既存スライド65点は変更前の同領域と全画素一致。
- 生成画像内の文字と矢印は目視確認。Bootstrapの追加図は画面幅による配置切替の模式図で、厳密な列幅は既存の12列図とコードで説明する。
- 原本PDF/Word、baseline、source-layout、既存資材は保全。Java 21・Boot 4.0.2の配布プロジェクトとZIPは今回変更していない。

詳細：[画像の小型レビュー](../../output/verification/illustrations-2026/generated-small-review.md)、[実PDFの目視](../../output/verification/illustrations-2026/final-visual-review.md)。前回のHTML/CSS化の検証はoutput/verification/modern-2026に保持しています。
