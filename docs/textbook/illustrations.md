# 教材へ挿入した小型イラスト

小型イラストは全34点です。HTMLのname属性とFormの対応図を作り直し、th:eachの左右を説明する図を追加しました。不要なRepository返り値の図は削除しています。画像本体は幅300pt・高さ140pt以内、標準幅280pt、既存DI図は260ptです。

図番号とキャプションを同じ枠内へ収め、図とキャプションを同じページに保持します。図中は短い語と色で関係を示し、詳しい説明は元の本文を使います。th:each図は、コードに混入していたPPT吹き出しの説明を図として分離したものです。

## 概念の理解を補う24点

| 挿絵 | 章・元頁 | 理解を補う点 | 画像 |
| --- | --- | --- | --- |
| 共通の基盤にアプリケーション固有の処理を組み合わせる | 01・18p | 抽象語の『フレームワーク』を、共通の土台と個別に作る部分の区別として記憶できるようにする。 | [表示](chapters/01/assets/revision-ill-framework-foundation.png) |
| DIコンテナからAクラスへリモコンを渡す | 01・20p | 倉庫に準備されたリモコンをAへ渡し、スイッチ（メソッド）でBの機能を利用する本文の比喩を示す。 | [表示](chapters/01/assets/revision-ill-di-remote-intro.png) |
| BeanはDIコンテナに準備されたリモコン本体 | 01・23p | DIコンテナを倉庫、Beanを倉庫の中のリモコン本体として識別する。 | [表示](chapters/01/assets/revision-ill-bean-auto-configuration.png) |
| 検索のお願いと検索結果の応答 | 02・35p | リクエストとレスポンスを、教科書本文の服の検索の具体的な行動と対応付ける。 | [表示](chapters/02/assets/revision-ill-request-response-search.png) |
| 同じURLでもGETとPOSTで担当メソッドが変わる | 02・52p | URLだけが対応付けの条件ではなく、HTTPメソッドも含めて処理が分かれることを理解する。 | [表示](chapters/02/assets/revision-ill-get-post-routing.png) |
| HTMLのname属性値とFormのフィールド名の対応 | 02・54p | inputのtypeとnameを区別し、name属性値からFormの同名フィールドへ値が渡る関係を示す。 | [表示](chapters/02/assets/revision-ill-form-name-binding.png) |
| user.idをキー名とフィールド名に分けて読む | 02・60p | ModelのキーとFormのフィールドを混同せず、ドットの前後を別の段階として理解する。 | [表示](chapters/02/assets/revision-ill-model-key-property.png) |
| Repositoryの宣言から使える実装オブジェクトが用意される | 03・78p | インターフェースを書いただけなのにfindAllやsaveを使える理由を、宣言と実体の区別で説明する。 | [表示](chapters/03/assets/revision-ill-repository-implementation.png) |
| メソッド名と引数が検索条件になる | 03・97p | 命名ルールを暗記するだけでなく、メソッド名のプロパティと引数の値がどう条件になるかを理解する。 | [表示](chapters/03/assets/revision-ill-query-method-name.png) |
| redirectはブラウザーからの新しいリクエストを生む | 03・124p | returnでController内の別メソッドを直接呼ぶことと、ブラウザーを介したredirectの違いを正しくイメージする。 | [表示](chapters/03/assets/revision-ill-redirect-new-request.png) |
| ModelとHttpSessionではデータを渡す範囲が違う | 04・143p | 既存p143-f08は完成画面とModelコードの例。既存追加図session-separationはセッションIDと利用者ごとの分離。新図はリクエストをまたぐ保存期間だけを対比する。 | [表示](chapters/04/assets/revision-ill-model-session-lifetime.png) |
| 入力値と入力エラーを同じ画面へ戻す | 04・153p | 既存validation-branchは成功/失敗の分岐だけ。新図はエラーで戻った画面に値とメッセージが再表示される理由を説明する。 | [表示](chapters/04/assets/revision-ill-form-error-roundtrip.png) |
| null・空文字・空白だけの文字列は同じではない | 04・157p | p157-f18は多数のアノテーション一覧表。新図は特に誤りやすい3種類の空の状態を具体的な容器で比較する。 | [表示](chapters/04/assets/revision-ill-null-blank-constraints.png) |
| タグに見える入力を文字として表示する | 05・169p | p167-f02はth:textの構文とXSSへの短い言及。新図はエスケープが文字列の見え方をどう変えるかに限定する。 | [表示](chapters/05/assets/revision-ill-text-escape.png) |
| リンクのURLに含めたIDを引数へ取り出す | 05・174p | 既存p173-f07/p174-f08は実ブラウザーとコード。新図はURL末尾の値がJava引数へ対応する1対1の関係を抽出する。 | [表示](chapters/05/assets/revision-ill-dynamic-url-id.png) |
| プロジェクト内の保存場所とブラウザー用URLを区別する | 05・179p | p178-f11はEclipseフォルダー画面。新図は保存場所と公開URLの対応、staticをURLに付けない理由を視覚化する。 | [表示](chapters/05/assets/revision-ill-static-public-path.png) |
| mappedByのフィールド名とJoinColumnの列名を区別する | 06・201p | p195-f02はアノテーションのコード、既存foreign-key-referenceはFK値とオブジェクト参照。新図は2つの属性に指定する名前の名前空間を区別する。 | [表示](chapters/06/assets/revision-ill-relationship-field-column.png) |
| 参照先がある場合だけ次のフィールドを読む | 06・206p | p206は2方式の構文のみ。既存foreign-key-referenceの「参照先がある場合」に対し、参照先なしで途中のドットアクセスを止める必要を示す。 | [表示](chapters/06/assets/revision-ill-null-reference-guard.png) |
| 選択肢の表示名と送信する値は異なる | 06・218p | p213-f10はselectとEntityのコード。p218はテキストのみなので、th:textとth:valueが別の役割であることを具体例で示せる。 | [表示](chapters/06/assets/revision-ill-select-label-value.png) |
| JPQLではJava側の名前を使う | 06・225p | p225-f16は構文の箇条書き。新図はSQL/DBの列名に慣れた学習者が混同する2つの名前空間を視覚的に分離する。 | [表示](chapters/06/assets/revision-ill-jpql-entity-names.png) |
| 商品をカテゴリ別にまとめて集計する | 06・233p | p233〜235はDTOと集計コード/表のみで、グループ化の途中状態の図がない。データをまとめる段階と集計済み結果を分離して理解できる。 | [表示](chapters/06/assets/revision-ill-groupby-aggregate-dto.png) |
| CSS・JSをどこから読み込むか | 07・245p | CDNとローカルを2つの設定手順として暗記せず、ブラウザーへ届くファイルの取得元の違いとして理解する。 | [表示](chapters/07/assets/revision-ill-cdn-local-delivery.png) |
| マージンは枠の外、パディングは枠の内 | 07・259p | mとpの違いを、コードやブラウザー色だけに頼らず同じ要素の境界で理解する。 | [表示](chapters/07/assets/revision-ill-spacing-box-model.png) |
| container・row・colの入れ子 | 07・265p | HTMLの閉じタグが連続すると見失いやすい親子関係を、空間の包み込みとして理解する。 | [表示](chapters/07/assets/revision-ill-grid-containment.png) |

