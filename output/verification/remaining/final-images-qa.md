# instruction下余白修正後の最終図版QA

見出し+図ブロックの外側下余白12ptを反映した最新章PDFで更新。全19章のSHA256と共通book.typのSHA256は final-images-qa.json に保存した。目視終了後にも全19章が不変であることと、図後余白監査の対象PDFが同じSHAであることを照合。原稿・原図・共通ツールは未編集。

修正15図版のPNG確認結果は次のとおり。

|図版ID|目視結果|
|---|---|
|03/p070-f06|Spring Boot選択値4.0.2を確認。選択リスト・枠を保持。|
|03/p071-f08|吹き出しが薄黄色単色で、上端の混入コード片なし。別PNGでコード1行目を含む背景も確認。|
|03/p108-f42|赤枠内はformパッケージとProductForm.javaのみ。entityとrepositoryは枠外。|
|03/p109-f44|Product productの校正波線は消失。拡大画像でpのディセンダーと文字下端を保持。|
|05/p182-f14|フッターのCopyright ©2027を確認。他の図内文字を保持。|
|05/p186-f17|フッターのCopyright ©2027を確認。|
|05/p186-f18|フッターのCopyright ©2027を確認。|
|07/p245-f05|PPT図内のCSS/JS両方のCDNがbootstrap@5.3.8。右端のURLを保持。|
|appendix-a/p285-f07|例示MavenログのFinished at年が2027であることを確認。|
|appendix-a/p287-f09|ウィンドウのパス表記Pleiades2025-12を確認。|
|appendix-a/p287-f10|Java21とPleiades2025-12の表記を確認。|
|appendix-a/p288-f11|選択値と吹き出し内のSpring Boot4.0.2を確認。|
|appendix-a/p288-f13|Initializr図内のSpring Boot4.0.2とJava21を確認。|
|ex05/p041-f04|フッターのCopyright ©2027を確認。|
|ex05/p041-f05|フッターのCopyright ©2027を確認。|

通常図と直後の本文/見出し/コード/表を全240組監査。同一ページ207組の最小gapは12.0000pt。接触/重なり0件、12pt未満0件、metadata欠損0件。native固定ページは原本配置を保全するためこの余白規則の検査から除外。

回帰指摘のp073-f11→p073-b02も、位置マーカー差12.0000pt、実PDFの先頭文字上端との差11.99998ptを確認。下側画像枠と本文に白い隙間があることを切抜きPNGで目視。修正15図版の切抜き、コード背景、Product productの文字下端、btn-link画像周囲も最終PDFで再確認。

65スライドは開始/終了yとSVG幅高が全件一致。元の切出し内の黒枠も全件0.1pt以内で一致。物理原本の17ページ上枠だけは原本115.8200pt→元SVG/現PDF116.1200ptの既存crop差0.3000ptを維持し、親指示どおり追加改造は行っていない。

付録18図版の開始/終了y差異0件、原本画像22組のxy端も0.05pt以内で一致。グラデーション線1件はマスク表現で画素digestが異なるが元画像サイズと描画bboxは一致。

青線は図外周辺の青画素0。正規のbtn-link下線のみ存在し、不要な図外線は再現しない。コードの先頭行まで薄黄色背景が統一されている。

機械結果は final-images-qa.json と final-figure-gaps.json、実文字上端の測定は p073-gap-proof.json。PNGは final-images-qa/。06/07の再生成ログは build-late.log。
