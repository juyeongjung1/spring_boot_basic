# 第1章のJava 21・Spring Boot 4.0.2対応

本文の既存ブロックIDと図版参照を保持し、更新版配布プロジェクトに合わせた箇所だけ改訂しました。

## 改訂箇所

- `migration-01-environment`: 実習環境と配布プロジェクトの対応を明記。
- `p025-b06`: 人気順で旧ドライバーを選ぶ手順を、Boot 4.0.2によるバージョン管理へ変更。
- `p026-b01`: 旧スクリーンショットと現行の依存定義を区別。
- `p026-b02`: Connector/Jの8.3.0固定を外し、配布POMと同じruntime依存へ変更。
- `p027-b01`: Pleiades 2025のMaven更新と検証ビルドを分けて説明。
- `p027-b02`: 配布Maven Wrapperによる確認方法を追加。
- `p028-b04`: Javaと親POMを含めた再現方法を明記。
- 追加ID: `migration-01-environment`, `migration-01-pom-parent`, `migration-01-pom-java21`

## 確認方針

Markdown全14章の解析、既存ID・図版参照・扉の保持、変更した依存XMLの構文は確認済みです。比較用Servlet例もJDK 21とTomcat 11の実際のAPIでコンパイルできました。Entity・Repository・Validation・Thymeleafの互換なコードと、演習の未実装部分は保持しています。実アプリのJava 21によるビルド・MySQL接続・画面動作は、配布プロジェクトの移行検証結果と合わせて確認します。

## 一次資料

- [Spring Boot 4.0移行ガイド](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Spring Boot 4.0.2の管理依存](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)
