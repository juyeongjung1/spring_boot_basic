# 追加24図の最終第二者レビュー

合格：最終24点を原寸・560px印刷相当で確認。再編集が必要な残件は0点です。

最終24点の生成元とSHAを固定。初回確認のうち10点はSHA一致で継承し、再編集4点・新規9点・差替え新規1点を原寸で確認した。今回の最終差替え時は他23点のSHA完全一致も確認。最終560pxシート4枚で24点を目視し、元画像/教材assetsは加工していない。

## 修正後の確認

- Formの入力`name`の引用符は直線となり、`id`/`password`の綴りと1つの`UserForm`へ入る対応を保持。
- Repositoryの長いラベルを短縮・拡大し、560pxでも読みやすくなった。図の宣言と実装の区別、`findAll()`/`save()`は維持。
- redirectの初回ブラウザーは空で、完成HTMLを返す矢印とは分離。`redirect:/product/findAll`の綴りと新規リクエストの向きも正しい。
- query-method-nameは30000=テレビ・20000=モニター・50000=PCへ修正。`findByPrice(20000)`と選別結果が一致。

## 技術的な確認

- `${user.id}`は`$`・波括弧・ドット・大小文字まで正確。`user`キー→`UserForm`の`id:1234`→出力`1234`の対応が正しい。
- `String`の`@NotNull`/`@NotBlank`は`null`・空文字・空白のみ・`ABC`に対する全8結果を確認。
- `th:text`は`<b>A</b>`をタグとして解釈せず文字列として表示する図になっている。
- 動的URLの商品ID4は冷蔵庫、`/product/findById/4`の`4`が`@PathVariable`の`id`へ入る。
- `static`内の`css/style.css`・`js/script.js`は、公開URLの`/css/style.css`・`/js/script.js`に対応する。
- `mappedBy`はJavaの`Product.category`、`JoinColumn`はDBの`category_id`を指す。`Category.productList`の綴りも正しい。
- `category`参照ありでは`Category.name`の冷蔵庫を表示し、`category`が`null`のときは`name`へ進まず未設定へ分岐する。文字列`null`の入った`Category`を描いていない。
- 表示名の冷蔵庫と送信値3を区別し、`categoryId=3`へ渡す。
- JPQLは`FROM Product p`と`p.category.name`で、DBの`product`/`category_id`と区別。
- 図の3件のGROUP BY例はAが30000+20000=50000、COUNT 2、Bが15000、COUNT 1。DTOへ各集計値が正しく出る。captionも図の例と明示。
- その他のリクエスト/レスポンス、GET/POST、Model/HttpSession、CSS box model、container/row/col、CDN/staticの矢印とラベルに問題なし。

## 全件の記録

| 図ID | 章/元頁 | 原寸確認 | 小型確認 | 判定 |
| --- | --- | --- | --- | --- |
| framework-foundation | 01/18 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| boot-managed-versions | 01/22 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| bean-auto-configuration | 01/23 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| request-response-search | 02/35 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| get-post-routing | 02/52 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| form-name-binding | 02/54 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| model-key-property | 02/60 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| repository-implementation | 03/78 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| query-method-name | 03/97 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| redirect-new-request | 03/124 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| model-session-lifetime | 04/143 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| form-error-roundtrip | 04/153 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| null-blank-constraints | 04/157 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| text-escape | 05/169 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| dynamic-url-id | 05/174 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| static-public-path | 05/179 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| relationship-field-column | 06/201 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| null-reference-guard | 06/206 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| select-label-value | 06/218 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| jpql-entity-names | 06/225 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| groupby-aggregate-dto | 06/233 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| cdn-local-delivery | 07/245 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| spacing-box-model | 07/259 | 目視/保存SHA一致 | 560pxで目視 | 合格 |
| grid-containment | 07/265 | 目視/保存SHA一致 | 560pxで目視 | 合格 |

## 印刷相当の比較シート

- [シート1](second-review-sheet-01.png)
- [シート2](second-review-sheet-02.png)
- [シート3](second-review-sheet-03.png)
- [シート4](second-review-sheet-04.png)

元出力の絶対パス・SHA256・画素数・印刷寸法・個別所見・教材側の保存予定先は[JSON](second-review.json)へ記録。最終差替え図のnull-reference-guardを原寸と560pxで確認し、他23点のSHA完全一致を確認した。シートは最新の24点だけで再作成している。

この記録は画像内容と小型表示のQAであり、本文への配置・PDFの自動改ページ・ページ端の欠けは統合後の検証で別途確認する。画像編集・原稿改稿・生成元/プロジェクトassetsの加工、テスト実行は行っていない。
