# 追加挿絵24点と既存10点の最終PDFレビュー

判定：合格。機械検査・全34図の目視を完了。

最終合冊本文364頁。PDF SHA256：`a3cfbd131dd2ada326f82c6b8778ef901f7c06d965d78f279d99e61a37c5e20b`。

追加前の比較対象はf16135f版（本文349頁）です。比較PNGには「追加前 f16135f」と「追加後」を明記しています。

- 全34図とcaptionが同じ物理頁。新24図は宣言した前後の原稿ブロックの間にあります。
- 幅280pt以下、高さ140pt以下。全34図の図/caption領域は章PDFと合冊で全画素一致。
- 全24図について、ページ全体と図/caption拡大を目視し、欠け・重なり・読めない文字を認めませんでした。既存10図も合冊PNGで再確認。
- 元PPT65点は追加前版と位置・幅・高さ・同領域の全画素が一致。
- 追加図5件の頁末移動と、DTO2件・丸数字方法導入の分離は、最終版で解消しました。

## 新24図の比較と実寸

|図|元頁|追加前f161本文頁|追加後本文頁|幅×高さpt|比較|実ページ|
|---|---:|---:|---:|---|---|---|
|共通の基盤にアプリケーション固有の処理を組み合わせる|18|18|18|280.00×116.64|[比較](pages/01-framework-foundation-comparison.png)|[実頁](pages/01-framework-foundation-merged-page.png)|
|Spring Bootが管理するライブラリのバージョンの組合せ|22|22|24|280.00×116.64|[比較](pages/01-boot-managed-versions-comparison.png)|[実頁](pages/01-boot-managed-versions-merged-page.png)|
|条件に合う共通機能のBeanを自動で用意する|23|23|25|280.00×116.64|[比較](pages/01-bean-auto-configuration-comparison.png)|[実頁](pages/01-bean-auto-configuration-merged-page.png)|
|検索のお願いと検索結果の応答|35|35|37|280.00×116.64|[比較](pages/02-request-response-search-comparison.png)|[実頁](pages/02-request-response-search-merged-page.png)|
|同じURLでもGETとPOSTで担当メソッドが変わる|52|56|59|280.00×116.64|[比較](pages/02-get-post-routing-comparison.png)|[実頁](pages/02-get-post-routing-merged-page.png)|
|入力欄のnameとFormのフィールドを結び付ける|54|58|61|280.00×116.52|[比較](pages/02-form-name-binding-comparison.png)|[実頁](pages/02-form-name-binding-merged-page.png)|
|user.idをキー名とフィールド名に分けて読む|60|67|71|280.00×119.38|[比較](pages/02-model-key-property-comparison.png)|[実頁](pages/02-model-key-property-merged-page.png)|
|Repositoryの宣言から使える実装オブジェクトが用意される|78|90|94|280.00×116.52|[比較](pages/03-repository-implementation-comparison.png)|[実頁](pages/03-repository-implementation-merged-page.png)|
|メソッド名と引数が検索条件になる|97|115|120|280.00×116.52|[比較](pages/03-query-method-name-comparison.png)|[実頁](pages/03-query-method-name-merged-page.png)|
|redirectはブラウザーからの新しいリクエストを生む|124|148|154|280.00×116.52|[比較](pages/03-redirect-new-request-comparison.png)|[実頁](pages/03-redirect-new-request-merged-page.png)|
|ModelとHttpSessionではデータを渡す範囲が違う|143|171|179|280.00×116.64|[比較](pages/04-model-session-lifetime-comparison.png)|[実頁](pages/04-model-session-lifetime-merged-page.png)|
|入力値と入力エラーを同じ画面へ戻す|153|185|193|280.00×116.64|[比較](pages/04-form-error-roundtrip-comparison.png)|[実頁](pages/04-form-error-roundtrip-merged-page.png)|
|null・空文字・空白だけの文字列は同じではない|157|190|198|280.00×116.64|[比較](pages/04-null-blank-constraints-comparison.png)|[実頁](pages/04-null-blank-constraints-merged-page.png)|
|タグに見える入力を文字として表示する|169|204|212|280.00×116.64|[比較](pages/05-text-escape-comparison.png)|[実頁](pages/05-text-escape-merged-page.png)|
|リンクのURLに含めたIDを引数へ取り出す|174|209|217|280.00×116.52|[比較](pages/05-dynamic-url-id-comparison.png)|[実頁](pages/05-dynamic-url-id-merged-page.png)|
|プロジェクト内の保存場所とブラウザー用URLを区別する|179|215|224|280.00×116.64|[比較](pages/05-static-public-path-comparison.png)|[実頁](pages/05-static-public-path-merged-page.png)|
|mappedByのフィールド名とJoinColumnの列名を区別する|201|241|251|280.00×116.64|[比較](pages/06-relationship-field-column-comparison.png)|[実頁](pages/06-relationship-field-column-merged-page.png)|
|参照先がある場合だけ次のフィールドを読む|206|246|257|280.00×116.64|[比較](pages/06-null-reference-guard-comparison.png)|[実頁](pages/06-null-reference-guard-merged-page.png)|
|選択肢の表示名と送信する値は異なる|218|259|270|280.00×116.64|[比較](pages/06-select-label-value-comparison.png)|[実頁](pages/06-select-label-value-merged-page.png)|
|JPQLではJava側の名前を使う|225|266|277|280.00×116.64|[比較](pages/06-jpql-entity-names-comparison.png)|[実頁](pages/06-jpql-entity-names-merged-page.png)|
|商品をカテゴリ別にまとめて集計する|233|275|287|280.00×116.64|[比較](pages/06-groupby-aggregate-dto-comparison.png)|[実頁](pages/06-groupby-aggregate-dto-merged-page.png)|
|CSS・JSをどこから読み込むか|245|288|301|280.00×116.64|[比較](pages/07-cdn-local-delivery-comparison.png)|[実頁](pages/07-cdn-local-delivery-merged-page.png)|
|マージンは枠の外、パディングは枠の内|259|305|318|280.00×116.64|[比較](pages/07-spacing-box-model-comparison.png)|[実頁](pages/07-spacing-box-model-merged-page.png)|
|container・row・colの入れ子|265|311|326|280.00×116.64|[比較](pages/07-grid-containment-comparison.png)|[実頁](pages/07-grid-containment-merged-page.png)|

