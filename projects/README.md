# Java 21・Spring Boot 4.0.2版の配布プロジェクト

更新版はこの `projects` フォルダーです。同一内容が重複していた元配布物を整理し、27種類のアプリを1コピーずつ収録しました。元の `SpringBootBasicPlus_05` と `SpringBootBasicPlus_05+DB` は、取り込み元としてそのまま保存しています。

| グループ | 内容 | アプリ数 |
| --- | --- | ---: |
| spring_answer | 本文教材の完成サンプル | 7 |
| spring_exercise | 本文教材の穴埋め開始用 | 7 |
| enshu_answer | 演習ガイドの解答 | 7 |
| enshu_exercise | 演習ガイドの開始用（第2〜7章） | 6 |

演習開始用のTODOは保持しています。課題を解く前は、画面が空だったり、課題対象のURLが未実装だったりする箇所があります。完成動作は対応するanswer側と比較してください。

## 前提

- Pleiades 2025のJava版（Full Editionには開発用JDKが同梱）
- アプリのコンパイル・実行・Maven実行にJDK 21
- Spring Boot 4.0.2（各アプリの親POMで固定）
- MySQL 8.0、通常ポート3306
- Maven Wrapper、またはMaven 3.6.3以降

Boot管理の依存関係を使用します。4.0.2ではHibernate 7.2.1.Final、MySQL Connector/J 9.5.0、Lombok 1.18.42、Thymeleaf Layout Dialect 3.4.0です。Java 21対応のためModelMapperは3.2.6へ更新しています。Web MVCは `spring-boot-starter-webmvc`、MVCテストは対応する `spring-boot-starter-webmvc-test` です。

## Pleiades 2025へインポート

1. 新しい学習用ワークスペースを開きます。
2. [ウィンドウ]→[設定]→[Java]→[インストール済みのJRE]でJDK 21を選択します。Full Editionの例は `C:/pleiades/2025-12/java/21` です。
3. [Java]→[インストール済みのJRE]→[実行環境]でJavaSE-21を同じJDKに対応付けます。
4. [ファイル]→[インポート]→[Maven]→[既存Mavenプロジェクト]で、この `projects` フォルダーを選びます。
5. プロジェクトの読み込み後、[Maven]→[プロジェクトの更新]（Alt+F5）を実行します。
6. アプリのJavaコンパイラーが21であることと、Maven実行構成・Spring Boot実行構成のJREも21であることを確認します。

Eclipseを起動するJDKと、開発・実行するアプリのJDKは別の設定です。既存のJava 17がPATHに残る場合も、アプリはJava 21で実行してください。

番号のないプロジェクトは集約用です。各アプリは単独でビルド・実行できるため、事前の集約プロジェクトのMaven installは必須ではありません。

## データベース

`database/sample.sql` は本文用、`database/exercise.sql` は演習用です。元のSQLをUTF-8へ変換し、データの内容を保持しています。既存DBを削除する命令は含めていません。新しい教材DBを作成するためのスクリプトなので、同名DBが既に存在する環境では、そのDBを利用するか別の検証用インスタンスで実行してください。

`projects` フォルダーで、管理権限のあるMySQLユーザーから実行します。パスワードはMySQLクライアントのプロンプトで入力します。セットアップはSQLを標準入力のバッチとして実行し、既存DBの作成エラーで停止します。

```powershell
.\database\setup.cmd
# mysql.exeがPATHにない場合
.\database\setup.cmd "C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe"
```

| 教材 | DB | 接続ユーザー | 学習用パスワード |
| --- | --- | --- | --- |
| 本文 | spring_sample | spring_sample_user | trainocate |
| 演習 | spring_exercise | spring_exercise_user | password |

接続先は各アプリの `src/main/resources/application.properties` にあります。別ポートで確認するときは `SPRING_DATASOURCE_URL` を一時設定できます。今回の自動検証では、既存のMySQLサービスとは別のデータ領域・ポート13306を使用しました。

## 起動とビルド

例として、本文第2章の完成サンプルを起動します。

```powershell
$env:JAVA_HOME = 'C:/pleiades/2025-12/java/21'
$env:Path = "$env:JAVA_HOME/bin;$env:Path"
cd spring_answer/spring_answer_2
.\mvnw.cmd spring-boot:run
```

Pleiadesではメインクラスを右クリックし、[実行]→[Spring Bootアプリケーション]を選びます。コンソールにJava 21、Spring Boot 4.0.2と起動完了が出ることを確認します。

全アプリのJARを作成する場合は、`projects` フォルダーで次を実行します。DBを使うテストは、各グループの学習DBを起動してから実行してください。

```powershell
.\mvnw.cmd -DskipTests package
.\mvnw.cmd -f spring_answer/pom.xml test
.\mvnw.cmd -f spring_exercise/pom.xml test
.\mvnw.cmd -f enshu_answer/pom.xml test
.\mvnw.cmd -f enshu_exercise/pom.xml test
```

検証用の `target` は配布・Git登録に含めません。Mavenで必要なときに生成します。

## 固定版の新規作成

Spring Initializrのバージョン一覧は時期によって変わります。4.0.2を選択できない場合は、`spring_exercise/spring_exercise_1_3` を複製してプロジェクト名・パッケージを調整する方法で、教材と同じ依存関係を再現できます。生成した別版を利用する場合も、親POMのバージョンを4.0.2、java.versionを21、Webをwebmvcへ揃えてからMaven更新してください。

## 根拠資料

- [Spring Boot 4.0.2リリース](https://spring.io/blog/2026/01/22/spring-boot-4-0-2-available-now/)
- [4.0.2の依存管理POM](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)
- [Spring Boot 4移行ガイド](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Pleiades 2025公式配布・JDK設定](https://willbrains.jp/pleiades_distros2025.html)
