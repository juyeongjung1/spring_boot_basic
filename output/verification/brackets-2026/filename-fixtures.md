# コード右上ファイル名の強調

判定：試作・回帰テストとも合格。CSSは確定し、全章再生成をrootへ引き渡した。

- 明朝/通常フォント相当だった実PDFのMS-PGothic(flags0)を、Meiryo-Bold(flags16)へ変更。深い青#123d68、下線、淡青ラベルと控えめな枠を追加した。位置は右上のまま。
- 文字列とHTMLのheader構造は変更せず、CSSのfilename/file-itemのみを変更。コード本文幅・白テーマ・表配色・挿絵は維持。
- 短い名前・通常path・続きカードのheader高さは35.52ptで変更なし。2/3行に折り返す極長日本語pathだけ約3.49pt増加。8fixture全ての本文コード幅は変更なし。
- 実PDFで全ファイル名のMeiryo-Bold埋込、flags16、深青色、各行の下線矩形を確認。短名/日本語長path/続きカードをPNGで目視し、欠け・重なりなし。
- モノクロPNGでも太字+下線でファイル名を識別できる。
- test_html_components.pyは10件成功。元5filename画像文字化のテキスト/ID保持、元46解説の原文、緑コメント、元表色の検査も成功。

## 証跡

`comparison-1.png`/`comparison-2.png`はbefore→after、`pdf-short-1.png`と`pdf-narrow-long-1.png`は実PDFレンダリング、`header-continued.png`は続きカードの実PDF。`header-*-monochrome.png`は印刷を想定したグレースケール確認用。

`report.json`に実寸・フォント・下線・CSS SHAと全測定結果を保存。本文/ファイル名文字列を変更していない。修正対象はcomponents.cssと回帰テストの2ファイルのみ。
