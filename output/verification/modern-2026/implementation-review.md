# HTML部品・PDF統合の独立レビュー

既知4件は修正済み。未解決の具体的な出力欠落は検出していない。最終PDFの全頁監査はbuild完了後。

修正済みの具体的指摘：

- P1 先頭空行でコードと行番号が1行ずれる：03/p085-b04：元の1行目空行、2行目@Controllerが、初版プレビューでは1行目@Controllerとなっていた。 root修正済み。改行4例と実データの再現確認すべて合格。
- P2 番号付きHTMLがJavaとして色分けされる：02/p060-b01のHTML継続および番号付きHTML ownerを持つ構文解説。 root修正済み。p060の言語htmlを確認。
- P2 最初のrow.source_idsへ同カードの後続IDが混入：07/p273-b04から始まるカードなど27行。 root指示でsource_idsだけをsource_fragmentsの重複除去へ補正。その他フィールド完全不変。rendererもfragments由来。
- P2 引数の列挙を単独newline除去で連結：02/p059-b02の第1引数と第2引数。 root修正済み。各引数が別pになることを確認。84 meaning内の他の番号列挙・箇条書きは0。

先頭/末尾改行4例、実p085の空行、p060のHTML判定、p059の引数列挙、計7件の再現検証はすべて合格。84 meaningを全件点検し、他の箇条書き/番号列挙の連結はない。

残る範囲・制約：

- コードのコピー：行番号は独立した可視PDF文字として出力され、コードはpre-wrap/overflow-wrap:anywhereで折り返される。HTMLカード全体やPDFページ全体をまとめて選択すると番号・見出し・折返し改行が混ざるため、そのまま実行できるコードのコピーを保証する実装ではない。専用source-code領域の選択や元プロジェクトのファイル内容とは区別する。
- 組版検査の意味：builderの最終CounterはHTML部品自身のpdf_textを期待値に使う。出力PDFへの合成欠落には強いが、HTML化前の誤変換自体は単独では検出しない。今回のraw source_texts/code_line_sourcesガードと独立JSON roundtrip/行ずれテストがその差を補う。
- IDアンカーのfallback：DOMのdata-source-idsに現れないconsume IDは末尾の1pt矩形に所属させる。このfallbackは画像ラベル変換向けであり、そのIDの元文章が表示されたことを単独で証明しない。今回の実データは全JSON fragmentを復元し、全元ID/頁所属も最終監査で別途確認する。

現在の構造について：

- コード・表・解説を共通の行分割rendererとPDF合成へまとめる方式は妥当。原本ページごとのデータ所属を維持し、browserをfinallyで閉じる実装も確認した。
- 表の共通本文幅426.672pt、9.5pt、padding5pt、純数値nowrapと、原スタイル由来の色/強調を確認。コメント色はCSSで#008000固定。
- 今回の目的外のリファクタリングや旧Typst描画の撤去は不要。既存の原位置比較と診断用fallbackを壊す変更を増やさない。

renderer/build/typ/原稿は編集していない。rootから明示されたJSON source_ids27行の最小補正と監査報告SHA更新のみ実施。
