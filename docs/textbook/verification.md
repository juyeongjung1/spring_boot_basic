# HTML/CSSによるコード・表・構文解説の改訂

2026年11月5日。本文348ページ、演習82ページ。今回の依頼で許可された表示刷新と、DI挿絵・メッセージ参考欄・エラー調査の追記を反映しました。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [最終独立監査](../../output/verification/modern-2026/final-audit.md)
- [原文とコードの対応検査](../../output/verification/modern-2026/explanations-report.md)

## 表示の変更

- コード186カードを白背景のHTML/CSSで統一。言語名、右上のファイル名、行番号、構文色、緑のコメントを表示します。画像だけのファイル名5件も文字へ統合しました。
- 通常の表32点は本文幅とセル余白を統一。元の背景色・文字色・太字・下線・列幅の比率は保持し、数値の途中改行を防ぎます。
- 構文解説46カード・84表示行は「行番号／該当コード／意味・補足」の3列にしました。原文を省略せず、引数の列挙や跨頁の続きも区別します。
- 長い部品は620ptを上限に行境界で分割。見出し・ファイル名・続き表示を再掲します。DOMと個別PDFの文字、実測した高さ、セル内の横はみ出しを検査します。
- 元のコード枠の幅と左端は保持。画像ラベル・URL定義・ModelMapper矢印は新ヘッダーや注記へ整理し、実行例2図はカード下部へ保持します。通常の図版と65点のスライドは元の左端・寸法、スライド上段の位置を保持します。

## 指定された内容

- 第3章の原80ページに、DIコンテナからリモコンを受け取って使う挿絵と説明を挿入しました。その他の挿絵は [提案一覧](illustration-proposals.md) に記録し、未挿入です。
- 第4章の原161ページ後に、固定文言の集約、標準ファイル、messages_ja.properties・_en・_ko、UTF-8、Locale、ThymeleafとMessageSourceの参考欄を1ページで追加しました。
- 付録Bの原291ページに、Pleiadesのコンソールで例外名・メッセージ・Caused by:・自分のコードの行番号を読む方法を追加しました。404/405/500の区別など、既存の誤記3ブロックも訂正しました。
- メッセージとエラーの例は、配布プロジェクトのBoot 4.0.2依存・Java 21で13項目を実行確認しました。配布プロジェクトは今回変更していません。
- 図内コメント6点を#008000へ局所修正。全268図の校正波線候補を目視し、既知の除去済み図も拡大して確認しました。ModelMapperの旧コード字片は新カードへ重ねません。

## 最終検証

- 全19章で文字照合が一致。見出し孤立、図・短いコード・小表・手順の分断、紙面のはみ出しは0件。
- 原本373ページ、空白17ページ、原本2853 IDを保持。基準版の依存コード1 IDと、今回許可された25 IDを含む2879 IDの所属・順序・元ページ境界を独立検査しました。
- ヘッダー430ページ、URI注釈89件、login3の実リンク、目次番号、章別PDFから合冊への本文を検査しました。
- 回帰テスト49件が合格。代表ページを原本と並べて画像比較し、全46構文解説カードと全32表も目視しました。詳細は下記の記録を参照してください。

## 代表ページの比較

| 対象 | 原本ページ | 改訂版ページ | 比較画像 |
| --- | --- | --- | --- |
| Javaコード | 41 | 41 | [表示](../../output/verification/modern-2026/code-comparison.png) |
| 構文解説 | 59 | 65 | [表示](../../output/verification/modern-2026/explanation-comparison.png) |
| 数値を含む表 | 67 | 76 | [表示](../../output/verification/modern-2026/table-comparison.png) |
| 表の色・下線 | 69 | 79 | [表示](../../output/verification/modern-2026/table-color-comparison.png) |
| 設定ファイル | 71 | 82 | [表示](../../output/verification/modern-2026/properties-comparison.png) |
| DI挿絵 | 80 | 93 | [表示](../../output/verification/modern-2026/di-comparison.png) |
| ModelMapper | 113 | 136 | [表示](../../output/verification/modern-2026/modelmapper-comparison.png) |
| コメント色 | 128 | 152 | [表示](../../output/verification/modern-2026/comment-comparison.png) |
| メッセージ参考 | 161 | 195 | [表示](../../output/verification/modern-2026/messages-comparison.png) |
| 跨頁の解説 | 274 | 323 | [表示](../../output/verification/modern-2026/continuation-comparison.png) |
| エラー原因調査 | 291 | 342 | [表示](../../output/verification/modern-2026/errors-comparison.png) |

## 比較範囲と保全

原本PDF/Word、baseline.md、source-layout.json、元の図版は変更していません。過去版の検証記録はoutput/verification/layout-restore/に保持しています。今回のcode・表・構文解説の表示は新デザインであり、以前の黄色背景やコードの字サイズを完全再現する方針から変更しています。

UI画面やスライド内のコード画像は、注釈や操作の意味を保つため図版として残しています。本文のコードは文字として選択できますが、PDFでカード全体をコピーすると行番号や折り返し改行も含まれることがあります。編集元のMarkdownからはコード本文を取得できます。

索引、本文中のページ参照の自動追従、PowerPointからの自動図版更新は今回の対象外です。章別HTMLは部品の確認用で、全文のHTML版ではありません。
