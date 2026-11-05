# 句点欠落の点検・補完報告

基準HEAD: a5cfe59。新しい説明・手順・言い換えを追加せず、完結する叙述/指示の句点だけを補いました。

全19章のparagraph/step 1839ブロックから候補600件を確認。本担当は10章31ブロックへ句点33字を追加し、第1章p022-b08の1字はboot4担当が補完しました。

- 第1章以外の全18章で、本文の非句点文字は完全一致。
- 原文の書式Span・改行も保持。rootのheading分類5件のみMarkdown種別差として区別。
- コード・表・URL・パス・図版参照・ページ順/内容IDは不変。
- baseline/source-layout全38ファイルのSHA-256が点検前後で一致。図版への書き込みは0件。
- 固定頁はrootが承認したp012-b05の1行目末とp285-b03の最終行末だけ補完し、既存native_text_updatesを保持してIDを追記。

見出し・目標項目・名詞の列挙・定義一覧・URL/コード・引用断片・括弧内の補助注記には機械的に句点を付けていません。次Divへ続く原文は結合/推敲していません。

|章|ID|行（1始まり）|補完前|補完後|
|---|---|---:|---|---|
|front|p012-b05|1|画面に表示される文字 [プロパティ]を選択します|画面に表示される文字 [プロパティ]を選択します。|
|02|p040-b03|2|「IndexController」と入力し、[完了]をクリック|「IndexController」と入力し、[完了]をクリック。|
|02|p045-b08|1|5. 任意のブラウザ（Chrome、Edge など）のアドレスバーに以下のURL を入力します|5. 任意のブラウザ（Chrome、Edge など）のアドレスバーに以下のURL を入力します。|
|03|p084-b04|1|② DAO クラスに定義されているデータベース操作用のメソッドを実行し、データを取得する|② DAO クラスに定義されているデータベース操作用のメソッドを実行し、データを取得する。|
|03|p084-b05|1|③ 取得したデータを、スコープに格納|③ 取得したデータを、スコープに格納。|
|03|p084-b06|1|④ JSP へ遷移|④ JSP へ遷移。|
|03|p094-b06|1|http://localhost:8080/product/  product の後ろに必ず/を付けてください|http://localhost:8080/product/  product の後ろに必ず/を付けてください。|
|03|p098-b02|1|http://localhost:8080/product/  product の後ろに必ず/を付けてください|http://localhost:8080/product/  product の後ろに必ず/を付けてください。|
|03|p102-b02|1|http://localhost:8080/product/  product の後ろに必ず/を付けてください|http://localhost:8080/product/  product の後ろに必ず/を付けてください。|
|03|p120-b02|1|http://localhost:8080/product/  product の後ろに必ず/を付けてください|http://localhost:8080/product/  product の後ろに必ず/を付けてください。|
|03|p124-b04|1|http://localhost:8080/product/  product の後ろに必ず/を付けてください|http://localhost:8080/product/  product の後ろに必ず/を付けてください。|
|07|p256-b04|1|※p や mb のクラスは、次のページで説明します|※p や mb のクラスは、次のページで説明します。|
|07|p258-b02|1|➀ 「F12」で「開発者ツール」を開きます|➀ 「F12」で「開発者ツール」を開きます。|
|07|p268-b04|1|※より詳しい構文は、https://getbootstrap.jp/docs/5.3/layout/grid/ を参照|※より詳しい構文は、https://getbootstrap.jp/docs/5.3/layout/grid/ を参照。|
|07|p271-b03|2|※より詳しい構文は、 https://getbootstrap.jp/docs/5.3/layout/columns/ を参照|※より詳しい構文は、 https://getbootstrap.jp/docs/5.3/layout/columns/ を参照。|
|appendix-a|p285-b03|2|[spring_exercise]プロジェクトを右クリック→[Maven install]をクリック|[spring_exercise]プロジェクトを右クリック→[Maven install]をクリック。|
|ex02|p015-b15|1|⚫ 身長と体重を入力し、正しくBMI 値が出力されるかを確認|⚫ 身長と体重を入力し、正しくBMI 値が出力されるかを確認。|
|ex02|p016-b13|1|⚫ 身長と体重を入力し、正しくBMI 値が出力されるかを確認|⚫ 身長と体重を入力し、正しくBMI 値が出力されるかを確認。|
|ex03|p027-b12|1|⚫ [社員データ登録]リンクをクリック|⚫ [社員データ登録]リンクをクリック。|
|ex03|p027-b13|1|⚫ 登録する社員データを入力し、[登録]ボタンをクリック|⚫ 登録する社員データを入力し、[登録]ボタンをクリック。|
|ex03|p027-b14|1|⚫ 入力したデータ通りに、新規データが登録されているかを確認|⚫ 入力したデータ通りに、新規データが登録されているかを確認。|
|ex04|p031-b03|1|⚫ 入力値に誤りがない場合は検索画面へ遷移|⚫ 入力値に誤りがない場合は検索画面へ遷移。|
|ex06|p051-b05|1|o クラスに@Entity、@Table アノテーションを付けること|o クラスに@Entity、@Table アノテーションを付けること。|
|ex06|p051-b06|2|と|と。|
|ex06|p051-b11|3|o Location 型のlocation フィールドを追加すること|o Location 型のlocation フィールドを追加すること。|
|ex06|p051-b11|5|付けを行うこと|付けを行うこと。|
|ex06|p051-b15|3|o Employee エンティティを格納するリストフィールドを作成すること|o Employee エンティティを格納するリストフィールドを作成すること。|
|ex06|p051-b15|4|o @OneToMany(mappedBy = "location") アノテーションを付けること|o @OneToMany(mappedBy = "location") アノテーションを付けること。|
|ex06|p058-b02|1|• LocationRepository から findAll() を使って、Location のリストを取得できます|• LocationRepository から findAll() を使って、Location のリストを取得できます。|
|ex06|p061-b04|1|1. 「/showSearchForm」でアクセスすると検索入力画面が表示される|1. 「/showSearchForm」でアクセスすると検索入力画面が表示される。|
|ex07|p070-b02|2|■ ブラウザから、「localhost:8080/findAll」を開いて、メニュー修正していく演習です|■ ブラウザから、「localhost:8080/findAll」を開いて、メニュー修正していく演習です。|
|ex07|p075-b06|1|• form-control は入力欄に付ける|• form-control は入力欄に付ける。|
|ex07|p075-b07|1|• 親要素に input-group を付けることで横並びになる|• 親要素に input-group を付けることで横並びになる。|

## 小見出し分類漏れの共有

03:p080-b06/b10、07:p246-b03/b09・p247-b05の5件をrootへ共有し、rootがheadingへ局所補正しました。本文や書式Spanの変更、句点追加はしていません。

PDF生成と組版の確認はrootが行います。
