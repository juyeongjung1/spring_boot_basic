# Java 21・Spring Boot 4.0.2への移行と検証

更新版27アプリ、本文248ページ・演習58ページの改訂PDF、targetを含めない配布ZIPを作成しました。Pleiades 2025の実m2e/JDTでも取り込み・ビルドを確認しています。

## 配布物

- [更新版プロジェクトと手順](../../projects/README.md)
- [配布ZIP](../../output/projects/SpringBootBasic_Java21_Boot4.0.2.zip)
- [本文の改訂PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習の改訂PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [教材の比較・組版検証](../textbook/verification.md)
- [機械検証の集計](../../output/verification/projects/summary.json)

元配布物にあった同内容の複製は、更新版では1コピーに整理しました。spring_answer 7、spring_exercise 7、enshu_answer 7、enshu_exercise 6の27アプリです。4グループの集約POMと全体集約POMを加えて、32POMを収録しています。配布ZIPは852ファイルで、target・classファイル・IDEワークスペースを含めていません。[SHA256と収録検査](../../output/projects/package-checks.json)も保存しています。

## 更新内容

| 対象 | 更新内容 |
| --- | --- |
| Spring Boot | 実POMの3.1/3.2/3.3系の混在を4.0.2へ固定 |
| Java | java.version、JDTのsource/target/complianceを21へ統一 |
| Web MVC | spring-boot-starter-webmvcと対応するテスト用スターター |
| MySQL Connector | 古い個別指定を外し、Boot 4.0.2の管理版9.5.0をruntimeで使用 |
| ModelMapper | Java 21対応の3.2.6へ更新。本文第3章はメソッド引数への暗黙生成を避け、明示的に生成 |
| IDE手順 | Pleiades 2025、JDK 21登録、Maven更新、アプリ単独実行を説明 |
| DB初期化 | SQLをUTF-8へ変換、UTF8MB4を明示。既存DBを削除する処理を含めず、作成エラーで停止 |
| 教材 | 固定4.0.2の作成、Jakarta Servlet、依存関係、URL/Java文字列/HTML引用符を改訂 |
| 記号 | 360箇所を通常の■・●・•へ正規化。絵文字フォントへの代替を防止 |

Bootの管理値は4.0.2の実BOMに合わせています。Hibernate 7.2.1.Final、Spring Framework 7.0.3、Thymeleaf 3.1.3.RELEASE、Layout Dialect 3.4.0、Lombok 1.18.42、JUnit 6.0.2、Tomcat 11.0.15です。Layout Dialectは管理版のまま、共通ヘッダー/フッターを実動作確認しました。

## 実行結果

| 検証 | 結果 |
| --- | --- |
| Java 21でのpackage | 27/27成功 |
| JUnitコンテキストテスト | 27/27成功、失敗・エラー・skip 0 |
| HTTP機能確認 | 本文79＋演習65＝144項目成功 |
| 実JARのクラス | 全27アプリがJava 21形式（major 65） |
| Pleiades m2e取り込み | 32/32 POM・プロジェクト |
| Pleiades JDTビルド | 27/27アプリ、生成182クラスがmajor 65 |
| IDEの引数名情報 | 全27アプリでmethod_parameters=generate |
| IDEのプロジェクトエラー | 0件 |
| PDFの回帰検証 | 10件成功 |
| 改訂PDFのコード | 192ブロックで原稿と順序付き文字列一致 |
| 合冊の描画 | 全306ページで番号更新領域以外の画素差・文字差0 |

Java実行はTemurin 21.0.13+9、Maven 3.9.9、MySQL 8.0.32で確認しました。検証用MySQLは独立したデータ領域・ポート13306で起動し、終了済みです。検証後、5テーブルの行の値が投入時のデータと全て一致し、テストレコードの残留がないことを確認しました。

HTTPではBMI、検索、通常/ModelMapper登録、更新・削除、ログイン・セッション、Validation、Thymeleaf共通レイアウト、管理者/一般社員の給与列表示、外部参照、JPQL、Bootstrapと静的ファイルを確認しました。

## Pleiadesの確認範囲

公式のPleiades 2025-12 Javaパッケージ（20260117、Standard）を検証用に展開し、外部のJDK 21を登録して使用しました。Eclipse 4.38.0.v20251201-0920、m2e 2.7.600.20251121-1832、Lombok 1.18.42です。授業向け手順では、開発用JDKを同梱するJava Full Editionを案内しています。

実m2eの取り込みAPIとJDTで、対象の一時コピーを新規ワークスペースへ取り込み、32プロジェクトの作成、Java 21設定、全27アプリのビルド、生成クラスと引数名情報、エラーマーカーを確認しました。

GUIのクリック操作・GUIのJUnitランナーは未検証です。画面なしの専用起動に伴い、Workbench未作成のm2e UI側とp2/JustJ側のログが出ています。これらはプロジェクトのエラーマーカーと分けて記録しています。詳細は[Pleiades結果](../../output/verification/projects/pleiades2025.json)と[実行方法・制約](../../output/verification/projects/pleiades-notes.md)を参照してください。

## 演習開始用の扱い

演習のTODOは保持しています。例えば本文第4章の開始用Validation画面は、formのth:objectを入れる課題が未実装なので、解く前には500になります。未実装のURLや空の一覧も、初期課題として期待値を分けて確認しました。これらを完成サンプルと同じ機能まで実装したという意味の合格ではありません。完成動作はanswer側で検証しています。

## 再実行

リポジトリのルートで、教材用MySQLを起動したうえで実行します。通常のDBポートは3306です。別ポートの検証にはDatabasePort/mysql-portを指定します。

```powershell
$env:JAVA_HOME = 'C:/pleiades/2025-12/java/21'
.\tools\projects\verify.ps1 -JavaHome $env:JAVA_HOME

python tools/projects/smoke_spring.py --java-home "$env:JAVA_HOME" --output output/verification/projects/spring-http.json
python tools/projects/smoke_enshu.py --java-home "$env:JAVA_HOME" --output output/verification/projects/enshu-http.json
```

HTTPランナーはPython標準ライブラリとmysqlクライアントを使います。アプリのJARを事前にビルドしてください。UUIDで識別したテスト用レコードだけを操作し、起動したJavaは終了時に停止します。使用中のHTTPポートでは要求を送る前に停止します。既定の開始ポートは本文18100、演習18200です。

検証スクリプトはWindows PowerShell 5.1でのJava 21判定も確認しました。DBのセットアップはprojects/database/setup.cmdを使い、管理者パスワードをプロンプトで入力します。

## 根拠資料

- [Spring Boot 4.0.2リリース](https://spring.io/blog/2026/01/22/spring-boot-4-0-2-available-now/)
- [4.0.2依存管理POM](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)
- [公式移行ガイド](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Pleiades 2025公式配布](https://willbrains.jp/pleiades_distros2025.html)
