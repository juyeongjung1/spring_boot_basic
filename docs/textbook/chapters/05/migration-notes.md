# 第5章のJava 21・Spring Boot 4.0.2対応

本文の既存ブロックIDと図版参照を保持し、更新版配布プロジェクトに合わせた箇所だけ改訂しました。

## 改訂箇所

- `migration-05-environment`: 実習環境と配布プロジェクトの対応を明記。
- `p182-b05`: Layout Dialectの管理版利用とMaven更新手順を明記。
- `p184-b10`: HTML属性のスマート引用符と壊れたコメント開始記号を通常の構文へ修正。
- 追加ID: `migration-05-environment`

## 確認方針

Markdown全14章の解析、既存ID・図版参照・扉の保持、変更した依存XMLの構文は確認済みです。比較用Servlet例もJDK 21とTomcat 11の実際のAPIでコンパイルできました。Entity・Repository・Validation・Thymeleafの互換なコードと、演習の未実装部分は保持しています。実アプリのJava 21によるビルド・MySQL接続・画面動作は、配布プロジェクトの移行検証結果と合わせて確認します。

## 一次資料

- [Spring Boot 4.0移行ガイド](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
- [Spring Boot 4.0.2の管理依存](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)
