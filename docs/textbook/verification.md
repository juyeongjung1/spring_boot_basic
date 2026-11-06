# 書体と継続箇所の改ページ改善

2026年11月6日。本文377→343ページ、演習ガイド84→81ページ、合計37ページ減です。本文の字号や段落余白は縮めず、指定されたパターンだけを調整しました。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [最終独立監査](../../output/verification/compact-pages-2026/final-audit.md)

## ① 本文と強調の書体

コードの読み方46箇所・84項目の本文をP明朝、元からの強調部分をPゴシックの太字に統一しました。45pの強調が細い原因は、EdgeがPゴシックの擬似太字を印刷PDFへ反映していないことでした。文字を1回だけ埋め込むPDFの文字描画で太さを補い、通常の本文と同じ字号/35ptの輪郭にそろえました。原文・強調箇所・字号・色・位置・リンクを保持しています。

明朝のまま太字になっていた57文字とTimes系25文字も共通の書体へ統一しました。全46箇所を完成PDFで目視し、文字の重複・通常本文への太字漏れがないことを確認しています。

[書体・太字の比較画像と検査案内](../../output/verification/compact-pages-2026/prose-fonts/確認内容.md)

## ②～④ 続き本文・画像・小小見出し

元頁境界をすべて強制改ページにしていたため、文の途中や小小見出しでも空きが残っていました。調査した箇所のうち、続き本文と小小見出しの56境界だけを明示登録しました。小小見出しは、再組版後も直前頁の本文が半頁以下のときだけ同頁へ続けます。節・項、章扉、スライド、固定頁、空白頁と、その他の元頁境界は保っています。

旧47pのreturnの補足を直前の説明へ続け、旧55～56pの「構造を整／理しやすく」の文は表示時に1段落へ戻しました。旧53～54pの短い説明と【作業手順】も同頁へ続きます。

| 指摘箇所（前版） | 最終版 | 確認する内容 |
| --- | --- | --- |
| 45p | [45pの画像](../../output/verification/compact-pages-2026/requested-pages/after-45.png) | public/String/indexの説明とPゴシック太字 |
| 46～47pのreturn補足 | [46pの画像](../../output/verification/compact-pages-2026/requested-pages/after-46.png) | 前の説明と同頁へ継続 |
| 49～50p | [48pの画像](../../output/verification/compact-pages-2026/requested-pages/after-48.png) | 操作手順1～6を1頁へ |
| 53～54pの作業手順① | [51pの画像](../../output/verification/compact-pages-2026/requested-pages/after-51.png) | 短い説明の後に見出しを継続 |
| 55～56pの本文と作業手順② | [52pの画像](../../output/verification/compact-pages-2026/requested-pages/after-52.png) | 文途中の分断をなくし、HTMLコードと同頁へ |

旧49～50pは操作画面1点を96%へ縮め、手順1～6を1頁へ収めました。他の採用は第3章の元94pの2図を96%、元120pの3図を97%です。縮小は計6点、3～4%だけで、元画像・左端・縦横比を保持しています。続きの配置だけで孤立頁がなくなる図と、縮小しても頁数が減らない図は原寸のままです。第1章の元22pは次頁が半頁近くあり、少量の続きという条件に合わないため縮小していません。

元274pは、同頁化すると継続用の「10行目」枠が直前と重複するため従来の区切りを保持しました。この除外による増頁はありません。コードや説明文の改稿はしていません。

- [確定した境界・倍率の一覧](../../output/verification/compact-pages-2026/approved-pagination.json)
- [候補調査と各箇所の根拠](../../output/verification/compact-pages-2026/curated-selection.json)
- [画像縮小の採否と比較](../../output/verification/compact-pages-2026/image-trial-review.json)

## 検証

回帰テスト78件が合格しました。全19章の原稿・コード・表・書式Span・2945 IDは変更せず、画像資材763点、baseline/layout38件、原本4件も保全しています。図番号229点、PPT65点の位置と画素、ファイル名、元頁373件、空白17頁、全424頁のヘッダーとページ番号を検査しました。論理リンク78箇所・URI注釈82矩形も、宛先とクリック領域を保持しています。

- [全テスト結果](../../output/verification/compact-pages-2026/regressions.json)
- [リンク監査](../../output/verification/compact-pages-2026/final-links.md)
- [最終PDFのSHA256・概要](../../output/verification/compact-pages-2026/summary.json)

前回の[図番号・枠・イラスト改訂](../../output/verification/figure-cards-2026/final-audit.md)と、[生成プロンプト・配置カタログ](illustrations.json)はそのまま保持しています。
