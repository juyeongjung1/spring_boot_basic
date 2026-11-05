# 12pt・ゴシック・太字と独立見出しの監査

全19章を読み取り確認しました。原稿/組版ルールは変更していません。

MS-PGothicではfont名にBoldがなくflags=0でも、stroke0.34286（12pt）や0.31543（11.04pt）で擬似太字を表しています。font名・flags・strokeを併せて判定しました。

追加kind候補は7件。全て独立した『動作確認』で、原本11.04ptのユーザー明示例です。原本12ptゴシック太字の独立見出しはすでにheadingになっており、今回追加の漏れは0件でした。

|章|元頁|ID|現kind|原本書式|補正候補|
|---|---:|---|---|---|---|
|02|61|p061-b01|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|05|174|p174-b04|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|05|180|p180-b01|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|07|249|p249-b02|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|07|261|p261-b05|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|07|268|p268-b01|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|
|07|271|p271-b01|heading|11.04pt MS-PGothic stroke=0.31543|heading、元文字/Spanを保持、上余白18pt|

## 全「動作確認」出現箇所

|章|元頁|ID|現kind|分類|原本文字|
|---|---:|---|---|---|---|
|02|52|p052-b05|heading|独立見出し|動作確認|
|02|56|p056-b09|heading|独立見出し|動作確認|
|02|56|p056-b10|paragraph|本文内の言及|以下のURL から、動作確認をすると、同じようにView からのリクエストパラメータを取得してコ / ンソール上に出力できているのがわかります。|
|02|61|p061-b01|heading|独立見出し|動作確認|
|03|89|p089-b01|heading|独立見出し|動作確認|
|03|94|p094-b05|heading|独立見出し|動作確認|
|03|98|p098-b01|heading|独立見出し|動作確認|
|03|102|p102-b01|heading|独立見出し|動作確認|
|03|111|p111-b04|heading|独立見出し|動作確認|
|03|120|p120-b01|heading|独立見出し|動作確認|
|03|124|p124-b03|heading|独立見出し|動作確認|
|03|126|p126-b16|paragraph|本文内の言及|◼ 動作確認用のダミー: テスト環境では、ダミーのデータを返すモッククラスを使いた / い。|
|04|141|p141-b01|heading|独立見出し|動作確認|
|04|146|p146-b01|heading|独立見出し|動作確認|
|04|153|p153-b08|heading|独立見出し|動作確認|
|05|174|p174-b04|heading|独立見出し|動作確認|
|05|180|p180-b01|heading|独立見出し|動作確認|
|06|207|p207-b01|heading|独立見出し|動作確認|
|06|212|p212-b01|heading|独立見出し|動作確認|
|06|221|p221-b01|heading|独立見出し|動作確認|
|06|227|p227-b04|paragraph|本文内の言及|http://localhost:8080/product/findAll で動作確認を行うと、従来と同じように全件検索の結果 / が表示されることを確認できます。|
|06|229|p229-b04|paragraph|本文内の言及|http://localhost:8080/product/ でID 検索の動作確認をすると、同じ主キー検索ができるの / が確認できます。|
|06|231|p231-b01|heading|独立見出し|動作確認|
|07|249|p249-b02|heading|独立見出し|動作確認|
|07|261|p261-b05|heading|独立見出し|動作確認|
|07|264|p264-b02|heading|独立見出し|■動作確認|
|07|268|p268-b01|heading|独立見出し|■動作確認|
|07|271|p271-b01|heading|独立見出し|■動作確認|
|07|279|p279-b01|heading|独立見出し|■動作確認|
|ex02|15|p015-b14|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex02|16|p016-b12|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex03|22|p022-b05|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex03|24|p024-b04|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex03|25|p025-b11|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex03|27|p027-b11|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex04|32|p032-b14|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex04|33|p033-b15|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex04|35|p035-b13|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex05|40|p040-b08|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex05|43|p043-b04|paragraph|URL/本文との混在|◼ 動作確認：http://localhost:8080/|
|ex06|54|p054-b03|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「全社員一覧」リンクをクリックし、社員リストが表示されるか確認してください。|
|ex06|54|p054-b15|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「社員番号で検索」に、「1001」を入力し、検索します。社員が表示されるか確認してくださ / い。|
|ex06|56|p056-b05|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「社員番号で検索2」に、「9999」を入力し、検索します。 / 「該当する社員情報は存在しません。」が表示されることを確認します。|
|ex06|58|p058-b07|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「社員データ登録」リンクをクリックします。勤務地の選択肢が正しく表示されるのかを確認し / ます。|
|ex06|59|p059-b05|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「社員データ登録」リンクをクリックし、任意のデータを入れ、登録します。正しく登録されるの / かを確認してください。|
|ex06|62|p062-b04|paragraph|URL/本文との混在|動作確認：http://localhost:8080/ / 「詳細検索」リンクをクリックし、給与を「400000 円」以上、勤務地は「tokyo」に設定し、検索し / てください。2 件のデータが表示されるかを確認してください。|
|ex07|76|p076-b12|paragraph|URL/本文との混在|■動作確認 / http://localhost:8080/4|

## 原本57pとの対応

原本57pのスライド下はp057-b02/p057-b03の本文で、「動作確認」の独立ラベルはありません。原本52p p052-b05と56p p056-b09は12pt太字ゴシックの既存headingです。元座標・前後node・参考flow位置はJSONへ記録しました。現PDFの58pを原本58p/57pと同一視しないでください。

## 明示除外条件に合う既存heading（別枠）

URLや式だけのコードラベルは、太字12ptでも全体を見出し化しない条件に当たります。以下は現在headingなので、paragraphへ戻すかrootが判断する候補です。

|章|元頁|ID|文字|理由|
|---|---:|---|---|---|
|03|89|p089-b02|http://localhost:8080/product/findAll|URL/URLを伴う案内行（全体を見出し化しない）|
|04|141|p141-b02|http://localhost:8080/|URL/URLを伴う案内行（全体を見出し化しない）|
|04|146|p146-b02|http://localhost:8080/2 <--こちらのURL へアクセスします。|URL/URLを伴う案内行（全体を見出し化しない）|
|06|206|p206-b07|■ th:if="${product.category != null}"|式/アノテーションだけのコードラベル|
|06|206|p206-b09|■ th:unless="${product.category != null}"|式/アノテーションだけのコードラベル|
|06|207|p207-b02|http://localhost:8080/product/findAll|URL/URLを伴う案内行（全体を見出し化しない）|
|06|212|p212-b02|http://localhost:8080/product/|URL/URLを伴う案内行（全体を見出し化しない）|
|06|221|p221-b02|http://localhost:8080/product/insert|URL/URLを伴う案内行（全体を見出し化しない）|
|06|231|p231-b02|http://localhost:8080/product/insert|URL/URLを伴う案内行（全体を見出し化しない）|

本文内の一部太字・表セル・図内ラベルは候補から除外しました。図内文字は本文段落の見出し判定と別です。既存小見出しの上余白18ptは本担当では変更していません。
