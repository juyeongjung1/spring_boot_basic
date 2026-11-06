# コード右上ファイル名の最終監査

判定：合格。全19章の最終章PDFを対象に、HTMLプレビューの期待文字列とcode cardの全partを照合し、ラベル116件を10枚のコンタクトシートで全件目視した。本文・CSS・PDFは変更していない。

## 対象と結果

| 項目 | 件数／結果 |
| --- | --- |
| 対象章 | 19 |
| コードカード | 186 |
| PDFのコードpart（続き含む） | 190 |
| 右上ラベルのあるpart | 116（続き2、コンソール表示例1を含む） |
| 空ラベルのpart | 74、余計な名前を追加せず保持 |
| 実太字・文字色・下線・位置・文字照合の不合格 | 0 |
| 元画像から文字化したファイル名 | 5/5合格 |
| Markdown filename属性の指定 | 5/5合格 |

全116件が実PDFのMeiryo-Bold／font flags16／濃青#123d68で表示され、下線が塗り矩形として残る。文字列はHTMLのfile-itemと空白を除き全文一致した。右上のヘッダー領域内に収まり、下線の欠け、文字切れ、続き表示との重なりは見当たらない。

元画像由来の5指定と、新しい参考欄のfilename属性も同じ規則で検査した。空のラベルへ推測したファイル名を追加していない。

## 元画像から文字化した5件

| 章 | コードID | 元図版ID | 表示文字 | 結果 |
| --- | --- | --- | --- | --- |
| 03 | p071-b03 | p071-f07 | application.properties | 合格 |
| 03 | p113-b04 | p113-f49 | pom.xml | 合格 |
| 04 | p149-b05 | p149-f13 | pom.xml | 合格 |
| 04 | p161-b02 | p161-f24 | /resources/messages.properties | 合格 |
| 05 | p182-b04 | p182-f15 | pom.xml | 合格 |

## 新しいfilename属性の指定

| 章 | コードID | 表示文字 | 結果 |
| --- | --- | --- | --- |
| 04 | revision-messages-bundles | messages.properties | 合格 |
| 04 | revision-messages-ja | messages_ja.properties | 合格 |
| 04 | revision-messages-en | messages_en.properties | 合格 |
| 04 | revision-messages-html | message.html | 合格 |
| appendix-b | revision-errors-trace | コンソールの表示例 | 合格 |

## 小型fixtureと回帰検査

実稿の監査に加え、先行fixtureで極長日本語pathの2/3行折返し、続きカード、モノクロ表示を確認した。変更前の実PDFはMS-PGothic(flags0)、変更後はMeiryo-Bold(flags16)。短名と普通path/続きのヘッダー高35.52pt、本文コード幅は維持し、極長pathだけヘッダー高が約3.49pt増加した。太字と下線はモノクロでも明瞭。

8fixture／10PDF partの試作、およびtest_html_components.pyの10回帰テストが成功。元原文46解説と元5filename図版ID、コメント緑、表配色の保持検査も成功した。

- [before→after比較](filename-audit/fixture-comparison-1.png)
- [設定ファイルの比較](filename-audit/fixture-comparison-2.png)
- [モノクロ表示](filename-audit/fixture-header-short-monochrome.png)
- [極長pathのモノクロ表示](filename-audit/fixture-header-narrow-long-monochrome.png)
- [続きカード](filename-audit/fixture-header-continued.png)

## 章別件数

| 章 | カード | part | ラベルpart | 続きのラベルpart |
| --- | --- | --- | --- | --- |
| 01 | 2 | 2 | 0 | 0 |
| 02 | 14 | 14 | 9 | 0 |
| 03 | 49 | 49 | 36 | 0 |
| 04 | 27 | 27 | 25 | 0 |
| 05 | 22 | 23 | 12 | 0 |
| 06 | 33 | 33 | 19 | 0 |
| 07 | 33 | 36 | 14 | 2 |
| appendix-a | 0 | 0 | 0 | 0 |
| appendix-b | 1 | 1 | 1 | 0 |
| ex-back | 0 | 0 | 0 | 0 |
| ex-front | 0 | 0 | 0 | 0 |
| ex01 | 0 | 0 | 0 | 0 |
| ex02 | 0 | 0 | 0 | 0 |
| ex03 | 0 | 0 | 0 | 0 |
| ex04 | 0 | 0 | 0 | 0 |
| ex05 | 0 | 0 | 0 | 0 |
| ex06 | 0 | 0 | 0 | 0 |
| ex07 | 5 | 5 | 0 | 0 |
| front | 0 | 0 | 0 | 0 |

## 証跡と検査範囲

`filename-audit.json`には全190partのspec ID／part token／章内頁／HTML期待名／実PDF font・flags・色・bbox／下線座標／各章PDF・checks・HTMLのSHA256を保存した。全116ヘッダーのPNGと10コンタクトシートは同名フォルダーへ保存した。

全件監査は最終章PDFを対象とし、最終合冊では代表3実ページを追加検査した。CSSや原稿への追加修正は不要。

CSS SHA256：`59dc523340ea1d281741d4dcce547b6e3f0a658499354db14c875d891a86b299`。

## 最終合冊の確認

最終合冊の物理41頁・82頁・136頁を全ページPNGで再目視し、右上ラベルが明瞭で、前後の本文/コードから分離していることを確認した。各ヘッダーを最終章PDFと144dpiで比較し、3/3が全画素一致（平均RGB差0）。合冊内の実文字もMeiryo-Bold／flags16／#123d68と全文一致を確認した。

| 実物理頁 | 表示文字 | 証跡 |
| --- | --- | --- |
| 41 | …/controller/IndexController.java | [実ページPNG](filename-audit/merged-p041.png) |
| 82 | application.properties | [実ページPNG](filename-audit/merged-p082.png) |
| 136 | pom.xml | [実ページPNG](filename-audit/merged-p136.png) |

| 最終PDF | 頁数 | SHA256 |
| --- | --- | --- |
| textbook | 349 | `e59623eefe51d8785aa573261a6ea9d3db3ca4aac2f0ae34160175385c0dacf2` |
| exercise | 82 | `ee833a175c2c711bba65823b1caa07a38c4de0c52a69731abe5f624487c0abb7` |

全件監査・全116ヘッダー目視・合冊代表3頁の確認を完了し、残件なし。

## 【の固定描画修正後の再検証

見出しの【を最小修正して再生成した6章（02・03・04・06・front・ex-front）を含め、全19章190partの文字・実太字・色・下線・右上配置を再照合し、不合格0を確認した。

- 6章のラベル付きヘッダー89画像は、修正直前に保存した画像と89/89全画素一致。平均RGB差0、カード位置も不変。
- 残る13章のPDFは13/13 SHA256不変。
- 期待するファイル名は全190partで不変、CSS SHAも不変。この結果により前回の全116件目視結果を継続適用し、全件の再目視は省略した。
- 新しい最終合冊の物理41・82・136頁は再び全ページPNGを目視し、ヘッダーが最終章PDFと3/3全画素一致すること、実Meiryo-Bold／flags16／#123d68が保たれることを確認した。

`filename-bracket-revalidation.json`に89画像と他13章の全比較結果を保存した。上記の最終PDF SHA256表はこの再合冊後の値へ更新済み。確認終了、残件なし。