## 重点確認

元201頁では、旧FK図と新mappedBy図が同じ物理頁に共存します。新旧の図と本文に重なりはありません。

元233/234頁のDTO導入ラベル2件は対応コードと同頁です。元206頁の方法見出し・導入文・コードも同頁です。位置と対応IDはJSONに記録しました。

## 余白が広い継続頁

元22頁のBoot管理対象図は本文24頁（章01の10頁）に図とcaptionだけを置いています。元の操作説明と依存ライブラリ画面のまとまり、次の元頁23の開始を保持した結果です。図自体は約99×41mmで、大きな絵に拡大して埋めてはいません。読み順の破綻やはみ出しはありませんが、余白が広いという紙面上の特徴を記録します。

[該当ページ](pages/01-boot-managed-versions-merged-page.png)

## 保存した証跡

pages/には新24点のbefore→after比較、全34点の最終合冊実ページ・図/caption拡大、全件コンタクト、元201/233頁の重点ページを保存しています。全件の画像SHA、図の座標・実寸・物理頁と、最終合冊SHAはJSONで結び付けています。

### 全件コンタクト

- [表示](pages/merged-detail-contact-01.png)
- [表示](pages/merged-detail-contact-02.png)
- [表示](pages/merged-detail-contact-03.png)
- [表示](pages/merged-detail-contact-04.png)
- [表示](pages/merged-detail-contact-05.png)
- [表示](pages/merged-detail-contact-06.png)
- [表示](pages/merged-page-contact-01.png)
- [表示](pages/merged-page-contact-02.png)
- [表示](pages/merged-page-contact-03.png)
- [表示](pages/merged-page-contact-04.png)
- [表示](pages/merged-page-contact-05.png)
- [表示](pages/merged-page-contact-06.png)
- [表示](pages/merged-page-contact-07.png)
- [表示](pages/merged-page-contact-08.png)
- [表示](pages/merged-page-contact-09.png)

### 重点ページ

- [表示](pages/focus-introduction-p206-b11-merged.png)
- [表示](pages/focus-introduction-p233-b09-merged.png)
- [表示](pages/focus-introduction-p234-b01-merged.png)
- [表示](pages/focus-source-201-merged-011.png)
- [表示](pages/focus-source-201-merged-012.png)
- [表示](pages/focus-source-233-merged-047.png)
- [表示](pages/focus-source-233-merged-048.png)
