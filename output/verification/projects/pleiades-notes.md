# Pleiades 2025の実環境検証

公式Java Standard 2025-12（20260117）をMD5照合・正常展開した検証用コピーで実施しました。ユーザー既存のPleiadesやワークスペースは操作していません。

- Eclipse 4.38.0.v20251201-0920、m2e 2.7.600.20251121-1832、同梱Lombok 1.18.42。
- Java 21.0.13、Xmx512mのJVMを1本使用。終了後の残留Java/Eclipsecは0本。
- 最新projectsのコピーを新しいtmpワークスペースへm2eのimportProjects APIで取り込み。
- 集約5＋アプリ27の32POM／32プロジェクトを取り込み。
- JDT clean/full build後、全27アプリでsource・target・compliance＝21、JRE＝21を確認。
- 全27アプリの生成クラスはmajor65（Java 21）、メソッド引数名のメタデータ生成も有効。
- プロジェクトのエラーマーカーは全32件で0。原projectsは書き換えず、インポート先は全件tmpコピー内であることも確認。

## 確認範囲の制約

GUIメニューのクリック操作やGUIのJUnitランナーは実施していません。Eclipse本体のm2e/JDTを画面なしで呼び出した検証です。起動ログにはp2更新機能のjustjアーティファクト不足と、UI専用m2e.core.uiがWorkbenchなしで起動する際のエラーがあります。これらをプロジェクトのコンパイルエラーと混同せず、上記の実ビルド結果と分けて記録しています。回避のために配布ソースを変更する処置は行っていません。

詳細はpleiades2025-report.json、要約はpleiades2025-summary.json、起動ログはpleiades-headless.logです。再検証用の一時プログラムはide-probeにあります。
