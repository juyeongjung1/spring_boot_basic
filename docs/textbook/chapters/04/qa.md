# 第4章 セッションと入力チェック 検証記録

## 対象と生成結果

- 元PDF: 133〜163ページ
- 元位置再現版: 31ページ
- 自動組版版: 25ページ
- 図版: 25点、うち編集用PPT原本 7点
- Markdown表: 2個
- 本文の改訂、JavaやSpring Bootの版変更はこの工程では行っていない。

## 自動検査

元位置再現版は全ページの文字照合が一致した。自動組版版も本文文字の照合が一致し、見出しの孤立、図版分断、短いコード枠分断、操作説明群の分断、ページ外へのはみ出しを検出しなかった。詳しい検査位置は出力先のchecks.jsonに記録した。

元PDFとの画像差は、RGB各成分0〜255に対する絶対差平均で 0.2168。最大は元PDF157ページの 0.8073。この値は完全な画素一致を意味するものではなく、フォントやSVG描画の微差を含む。

## 画像による確認

元位置再現版・自動組版版の全ページを縮小画像で確認した。特に元PDF136・137・138・150・155・157・159・161ページに対応するスライド・表・コード・注釈を実寸画像でも確認し、文字欠けや注釈の切れがないことを確認した。図版ROIと元PDFのベクトル図形の交差も監査し、独立した吹き出し・矢印が切り出し枠から欠ける箇所を解消した。

User定義と初期データを2つのMarkdown表にした。157ページのValidation一覧はPPT内部の図版として保持した。137ページの閉じ括弧や空行を含むコード枠の結合、ファイル名とコードの一体配置を確認した。

PPT原本はWord埋め込みファイルとのバイト照合が一致した。元位置再現版は元の改ページを保持する。自動組版版は本文量に従って改ページするため、ページ数・ページ内位置は変化する。各版は同じchapter.mdから生成される。

## 成果物

- docs/textbook/chapters/04/chapter.md
- docs/textbook/chapters/04/source.json
- docs/textbook/chapters/04/source-layout.json
- docs/textbook/chapters/04/assets/
- output/pdf/textbook/chapter-04/chapter-reference.pdf
- output/pdf/textbook/chapter-04/chapter-flow.pdf
- output/pdf/textbook/chapter-04/comparison.pdf
- output/pdf/textbook/chapter-04/checks.json
