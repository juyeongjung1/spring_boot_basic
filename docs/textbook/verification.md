# 括弧・小小見出し・コードのファイル名の修正

2026年11月6日。本文349ページ、演習82ページ。改訂前の530b127からページ数は変わっていません。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [最終独立監査](../../output/verification/brackets-2026/final-audit.md)

## 【】と原本の比較

全19章を調べ、原稿中の212ブロック・215組を原本と実PDFに対応付けました。内側の実空白は0件でした。閉じ括弧の外側にある原文の空白103箇所は保持します。

自動組版で【】だけを全角幅の別書体へ置き換えていた処理をやめ、元の比例書体と字送りを使います。さらに、固定座標で1文字ずつ描く大見出しなどでは、組版エンジンが開き括弧を行頭記号として左へ寄せていたため、原本の指定位置に戻します。原稿の文字や既存図版は変更していません。

36pの小見出しの【→参は、原本6.108pt・修正前12pt・修正後6ptです。原本にある微小な字間調整と、自動組版の標準送りは分けて記録しています。図内の輪郭化された文字は文字抽出の対象と区別し、元資材と実PDFの描画の保全を確認します。

- [全【】の対応一覧](../../output/verification/brackets-2026/inventory-final.md)
- [書体・小見出しの確認](../../output/verification/brackets-2026/content-typography-report.md)
- [36pの原本と修正版](../../output/verification/brackets-2026/p036-full-comparison-final.png)
- [37pの原本と修正版](../../output/verification/brackets-2026/p037-full-comparison-final.png)

## 小小見出しの太字

37pの「【参考】サーブレットの基本」と、同じ原因で太字が欠けていた作業見出し5箇所を補強しました。元の書体・サイズ・色を保持します。既存の太字・大見出し・説明文の続きには補強を加えません。

## コード右上のファイル名

右上の位置を保ち、Meiryoの実太字、濃青、下線、淡青のラベルで強調しました。全116ヘッダーを目視し、折り返し・続きカードを含めて欠けや重なりがないことを確認しました。名前のない74部品には推測したファイル名を追加していません。元のコード枠の幅、コード本文、表の配色は維持します。

- [全件監査と実ページ](../../output/verification/brackets-2026/filename-audit.md)
- [ファイル名の変更前後](../../output/verification/brackets-2026/filename-audit/fixture-comparison-1.png)

## 最終検証

- 回帰テスト62件が合格。全19章の文字照合、はみ出し、孤立見出し、図・短いコード・表・作業手順の分断検査も合格しました。
- 全2897 ID、原本373ページへの所属、空白17ページ、合冊431ページのヘッダーを照合しました。今回の新規ID・本文改稿は0件です。
- 章別PDFから合冊への全文一致とURIリンク89件を確認しました。
- 元PDF・Word、Markdown、source設定、baseline、source-layout、既存資材を保全しました。

[テスト件数](../../output/verification/brackets-2026/regressions.json)と[最終PDFのSHA256](../../output/verification/brackets-2026/summary.json)を保存しています。前回の商標・段落字下げ・挿絵の確認は[illustrations-2026](../../output/verification/illustrations-2026/final-audit.md)に保持しています。
