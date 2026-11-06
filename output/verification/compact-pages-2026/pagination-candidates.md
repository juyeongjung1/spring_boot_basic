# 改ページ候補の独立調査

## 元頁境界の候補

|冊子・章|元頁|現頁|前頁使用率|直前末尾|次の先頭|保護|
|---|---:|---:|---:|---|---|---|
|textbook front|2|1|0.0%|~サーブレット&JSP からのステップアップ~|商標|True|
|textbook front|3|1|0.0%|T CAMP、NEW TRAIN、MIX TRAIN、TRAINOCAMP は、トレノケート株式会社の登録商標です。その他の会社名、製品名およびサービス名は、それぞれ各社の商標または登録商標です。|目 次|True|
|textbook front|13|1|0.0%|If command1 returns success, command2 runs$ ls –l sample.txt|◼ UNIX とLinux 関連のテキストでの表記|True|
|textbook 01|23|25|43.6%||3. Bean の自動設定|False|
|textbook 01|25|27|98.9%|、ライブラリ間の参照関係やバージョンの整合性を手動で管理する必要があり、非常に面倒です。さらに、プロジェクトを他の開発者と共有する際も、全てのライブラリファイルを含める必要があるため、非効率です。|「Maven」や「Gradle」といったビルドツールを利用することで、問題を解決できます。これらのツールを使うと、必要なライブラリをプロジェクトの設定ファイルに記述するだけで、ツールが自動的にライブラリをダウンロードし、参照関係を管理してくれます。このおか|False|
|textbook 02|35|37|96.7%|一方で、「レスポンス」とはサーバーがリクエストに応じてブラウザに返す応答のことを指します。これは通常、HTML 形式のWeb ページとして表示され、ユーザに情報が送られます。|例えば、オンラインの服のショッピングサイトを訪れて、特定のブランドの服や靴を探しているとします。検索ボックスに「夏のファッション」と入力して検索ボタンをクリックします。これが「リクエスト」です。|False|
|textbook 02|41|43|54.3%||…/controller/IndexController.java|False|
|textbook 02|44|47|41.7%|今回のreturn は、サーブレットのrequest.getRequestDispatcher と似た役割をするコードだと覚えると良いでしょう。|Spring のreturn は、正確にはforward をしているのではなく、「指定したHTML ページを呼び出す」に近いですが、MVC パターンでの画面出力という観点では似ています。|False|
|textbook 02|45|49|35.5%|[トップページ]と表示される部分（10 行目）からは、ユーザに見える画面の内容が入ります。今後、さまざまな情報やデザイン要素を追加していくことになります。|【作業手順③】Spring Boot アプリケーションの実行|False|
|textbook 02|46|51|26.9%||【参考】 application.properties ファイルについて|False|
|textbook 02|48|54|7.1%|では、直接HTML ページを開くのではなく、Controller のメソッドを経由させます。よって、実装時は HTML ファイルより先に、画面遷移の処理のみを持つメソッドを作成する必要があります。|【作業手順①】ログイン画面を表示するメソッドの作成|False|
|textbook 02|49|56|7.0%|一般的に、Spring では、コントローラーのメソッドを経由してHTML ページを呼び出します。この手法により、URL とビューとの間に明確な対応関係を持たせ、アプリケーションの構造を整|理しやすくなります。また、必要に応じて追加のデータ処理やビジネスロジックをメソッド内に組み込むことが可能です。|False|
|textbook 02|50|58|38.9%|なGET 方式の送信ではなく、POST 方式の送信をするという意味です。POST 方式にすると、パスワードがURL に表示されないなどのメリットがあり、隠したいデータを送信する時によく使われます。|・11 行・12 行目 <input type = “text” name = “パラメータ名”>|False|
|textbook 02|52|61|43.6%|メータを受け取ることができます。login_input.html では、「id」と「password」のデータが送られるので、引数名も、int id, String password に合わせます。|【参考】サーブレットでパラメータを受け取る方法|False|
|textbook 02|54|65|31.1%||その後、[form]パッケージに、[UserForm]というクラスを作成します。|False|
|textbook 02|59|73|26.4%|UserForm の時と同様に、Spring ではメソッドの仮引数にオブジェクト名を書くと、オブジェクトを生成しなくても、使うことができます。|・14-15 行目 model.addAttribute("user", userForm);|False|
|textbook 02|62|78|49.4%|これにより、サーバーサイド(Controller)のロジックとView(HTML)の表示を分離しながら、動的なWeb ページを作成することが可能になります。|章のまとめ|True|
|textbook 03|68|85|42.8%|00004 2 ドア冷蔵庫 500005 コンパクト冷蔵庫 150006 ワインクーラー 300007 全自動洗濯機 250008 乾燥機能付き洗濯機 400009 洗濯乾燥機 60000|【参考】既存のJDBC 接続(Java+MySQL)方法と問題|False|
|textbook 03|71|90|46.4%||【作業手順②】接続情報の設定|False|
|textbook 03|74|94|99.0%|public class Product {    private Integer id;    private String name;    private Integer price;}|このコードにおいて、@Entity アノテーションはこのクラスがエンティティクラスであることを示し、@Table アノテーションは実際のテーブル名を指定します。その後、テーブルの各列を型に合わせて定義します。この例では、id、name、price が該当し|False|
|textbook 03|75|96|27.1%||【作業手順③】 制約をアノテーションで表現|False|
|textbook 03|80|103|10.9%|@AutowiredProductRepository prodRepo;|Spring では、いくつかの依存性の注入方法があります。一番簡単な方法は、上記のように、フィールドへ直接注入する方法があります。|False|
|textbook 03|88|113|34.5%|el で格納したキー名、左はリストの中に格納されているものを意味する変数名を使います。今回は、リストの中に、複数のproduct インスタンスが格納されているため、「product」としました。|9-11 行目 <td th:text="${product.id}">、<td th:text="${product.name}">～～|False|
|textbook 03|89|115|9.7%|い表形式で表示するために使用されます。Thymeleaf のth:each を使用することで、リストの各要素に対してテーブルの行が自動的に生成され、リスト内のデータが簡単かつ効率的に表示されます。|動作確認|False|
|textbook 03|93|120|17.4%|View から送信される主キーのname 属性が「id」ですので、引数名を一致させることで、リクエストパラメータを取得します。|5 行目 Product product = prodRepo.findById(id).orElse(null);|False|
|textbook 03|94|122|24.3%|product フォルダに、[detail.html]を作成します。|…/resources/templates/product/detail.html|False|
|textbook 03|97|126|92.8%|一見、インターフェースに抽象メソッドを記載しただけに見えますが、リポジトリは、決まったルール通りのメソッド名を合わせるだけで、本当にその処理をするメソッドを裏で作ってくれます。|例えば「findBy[エンティティのフィールド名](入力値の変数)」というルールに合わせれば、|False|
|textbook 03|98|128|39.8%|findAll メソッドを実行した時と、出力結果は同じくList になるメソッドですので、6 行以降はshowProductList メソッドと全く同じです。|動作確認|False|
|textbook 03|101|132|1.8%|という SQL 処理をするメソッドが裏で完成されます。|product テーブルには同じ名前で同じ価格を持つ商品が複数存在する可能性があるため、このメソッドの戻り値はリスト形式になっています。もし、検索結果が複数行にならない条件検索をしたいなら、戻り値を「Product」のような、エンティティ型にすれば良いです|False|
|textbook 03|102|134|11.5%|例：ｆindByNameOrPriceAndId|動作確認|False|
|textbook 03|109|142|27.1%||【作業手順④】 登録処理メソッドの定義|False|
|textbook 03|110|144|45.0%||・8 行目: product = prodRepo.save(product);|False|
|textbook 03|111|146|56.4%|・10 行目: return "/product/result";本当に登録が完了したのか確認するために、商品データを出力する結果画面を表示させます。|…/resources/templates/product/result.html|False|
|textbook 03|115|151|89.8%|ing Data JPA はUPDATE 文を実行します。ここで重要なのは、主キーがすでに割り当てられているエンティティは、データベースにすでに存在しているとみなされるため、更新処理が行われます。|このアプローチは、コードの再利用性を高め、データベース処理をより直感的に行えるようにします。特に、開発者が明示的にINSERT やUPDATE を意識する必要がなく、エンティティの状態に応じてSpring が適切な処理を自動的に行ってくれるため、開発効率が|False|
|textbook 03|119|156|10.6%|「修正」のsubmit ボタンをクリックすると、フォーム内の入力データ値が全てリクエストパラメータとして/product/update のURL へ送信されます。|【作業手順④】 修正処理メソッドの定義|False|
|textbook 03|124|162|96.1%|本当に削除が完了したのか確認するために、全件検索ページを呼び出したいところですが、全件検索は、html ファイルではなく、findAll メソッドを実行していました。|つまり、returnでhtmlではなく、メソッドを呼び出すURLを指定する必要があるということです。|False|
|textbook 03|129|168|90.1%|: public Product findProductById(int id) {14: return prodRepo.findById(id).orElse(null);15: }16:}|・5 行目： @Serviceサービス実装クラスには、@Service アノテーションを付けます。忘れがちですので、注意してください。|False|
|textbook 03|131|171|48.2%|troller のメソッドの中で直接「prodRepo.メソッド」を実行する書き方でしたが、今回はServiceクラスに定義されているメソッドを実行させて、その戻り値を利用する書き方になりました。|「ProductService」インターフェース型のインスタンスからメソッドを呼び出していますが、「ProductServiceImpl」クラスに具体的な処理がオーバーライドされているので、実際は「ProductServiceImpl」のメソッドがポリモフ|False|
|textbook 04|137|178|23.8%|emp_id password emp_name123456 pass1234 山田太郎234567 pass2345 佐藤花子345678 pass3456 鈴木一郎|【事前準備①】 エンティティの定義|False|
|textbook 04|138|180|38.0%|エンティティの次は、リポジトリです。3章の定義方法と同様ですので、説明は割愛いたします。|【事前準備③】Form クラス定義|False|
|textbook 04|141|184|17.9%|<!--省略--><body><h1>メイン画面</h1>ログインに成功しました。</body>|動作確認|False|
|textbook 04|144|188|27.0%|Model については、3 章の「findAll メソッドでの全件検索」を参照してください。|【作業手順①】 HttpSession 直接利用する方法|False|
|textbook 04|145|190|48.9%|ドが実行されると、セッションスコープの中に、"userData"という名前でログインユーザの全情報を保持できるようになります。このデータは、画面が変わっても、システム全域で呼び出すことができます。|【作業手順②】 セッションスコープ内のデータを参照する方法|False|
|textbook 04|152|199|45.5%|エラーの詳細を取得するために使用されます。通常、メソッドの引数として渡されます。必ず、@Valid をつけた直後(ここでは、第2 引数)に記載しないといけないルールがありますので、ご注意ください。|・4 行目 bdResult.hasErrors()：|False|
|textbook 04|153|201|40.7%|、*{...}という選択式を使用して、userForm オブジェクトのプロパティに簡潔にアクセスできます。userForm.empId ではなく、*{empId}だけでアクセスできるようになります。|・6 行目 th:field="*{empId}":|False|
|textbook 04|154|203|52.6%||② 入力エラーメッセージが表示されます。|False|
|textbook 04|156|205|71.9%|      <span th:errors="*{password}"></span></p><input type="submit" value="ログイン"></form></body>|…/controller/LoginController.java|False|
|textbook 04|160|211|1.6%|Spring では、メッセージをカスタマイズできるファイルを別途作成できます。|messages.properties の作成|False|
|textbook 05|169|222|9.7%|えば、データベースから取得した情報やユーザ入力）をWeb ページに表示する際に用います。<td></td> タグ内のテキストは、th:text 属性に指定された式の結果によって置き換えられます。|th:text の特徴の一つは、クロスサイトスクリプティング（XSS）の対策です。例えば、ユーザが「<script>悪質なJavaScript コード</script>」 というデータを入力した場合、XSS対策が施されていないと、この悪意のあるJavaSc|False|
|textbook 05|174|227|98.7%|duct} + ${product.id} + @{.png},         alt=${product.name}, width=60, height=60" />  </td></tr>|…/controller/ProductController.java|False|
|textbook 05|176|230|97.9%|00 以下の場合、通常のスタイルで価格を表示 --><td th:unless="${product.price > 30000}"th:text="${product.price}"></td>|この例では、product.price の値が30000 を超えるかどうかで、スタイルが適用された価格と、通常スタイルの価格を切り替えて表示しています。HTML コードは2行ですが、条件に合うコードだけが表示されるようになっています。|False|
|textbook 05|177|232|20.2%|<div th:unless="${#lists.isEmpty(products)}">    <!-- 商品情報リストの内容(<table>～</table>)をここに記載 --></div>|⑷ 日付や時間に基づくコンテンツの表示：|False|
|textbook 05|180|236|13.2%|JavaScript でHTML を生成することもできます。|動作確認|False|
|textbook 05|182|239|1.6%|それでは、Thymeleaf でのレイアウトの作成方法について詳しくご説明します。|目標画面|False|
|textbook 05|184|241|93.1%|3:<p>Copyright © 2027 Trainocate Spring. All rights reserved.</p>34:</footer>35:</body>36:</html>|このlayout.html には、Web サイトの共通要素であるヘッダー、ナビゲーションバー、フッターが定義されています。注目すべき3 つの箇所をご説明します。|False|
|textbook 05|185|243|46.9%|修正するHTML ファイルは、商品関連のどのHTML ファイルでも構いません。|・3 行目 xmlns:layout=”http://www.ultraq.net.nz/thymeleaf/layout”|False|
|textbook 05|190|250|36.4%|ainer {    min-height: 0; /* フレックスコンテナのmin-height をリセット */}body > footer {    flex-shrink: 0;}|章のまとめ|True|
|textbook 06|201|262|1.6%|しかし、category_id ではなく、「Category category」 のフィールドを定義しています。|JPA では、外部キー（例: category_id 列）を直接操作せず、リレーション先のエンティティ（例:Category）をフィールドとして扱います。これにより、オブジェクト指向の設計とデータベース操作を統一できます。|False|
|textbook 06|202|264|41.4%|これにより、テーブル間のリレーションシップがSpring上で明確に定義され、データベース操作が容易になります。|【作業手順④】 CategoryRepository の作成|False|
|textbook 06|207|270|43.0%|条件がfalse の場合に右側の値（'未設定'）を表示します。|動作確認|False|
|textbook 06|210|273|44.2%|もちろん、エンティティ間の定義が完了しているので、findById でも結合した結果を取得できます。|【作業手順②】 商品が見つからなかった際の表示の切り替え|False|
|textbook 06|211|274|88.2%|このように、複数行のThymeleaf 条件式は、視認性や保守性を高めるために<div></div>を使用することを推奨します。|※単体のデータの有無ではなく、リスト内の判定については、5.1.2 の➁を再度ご確認ください。|False|
|textbook 06|212|275|26.5%|<div th:unless="${#lists.isEmpty(products)}">    <!-- 商品情報リストの内容(<table>～</table>)をここに記載 --></div>|動作確認|False|
|textbook 06|215|279|100.7%|ption>                       <option value = "4">洗濯機</option>               </select>        </p>|このように固定値を記載する方法は簡単ですが、以下のような問題点があります。|False|
|textbook 06|217|281|88.4%|カテゴリリストをfindAll()メソッドで取得します。|⚫ model.addAttribute:|False|
|textbook 06|218|282|16.9%|これで、登録画面へカテゴリのリストの送信ができましたので、登録画面のView を実装しましょう。|【作業手順③】 カテゴリのリストの動的表示|False|
|textbook 06|226|291|7.9%|• メソッド名の命名規則が不要JPQL を使用する場合、自由にメソッド名を設定できます。|全件検索の実装|False|
|textbook 06|227|292|87.3%|SQL とほぼ同じ構文ですが、SELECT 句やWHERE 句でテーブルではなくエンティティを扱うことを意識しましょう。|次は、コントローラーの全件検索用メソッドで、呼び出すメソッドを「findAll」から、「findAllProducts」に変更します。|False|
|textbook 06|229|294|101.4%|JPQL では、:id のような名前付きパラメータを使用します。番号ではなく、パラメータ名と引数名を一致させることで紐付けされるため、直感的で扱いやすいのが特徴です。|…/controller/ProductController.java|False|
|textbook 06|230|295|35.7%|http://localhost:8080/product/ でID 検索の動作確認をすると、同じ主キー検索ができるのが確認できます。|名前のLIKE 検索と価格のAND 検索の実装|False|
|textbook 06|231|297|4.3%|ローラーでは、既存のfindByNameAndPrice メソッドの代わりに、JPQL で新たに定義したfindByNameContainingAndPrice メソッドを呼び出すように修正します。|動作確認|False|
|textbook 06|234|301|50.8%|    return categoryName;    }    public Long getTotalSales() {        return totalSales;    }}|■カテゴリごとの商品数を受け取るDTO|False|
|textbook 06|236|304|26.8%|gory.namefindCategoriesByMinSales(LongminSales) 価格の合計が指定値以上のカテゴリを取得 HAVING SUM(price) >=minSales|章のまとめ|True|
|textbook 07|243|311|81.5%|スマホやタブレット、PC で異なるレイアウトを実装する必要があり、工数が増えます。|Bootstrap での解決|False|
|textbook 07|244|313|21.1%||Bootstrap を使うメリット|False|
|textbook 07|247|317|4.3%|Bootstrap をWeb サイト内で利用したいなら、上記のコードは必須です。URL は、公式ホームページからお勧めのURL を参照することができます。|ローカル(Spring プロジェクト内) からの導入|False|
|textbook 07|248|318|99.1%|html ファイルに遷移させるために、遷移用メソッドを定義します。|…/resources/templates/bootstrap_setup.html|False|
|textbook 07|249|320|29.5%|Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"crossorigin="anonymous"></script></body></html>|サンプルコードには、両方の方法を記述していますが、実際は CDN とローカルのうち、どちらかのみ記述してください。本研修では、ローカルからの読み込みを採用します。|False|
|textbook 07|253|324|96.7%||◼ 背景色|False|
|textbook 07|255|327|84.1%|※btn-link は見た目がリンクのようになります。※<button>だけでなく、<input>や<a>タグにも適用可能です。|◼ ボタンのサイズbtn クラスに加えて、サイズを指定するクラスを追加することで、大きなボタンや小さなボタンを作成できます。|False|
|textbook 07|258|330|79.1%|※<hr>は、水平線を引く要素です。余白の範囲の参考のため記述されています。（デフォルトで少しの上下の余白が生成されます）|要素の余白を簡単に調べられる方法についてご紹介します。|False|
|textbook 07|259|331|57.9%||◼ パディング（Padding）|False|
|textbook 07|261|334|94.5%||◼ 横幅(Width)の調整|False|
|textbook 07|266|340|30.6%|入れ子構造は、<table><tr><td>の関係と似ています。|基本的なグリッドレイアウト|False|
|textbook 07|267|341|93.0%|er">今回のサンプルでは、外側を container でコンテナを作っています。画面の中央にコンテンツが配置されます。もし、container-fluid にすると、横幅いっぱいに変わります。|・2 行目 <div class="row"> コンテナの中に、row をclass 属性として持つdiv 要素を入れます。後述のカラムを配置するためにも、必ずrow が必要です。まるでtable 要素に、<tr>がないと、<td>も書けないのと同じで|False|
|textbook 07|268|343|21.4%|・g-1 (g-5 まである) をrow クラスに加えると、カラム同士の間隔を調整できます。微調整することが多いので、覚えておいてください。|■動作確認|False|
|textbook 07|269|344|25.6%|※より詳しい構文は、https://getbootstrap.jp/docs/5.3/layout/grid/ を参照。|【参考】 グリッドシステムの応用|False|
|textbook 07|270|345|100.7%|col-md-3／col-md-9では、幅768px以上は横並び、それ未満はサイドバー・本文の順に縦に並びます。|…/resources/templates/grid_sample2.html|False|
|textbook 07|271|347|20.2%|"container-fluid bg-dark text-white text-center py-3">    <p>フッター</p></div> <!-- END container3-->|■動作確認|False|
|textbook 07|273|349|95.3%||…/resources/templates/form_sample.html|False|
|textbook 07|274|351|59.6%|・10 行目 <input type="text" class="form-control"～|Bootstrap のフォーム関連クラスの中で、一番大事なクラスです。テキストフォームにこのクラスを付与することで、Bootstrap 式のテキストフォームのデザインを適用することができます。|False|
|textbook 07|279|358|20.2%|     </div> <!-- END form column -->    </form> <!-- END form row --></div> <!-- END container -->|■動作確認|False|
|textbook appendix-a|283|361|0.0%|付録 A 環境構築手順|Import 手順|True|
|textbook appendix-a|287|361|45.3%|ng.io」で管理していますので、常に最新のSpring Boot のバージョンと互換性があります。その分、新規プロジェクト作成時は、過去のバージョンは選択できなくなりますので、注意が必要です。|Spring Boot の「Spring Initializr」で新規Spring プロジェクトを作成する方法をご説明します。|True|
|textbook appendix-a|289|361|103.6%||「ADD DEPENDENCIES」をクリックし、|True|
|textbook appendix-b|291|370|0.0%|付録B よく起きるエラーまとめ|404 エラーが出る場合：|True|
|textbook appendix-b|292|369|19.4%|5. Thymeleaf の式に誤りはありませんか？ Thymeleaf では、${...}や*{...}などの式を使ってオブジェクトのプロパティにアクセスしま|す。これらの式に誤った構文や存在しないプロパティを参照していると、エラーが発生します。|True|
|textbook appendix-b|295|369|99.5%||インポートエラーが出る場合は、ここにあるファイルがエラーの原因になる可能性がありますので、repository フォルダを削除してください。その後、インポートし直してください。|True|
|textbook appendix-b|296|369|0.0%|に、講師の方から研修中に使用するライブラリが入っているrepository フォルダをまとめて配布しますので、こちらのrepository フォルダにコピーを行ってからインポートを行ってください。|無断複写・複製の禁止本書は著作権法上の保護を受けています。Spring Boot 入門本書の全部または一部を無断で複写複製することは~サーブレット&JSP からのステップアップ~禁じられています。|True|
|exercise ex-front|2|1|0.0%|演習ガイド|商標|True|
|exercise ex-front|3|1|0.0%|T CAMP、NEW TRAIN、MIX TRAIN、TRAINOCAMP は、トレノケート株式会社の登録商標です。その他の会社名、製品名およびサービス名は、それぞれ各社の商標または登録商標です。|目 次|True|
|exercise ex-front|4|1|0.0%|オプション】Service クラスの利用 ............................................................................ 28|演習 4 セッションと入力チェック ......................................................................... 29|True|
|exercise ex-front|5|1|0.0%|Bootstrap 導入前後の変化を確認 ............................................................................ 67|演習 7.2. Bootstrap の基本スタイルの適用 ............................................................................. 68|True|
|exercise ex01|8|8|0.0%|演習 1  Spring Boot と開発環境の概要|演習の目標|True|
|exercise ex02|12|12|0.0%|演習 2  Spring Web アプリケーション|演習の目標|True|
|exercise ex03|18|18|0.0%|演習 3  Spring Data JPA|演習の目標|True|
|exercise ex03|22|23|79.1%|⚫ 遷移先は、「emp_list.html」です。|e. emp_list.html にmodel 内のデータを出力してください。|False|
|exercise ex03|24|25|87.4%|⚫ 遷移先は、「emp.html」です。|e. emp.html にmodel 内のデータを出力してください。|False|
|exercise ex03|25|26|86.1%|⚫ 複数行の検索結果を取得する可能性があるため、戻り値型を List<Employee>にします。|c. EmpController クラスのshowFindBySalary メソッドの引数に、a.のname 属性値を追記してください。|False|
|exercise ex03|27|28|94.2%|⚫ action 属性値が[“insertEmp”]、method 属性値が[“post”]だということを覚えてください。|⚫ 3 つのテキストフォームがあり、それぞれname、password、salary のname 属性値が入っていることを覚えてください。|False|
|exercise ex04|30|31|0.0%|演習 4  セッションと入力チェック|演習の目標|True|
|exercise ex04|32|33|94.6%|⚫ この演習では、「empId」ではなく、「Id」です。間違えるとエラーが出ます。注意|c. LoginController のlogin メソッドの引数を入れてください。|False|
|exercise ex04|35|36|102.7%|⚫ この手順を書き忘れると、エラーが出ます。|c. LoginController のlogin メソッドの引数の部分を、入力チェックができるように修正してください。|False|
|exercise ex05|38|39|0.0%|演習 5  Thymeleaf とWeb デザイン|演習の目標|True|
|exercise ex05|40|41|101.2%||a. 以下のファイルのフォルダ構成と、ソースコードを確認してください。|False|
|exercise ex05|42|44|48.4%||◼ 4 章までのソースコードからの変更点|False|
|exercise ex05|43|45|73.7%| ※コンテンツになる html のデザインは、/css/main_style.css で担当しています。|g. templates/emp フォルダの中の全てのhtml ファイルの<body>以下のコードを<main>要素で囲って、layout:fragment 属性を付与してください。|False|
|exercise ex05|46|49|4.5%|a. emp_list.html の給与列は、ログインユーザの社員番号が 1001 の場合のみ表示するように修正してください。|⚫ テキスト 5.1.2 と、「②その他の条件式」の「⑵ 管理者権限に基づく機能の表示」を参考にしてください。|False|
|exercise ex06|48|51|0.0%|演習 6  外部参照と複雑な SQL 操作|演習の目標|True|
|exercise ex06|52|56|72.7%|ppedBy = "location") アノテーションを付けること。▪ mappedBy には、Employee エンティティ側で定義したフィールド名（"location"）を指定してください。|• フィールド名は、employeeList としてください。|False|
|exercise ex06|54|58|81.9%|ist.html ファイルを修正してください。• empList リストから、社員番号、社員名、給与、勤務地名を表示してください。• Thymeleaf のth:each 構文を利用してください。|【ヒント】|False|
|exercise ex06|58|62|98.4%|/showInputView にしてください。• 画面に <select> を表示するために、Location の全件を取得し、"locations" という名前でModel に格納してください。|【ヒント】|False|
|exercise ex06|61|65|62.4%||a. EmpController のshowSearchForm メソッドのソースコードを確認してください。|False|
|exercise ex06|62|66|88.5%|QL では、テーブル名ではなくエンティティ名を使います。)• location テーブルは @ManyToOne で結ばれているため、e.location.name のように書くことができます。|• WHERE 句には e.salary >= :salary AND e.location.name = :locationName のように書きます。• テキストの6.4.2 の部分を参考にしてください。|False|
|exercise ex07|64|68|0.0%|演習 7  Bootstrap|演習の目標|True|
|exercise ex07|66|70|49.0%|演習7.6 演習7.6. 【オプション】 共通レイアウト画面に変更：20 分|■事前準備（※操作不要）|False|
|exercise ex07|69|74|19.4%|• bg-light：全体を淡い灰色の背景色に• p-4：ページ内に十分な余白を追加|b. タイトル部分に装飾を加えてください|False|
|exercise ex07|71|77|5.2%| 今回の演習では、まず .table だけを付け、見た目の変化に注目します。| 補助的に .table-hover や .table-striped を後の演習で追加します。|False|
|exercise ex07|73|80|4.5%|い。|• 「全社員一覧」「詳細検索」「社員データ登録」のボタンが左側の縦方向に並ぶメニューとして表示されています。• その右側には、社員情報のテーブル一覧が表示されています。• 上記2 つのエリアが横に並んでいることを確認しましょう。• 演習URL は、lo|False|