## そのほかの9点とDI図

| 挿絵 | 章・元頁 | 画像 |
| --- | --- | --- |
| pom.xmlの指定から必要なライブラリをそろえる | 01・28p | [表示](chapters/01/assets/revision-ill-maven.png) |
| Modelを使ったデータの受け渡し | 02・58p | [表示](chapters/02/assets/revision-ill-model.png) |
| th:eachの変数名とModelのキー名 | 03・87p | [表示](chapters/03/assets/revision-ill-each-variable-key.png) |
| 識別IDとサーバー側のセッション保存 | 04・142p | [表示](chapters/04/assets/revision-ill-session.png) |
| 入力チェックの成功とエラーの分岐 | 04・148p | [表示](chapters/04/assets/revision-ill-validation.png) |
| 共通レイアウトと画面ごとの内容を組み合わせる | 05・181p | [表示](chapters/05/assets/revision-ill-layout.png) |
| DBの外部キー値とJavaのオブジェクト参照 | 06・201p | [表示](chapters/06/assets/revision-ill-foreign-key.png) |
| 横幅によって左右配置から上下配置へ切り替わる | 07・269p | [表示](chapters/07/assets/revision-ill-responsive.png) |
| 外側の例外から原因と自分のコードをたどる | appendix-b・291p | [表示](chapters/appendix-b/assets/revision-ill-errors.png) |
| 依存性の注入 | 03・80p | [表示](chapters/03/assets/revision-di-remote.png) |

## 保存と生成記録

画像は組み込みimage_genで生成し、各章のassetsへ保存しています。正確な生成プロンプト、元出力パス、最終画像のSHA256、配置元頁・ID・キャプションは[カタログ](illustrations.json)に記録しています。今回の指示でname属性図を差し替え、Repository返り値図を削除し、th:each図を追加しました。

元頁は配置元の原本ページ番号です。現在のPDFの物理ページ番号は、組版後の検証記録で確認します。
