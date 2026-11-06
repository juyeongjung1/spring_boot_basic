# 生成挿絵9点の小型目視QA

2026-11-05。原稿・図版を変更せず、300×140pt相当・144dpiに縮小したPNGを全件目視し、現在の本文captionと照合した。

| 図 | 判定 | 確認内容 |
| --- | --- | --- |
| 01・maven | 可読・欠けなし | pom.xml→Maven→必要ライブラリ。最新版やアプリ全体の自動生成とは描いていない。 |
| 02・model | 可読・欠けなし | Controllerのデータとテンプレートの二入力をThymeleafが合成しHTML出力。Modelを実行工程やDBと描かない。 |
| 03・repository | 可読・欠けなし | findAllは0件以上、findByIdは0/1件。captionがOptionalを明示し、絵の空ケースと一致。 |
| 04・session | 可読・欠けなし | ブラウザーにID、ログイン情報はサーバー枠内。captionがセッションIDと明示。 |
| 04・validation | 可読・欠けなし | 検証→エラー表示／処理を続けるの分岐。captionでForm・サーバー側と補足し、認証成功を表さない。 |
| 05・layout | 可読・欠けなし | 青の共通レイアウトと橙の内容が合成前後で一致。captionがサーバー側と補足。 |
| 06・foreign-key | 可読・欠けなし | DBはcategory_id=2→id=2、JavaはProduct.category→Category。DBセルにオブジェクト全体を置かない。 |
| 07・responsive | 可読・欠けなし | 768px以上は横並び、未満はサイドバー→本文の上下。同じ色と順序。3:9は概略寸法（注記参照）。 |
| appendix-b・errors | 可読・欠けなし | Caused by:→自分のコードProductService.java/26行。captionがこのログの例と限定。 |

全図でラベルの誤字・切れ・意図しない矢印の文字接触は見当たらない。画像内の情報だけに依存せず、Session／Validation／Layout／Optional／エラー例の限定をcaptionで補っている。

## Responsiveの寸法について

768px以上／未満、サイドバー→本文の順序は正しい。広幅の青色面296px・緑色面823pxで約1:2.78であり、12列を数学的に分割した厳密な3:9の作図ではない。今回は横並びが縦並びへ変わる概念図として扱い、正確な列幅は本文のcol-md-3/col-md-9と既存のグリッド図に委ねる。親担当へ数値を報告済み。図版自体は変更していない。

## 次の実PDF確認

最終章PDFで小型表示の文字、figure/caption同頁、原page境界、既存コード・表・見出しへの接触を確認する。現時点では単体画像の合格であり、最終PDF配置まで検証済みとはしない。既存DI図も縮小後の実サイズを確認する。

根拠画像：各 `*-small300x140-144dpi.png` と `generated-small-review-1.png`／`2.png`。JSONには9元画像のSHA256・本文caption・個別判定を保存した。
