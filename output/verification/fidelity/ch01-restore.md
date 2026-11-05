# 第1章の原文復元と最小差分の監査

結果：合格。第1章をbaselineの原文へ戻し、必要なFramework版名と句点1か所だけを本文の差分として残した。外部プロジェクト・元SVG・baseline・source-layoutは変更していない。

## 撤回・復元した内容

- `p025-b06`：原文の「導入したいバージョン名をクリック」「Usagesが一番多い方を選ぶ」を復元。
- `p026-b01`：ビルドツールのタブを切り替え、表示されたテキストをコピーする原文へ復元。
- `p026-b02`：Maven導入例を原文の`version=8.3.0`・`scope=compile`へ復元。
- `migration-01-pom-parent`・`migration-01-pom-java21`：原文にない追加説明とコードを削除。
- `p027-b01`・`p027-b02`：GUIでの`Maven install`と、コンソールにダウンロード/インストールのログが流れる原文へ復元。
- `p028-b04`：`maven install`を実行する原文へ復元。`mvnw verify`のCLI説明は削除。

教材中の導入例を戻したもので、Java21・Spring Boot4.0.2へ更新した配布アプリの実POMは巻き戻していない。

## baselineから残る差分の全件

| 箇所 | baseline | 最終原稿 | 理由 |
| --- | --- | --- | --- |
| 冒頭の非表示HTMLコメント | 本文の改訂はまだ行っていません。 | Java 21・Spring Boot 4.0.2対応版。 | 本文に出ない管理情報。 |
| `p020-b10` | 本書では、Spring Framework 6.0(2022 年11 月リリース)を利用します。 | 本書では、Spring Framework 7.0.3を利用します。 | 必要な版名の訂正。旧6.0に対応する2022年11月の注記を除去し、主文は保持。 |
| `p022-b08` | …スムーズに開発を始めることができます | …スムーズに開発を始めることができます。 | 明らかな文末句点の欠落1か所を補完。 |

監査時点で図版参照15点はbaselineと一致し、`p018-f02`を含む既存active参照行は変更していない。別担当がこの図の改訂参照へ切り替える場合も、本文の復元とは分けて扱う。

## Spring Framework 6.0についての回答根拠

本教材のSpring Boot **4.0.2**を前提とすると、Framework **6.0**という記述は旧版の記述であり、正しくは**7.0.3**。

公式Maven Centralの[Spring Boot 4.0.2実BOM](https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.2/spring-boot-dependencies-4.0.2.pom)をHTTP200で再取得し、`spring-framework.version=7.0.3`を確認した。取得内容のSHA256は`b4904891e811431820f16b378776f935fb7bff8129e26e8dc72936b6283af8da`。

公式リポジトリの[v4.0.2 gradle.properties](https://raw.githubusercontent.com/spring-projects/spring-boot/v4.0.2/gradle.properties)も`springFrameworkVersion=7.0.3`。さらに[Spring Framework 7.0.3公式リリース記事](https://spring.io/blog/2026/01/15/spring-framework-7-0-3-available-now/)に、同版がSpring Boot4.0.2へ同梱される旨がある。日付の説明を教材へ新たに書き足さず、旧リリース日の注記だけを除去した。

## 機械検査

- 84本文ブロックのID集合・16元ページの順序・15図版のIDを保持。
- 原文にない新規IDは0、追加説明段落は0。
- 本文差分は`p020-b10`と`p022-b08`だけ。その他の本文・コード・書式はbaselineと一致。
- GUI手順とMySQLの原導入例がbaselineに完全一致。
- 第1章内に`verify`・`mvnw`の追記は残っていない。
- Markdownの全文を、上記3差分だけbaselineへ適用した期待値と比較して完全一致。

全diffと検査条件・結果は`ch01-restore.json`に保存。PDF再生成・最終表示確認・コミットは親担当の作業として、この監査では実行していない。
