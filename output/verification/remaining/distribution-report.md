# 配布ZIP再生成・検証報告

実施日時(UTC): 2026-11-05T04:11:17.734358+00:00

従来と同じprojects/配下の構造と852ファイルを維持して、最新のソースから配布ZIPを再生成しました。READMEは既存の前提一覧へBootstrap 5.3.8を1行だけ追記しました。

- 配布物: `output/projects/SpringBootBasic_Java21_Boot4.0.2.zip`
- SHA-256: `8dff9ef63b0dc5f24a147e9a19e6624045bcde3b1ff86428c9010a23432c1202`
- サイズ: 6,161,415 bytes
- 32 POM（集約5＋アプリ27）。全アプリのJava 21・Boot親4.0.2・Eclipseコンパイラー21を実内容で確認。
- ZIP全852エントリのbytesが現在のprojectsファイルと一致。CRCエラー0。
- サンプルHTML 253件に旧Bootstrap 5.3.0・年2023/2024なし。Bootstrap資材88件のヘッダーは全て5.3.8。
- 収録パスの追加/削除0。内容を更新したエントリは1件。
- target等の除外ファイルは904件。実フォルダーの削除は行っていません。

package-checks.jsonの配布SHA・件数・検証結果を更新し、output/verification/projects/summary.jsonはdistribution項目だけを更新しました。
以前のJUnit・HTTP・Pleiades・PDF等の検証結果はd3933b4時点の履歴として、そのまま保持しています。

projects/.gitattributesのCSS/JS用text eol=lf設定2行も収録し、checkout時の改行変換による公式Bootstrap資材のbytes変化を防ぐ設定を確認しました。今回の最終再生成では資材内容やJARを変更していません。

全エントリのパス・bytes・CRC・SHA、および除外ファイル一覧はdistribution-report.jsonに収録しています。

最終再生成で前回ZIPから変わった内容は `projects/.gitattributes` のみです。Bootstrap 88資材のSHAが公式配布物と同じ値を維持することも再確認し、versions-reportにも同じ最終配布SHAを記録しました。