## 同一元頁の小さい続きと画像縮小候補

|章|元頁|現頁|続きの高さ|必要節約|画像倍率目安|元図|
|---|---:|---|---:|---:|---:|---|
|01|22|23→24|291.77|24.27|87.4%|p022-f05|
|02|43|45→46|279.48|215.57|-365.6%|p043-f12|
|02|45|49→50|179.98|17.43|93.4%|p045-f15,p045-f16|
|02|48|54→55|47.04|19.99|87.6%|p048-f22|
|02|52|61→62|217.18|174.49|-21.1%|p052-f23,p052-f24|
|03|68|85→86|251.42|92.91|42.1%|p068-f03,p068-f04,p068-f05|
|03|78|99→100|295.06|194.48|-38.9%|p078-f14|
|03|87|111→112|230.81|73.06|18.4%|p087-f20|
|03|88|113→114|65.04|61.09|79.1%|p088-f21|
|03|92|118→119|116.81|43.4|28.5%|p092-f25|
|03|93|120→121|162.54|108.19|-156.6%|p093-f26|
|03|94|122→123|11.04|19.33|89.5%|p094-f28,p094-f29|
|03|100|130→131|11.87|26.71|64.4%|p100-f35|
|03|108|140→141|181.5|150.3|-35.3%|p108-f42|
|03|111|146→147|11.04|26.91|84.7%|p111-f46|
|03|118|154→155|71.04|77.78|65.6%|p118-f54|
|03|120|157→158|11.04|24.28|94.9%|p120-f55,p120-f56,p120-f57|
|03|124|162→163|138.54|157.98|46.3%|p124-f61,p124-f62|
|03|130|169→170|322.88|104.48|-72.1%|p130-f67|
|04|143|186→187|181.18|179.52|-11.2%|p143-f08|
|06|212|275→276|100.8|21.42|93.7%|p212-f07,p212-f08|
|07|243|311→312|141.06|54.02|32.4%|p243-f03|
|07|267|341→342|143.04|127.04|-694.0%|p267-f23|
|ex05|41|42→43|324.53|57.24|81.9%|p041-f04|
|ex05|45|47→48|29.87|29.36|94.4%|p045-f08,p045-f09|
|ex07|68|72→73|130.2|62.43|73.0%|p068-f03|
|ex07|70|75→76|35.04|57.28|79.4%|p070-f04|
|ex07|72|78→79|30.0|31.02|94.5%|p072-f05|
