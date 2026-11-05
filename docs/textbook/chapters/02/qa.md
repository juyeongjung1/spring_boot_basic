# 第2章 Spring Web アプリケーション 検証記録

## 対象と生成結果

- 元PDF: 31〜62ページ
- 元位置再現版: 32ページ
- 自動組版版: 27ページ
- 図版: 33点、うち編集用PPT原本 9点
- Markdown表: 0個
- 本文の改訂、JavaやSpring Bootの版変更はこの工程では行っていない。

## 自動検査

元位置再現版は全ページの文字照合が一致した。自動組版版も本文文字の照合が一致し、見出しの孤立、図版分断、短いコード枠分断、操作説明群の分断、ページ外へのはみ出しを検出しなかった。詳しい検査位置は出力先のchecks.jsonに記録した。

元PDFとの画像差は、RGB各成分0〜255に対する絶対差平均で 0.2125。最大は元PDF38ページの 0.6187。この値は完全な画素一致を意味するものではなく、フォントやSVG描画の微差を含む。

## 画像による確認

元位置再現版・自動組版版の全ページを縮小画像で確認した。特に元PDF38・47・58ページに対応するスライド・表・コード・注釈を実寸画像でも確認し、文字欠けや注釈の切れがないことを確認した。図版ROIと元PDFのベクトル図形の交差も監査し、独立した吹き出し・矢印が切り出し枠から欠ける箇所を解消した。

47ページの黄色い吹き出しを画面と一体で切り出し、62ページの埋め込みPPT対応をSlide17へ訂正した。コード枠を表と誤検出した候補を除外した。

PPT原本はWord埋め込みファイルとのバイト照合が一致した。元位置再現版は元の改ページを保持する。自動組版版は本文量に従って改ページするため、ページ数・ページ内位置は変化する。各版は同じchapter.mdから生成される。

## 成果物

- docs/textbook/chapters/02/chapter.md
- docs/textbook/chapters/02/source.json
- docs/textbook/chapters/02/source-layout.json
- docs/textbook/chapters/02/assets/
- output/pdf/textbook/chapter-02/chapter-reference.pdf
- output/pdf/textbook/chapter-02/chapter-flow.pdf
- output/pdf/textbook/chapter-02/comparison.pdf
- output/pdf/textbook/chapter-02/checks.json
