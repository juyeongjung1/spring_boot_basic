# 第3章のJava 21・Spring Boot 4.0.2対応

本文の既存ブロックIDと図版参照を保持し、更新版配布プロジェクトに合わせた箇所だけ改訂しました。

## 改訂箇所

- `migration-03-environment`: 実習環境と配布プロジェクトの対応を明記。
- `p071-b03`: 接続URLを実際に読める1行に修正し、propertiesとして表示。
- `p071-b11`: 設定反映と依存更新を分け、install必須という説明を修正。
- `p082-b06`: 参考JDBC例の通常文字列が実改行で切れる構文を修正。
- `p113-b04`: ModelMapperをJava 21対応の3.2.6へ更新。
- `p113-b05`: 管理対象外のライブラリとJava 21対応版を明記。
- `p113-b07`: 配布実装に合わせローカルでModelMapperを生成し、MVC引数との混同を解消。
- `p113-b08`: ModelMapperの生成とフォーム引数の違いを説明。
- 追加ID: `migration-03-environment`, `migration-03-jpa-dependencies`, `migration-03-jpa-pom`, `migration-03-url-line`

## 確認方針

Markdown全14章の解析、既存ID・図版参照・扉の保持、変更した依存XMLの構文は確認済みです。比較用Servlet例もJDK 21とTomcat 11の実際のAPIでコンパイルできました。Entity・Repository・Validation・Thymeleafの互換なコードと、演習の未実装部分は保持しています。実アプリのJava 21によるビルド・MySQL接続・画面動作は、配布プロジェクトの移行検証結果と合わせて確認します。

## 一次資料

- [Spring Boot 4.0移行ガイド](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Spring Boot 4.0.2の管理依存](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)
- [ModelMapper変更履歴（3.2.0でJDK 21対応）](https://raw.githubusercontent.com/modelmapper/modelmapper/master/CHANGES.md)
