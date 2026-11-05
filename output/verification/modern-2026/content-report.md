# メッセージ参考欄・付録Bの内容改訂

結果：pass。変更は04と付録Bだけ。

第4章の元161頁末尾へ、固定文言の共通化、標準と言語別ファイル（ja/en/ko）、UTF-8、Locale、ThymeleafとMessageSourceの取得例を追加した。既存説明・図版は保持。各コードには右上のファイル名表示用filename属性を付けた。

付録B元291頁には、Pleiadesコンソールでの例外名/メッセージ/Caused by/自分のコードの行番号の読み方と、テンプレート・SQL・HTTP状態コードの切り分けを追加した。既存p291-b06/b07/b08だけは、コンパイルと実行の混同・テンプレート未解決を404とする誤りを許可範囲で訂正した。

追加指示の04/p150-b06は、@NotNullが現コードの11行目にあるため、数字10→11だけ訂正した。

## 動作確認

Java21＋配布spring_answer_2のBoot4.0.2ライブラリで独立アプリを起動し、13検査が合格した。配布プロジェクトは未編集、JVMはfinallyで停止済み。

- ja/en/ko/frのLocaleごとにMessageSourceとThymeleafで同じキーを解決。
- 言語別ファイルにないキー、および対応言語ファイルがないfrは標準文言へ補完。
- 不明URL404、POST先不一致405、テンプレート未解決500、意図的なSQL例外500を実HTTPで確認。
- TemplateInputException / Error resolving template / Caused byの例外連鎖を実ログで確認。

構造監査では既存ID・図ID・元ページ順序、baseline/source-layoutを保持。旧本文の差は許可された4IDのみ。並行担当によるp136-f02のコメント色修正用clean.svg参照だけは別途許可済みの差として記録し、SVG外寸・viewBox不変も確認した。

## 追加ID

- 04: `revision-messages-bundles`、`revision-messages-controller`、`revision-messages-en`、`revision-messages-fallback`、`revision-messages-files`、`revision-messages-html`、`revision-messages-ja`、`revision-messages-java`、`revision-messages-locale`、`revision-messages-purpose`、`revision-messages-settings`、`revision-messages-settings-note`、`revision-messages-thymeleaf`、`revision-messages-title`
- appendix-b: `revision-errors-console`、`revision-errors-name`、`revision-errors-sql`、`revision-errors-status`、`revision-errors-template`、`revision-errors-title`、`revision-errors-trace`、`revision-errors-trace-intro`、`revision-errors-trace-read`

## 組版引き継ぎ

- revision-messages-*14IDを保持して短縮。settings/controllerはparagraphへ変更し、標準/ja/en各2行＋HTML1行の4カードだけを残した。root目視で最新38頁の1ページ枠内に全14IDが収まった。
- 元291頁だけnative対象から外す設定はrootが担当。292〜296頁の固定配置と291末尾→292冒頭の既存継続文はそのまま。
- rootが最終PDF生成・目視を担当。04参考欄は1ページ内に収まったとの確認を受領。

## 確認範囲

- コンソール例は読み方を示すための省略例で、行番号は説明用。
- 最終参考欄は1ページを目指して短縮し、新しいエンドポイントのJavaコードや設定カードは掲載していない。13件のHTTP検証は文言解決・Locale・エラー状態の根拠となる独立アプリの結果。
- SQL例のruntime検証は意図的な例外生成であり、実DBの障害再現ではない。
- 標準Tomcatログではroot causeだけが直接表示される場合も実測し、Caused byがない場合の読み方を補足した。
- 紙面の翻訳コード例は標準/ja/en。messages_ko.propertiesとkoの関係は本文で説明し、実検証ではkoのUTF-8韓国語も表示確認。

## 公式一次資料

- [Spring Boot 4.0.2 MessageSourceProperties](https://github.com/spring-projects/spring-boot/blob/v4.0.2/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/context/MessageSourceProperties.java)：basename=messages、encoding=UTF-8、既定のシステムLocale fallbackとfalse指定の意味。
- [Spring Boot 4.0.2 MessageSourceAutoConfiguration](https://github.com/spring-projects/spring-boot/blob/v4.0.2/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/context/MessageSourceAutoConfiguration.java)：標準messages.propertiesの存在による自動設定、ResourceBundleMessageSourceへの設定適用。
- [Spring Boot 4.0 Internationalization](https://docs.spring.io/spring-boot/4.0/reference/features/internationalization.html)：言語別ファイルのみでは自動設定されず標準ファイルが必要。表示時点の4.0系最新版のため、固定版仕様は上記v4.0.2ソースで照合。
- [Java SE 21 Locale](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Locale.html)：言語コードja/enとLocaleの役割。韓国語Locale.KOREANはko。
- [Thymeleaf 3.1 / Spring integration](https://www.thymeleaf.org/doc/tutorials/3.1/thymeleafspring.html#listing-seed-starter-data)：Spring MessageSourceを使った#{key}による文言取得。
- [Spring Framework MessageSource API](https://docs.spring.io/spring-framework/docs/7.0.3/javadoc-api/org/springframework/context/MessageSource.html)：getMessage(code,args,locale)の引数。
- [Spring Boot 4.0.2 WebProperties / WebMvcAutoConfiguration](https://github.com/spring-projects/spring-boot/blob/v4.0.2/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/web/WebProperties.java)：Locale解決の既定はaccept-header。WebMvcAutoConfigurationでもAcceptHeaderLocaleResolverを生成することを確認。
- [Spring MVC method arguments](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/arguments.html)：ControllerのLocale引数は現在のリクエストLocale。
- [Java SE 21 Throwable](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html#printStackTrace())：例外名・メッセージ・at行・Caused byの原因連鎖の形式。
- [Thymeleaf TemplateInputException API](https://www.thymeleaf.org/apidocs/thymeleaf/3.1.3.RELEASE/org/thymeleaf/exceptions/TemplateInputException.html)：テンプレート名、行、列、causeを保持できること。未解決時の500は実HTTPでも確認。
- [Spring Framework 7.0.3 HttpRequestMethodNotSupportedException](https://github.com/spring-projects/spring-framework/blob/v7.0.3/spring-web/src/main/java/org/springframework/web/HttpRequestMethodNotSupportedException.java)：メソッド不一致時の405。404/405/500は実HTTPでも確認。
- [MySQL 8.0 接続障害の切り分け](https://dev.mysql.com/doc/refman/8.0/en/problems-connecting.html)：Access deniedに対するユーザー・パスワード・接続元/権限の確認。
- [MySQL Connector/J troubleshooting](https://dev.mysql.com/doc/connector-j/en/connector-j-usagenotes-troubleshooting.html)：Communications link failureを接続/通信状態の確認の手掛かりとする。
- [Eclipse JDT Stacktrace Console](https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/reference/views/console/ref-stacktrace_console.htm)：スタックトレースのリンクからソース位置へ移動する機能。

実行結果：`content-example-verification.json`、実ログ：`content-example-runtime.log`、変更前原稿：`04-before-content.md` / `appendix-b-before-content.md`。
