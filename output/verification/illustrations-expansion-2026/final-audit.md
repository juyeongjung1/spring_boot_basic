# イラスト24点追加後の最終独立監査

判定：合格。問題0件。

Git f16135f3cebb2e2f9ab481e9cfead35b05bd52d4の2897 IDへ、図24・caption24だけを追加し、現在2945 ID。原本373頁、空白17頁、合冊446頁を確認。

新規24図と既存10図の全34図、原図資材739点、baseline/layout38件を検査。コード・表・Span・元図の行・元頁内の順序は保持。

全ヘッダー446頁、URI89件、元頁境界、章→合冊全文、原PPT65点の原位置、固定【】24組を照合。

組版変更はapproved-render-change.jsonのbuild.pyのSHA完全一致だけを許容。他の組版入力はf16135fと不変。元22頁末尾のboot-managed-versionsのみ、図/captionの所属22を保ち、beforeが元23頁先頭となる4連続順序を明示許容。

code_explanations.jsonはGit blobのLFとWindows作業ファイルのCRLFを区別し、改行正規化後の全文・JSON値の完全一致・Git diff差分0をすべて確認。本文・構文解説の変更はない。

入力時刻の限定互換の適用は0章。以前の承認PDF/checks・今回対象外・同じMD/設定/組版コード・他入力時刻の全条件でのみ継承。catalogは組版入力へ追加しない。

| 図 | 元頁 | 章物理頁 | 合冊物理頁 | 幅×高さpt |
| --- | ---: | ---: | ---: | --- |
| illustration-2026-maven-libraries | 28 | 16 | 30 | 280.00×116.64 |
| illustration-2026-model-transfer | 58 | 35 | 67 | 280.00×116.64 |
| illustration-2026-repository-results | 90 | 37 | 111 | 280.00×116.64 |
| illustration-2026-session-separation | 142 | 13 | 177 | 280.00×117.17 |
| illustration-2026-validation-branch | 148 | 21 | 185 | 280.00×116.64 |
| illustration-2026-layout-reuse | 181 | 22 | 227 | 280.00×116.64 |
| illustration-2026-foreign-key-reference | 201 | 11 | 251 | 280.00×116.64 |
| illustration-2026-responsive-switch | 269 | 38 | 331 | 280.00×116.64 |
| illustration-2026-error-cause-chain | 291 | 3 | 358 | 280.00×117.11 |
| illustration-expansion-2026-framework-foundation | 18 | 4 | 18 | 280.00×116.64 |
| illustration-expansion-2026-boot-managed-versions | 22 | 10 | 24 | 280.00×116.64 |
| illustration-expansion-2026-bean-auto-configuration | 23 | 11 | 25 | 280.00×116.64 |
| illustration-expansion-2026-request-response-search | 35 | 5 | 37 | 280.00×116.64 |
| illustration-expansion-2026-get-post-routing | 52 | 27 | 59 | 280.00×116.64 |
| illustration-expansion-2026-form-name-binding | 54 | 29 | 61 | 280.00×116.52 |
| illustration-expansion-2026-model-key-property | 60 | 39 | 71 | 280.00×119.38 |
| illustration-expansion-2026-repository-implementation | 78 | 20 | 94 | 280.00×116.52 |
| illustration-expansion-2026-query-method-name | 97 | 46 | 120 | 280.00×116.52 |
| illustration-expansion-2026-redirect-new-request | 124 | 80 | 154 | 280.00×116.52 |
| illustration-expansion-2026-model-session-lifetime | 143 | 15 | 179 | 280.00×116.64 |
| illustration-expansion-2026-form-error-roundtrip | 153 | 29 | 193 | 280.00×116.64 |
| illustration-expansion-2026-null-blank-constraints | 157 | 34 | 198 | 280.00×116.64 |
| illustration-expansion-2026-text-escape | 169 | 7 | 212 | 280.00×116.64 |
| illustration-expansion-2026-dynamic-url-id | 174 | 12 | 217 | 280.00×116.52 |
| illustration-expansion-2026-static-public-path | 179 | 19 | 224 | 280.00×116.64 |
| illustration-expansion-2026-relationship-field-column | 201 | 11 | 251 | 280.00×116.64 |
| illustration-expansion-2026-null-reference-guard | 206 | 17 | 257 | 280.00×116.64 |
| illustration-expansion-2026-select-label-value | 218 | 30 | 270 | 280.00×116.64 |
| illustration-expansion-2026-jpql-entity-names | 225 | 37 | 277 | 280.00×116.64 |
| illustration-expansion-2026-groupby-aggregate-dto | 233 | 47 | 287 | 280.00×116.64 |
| illustration-expansion-2026-cdn-local-delivery | 245 | 8 | 301 | 280.00×116.64 |
| illustration-expansion-2026-spacing-box-model | 259 | 25 | 318 | 280.00×116.64 |
| illustration-expansion-2026-grid-containment | 265 | 33 | 326 | 280.00×116.64 |
| revision-di-remote | 80 | 24 | 98 | 260.00×133.12 |

最終PDF：

- output/pdf/textbook/textbook/flow.pdf：`a3cfbd131dd2ada326f82c6b8778ef901f7c06d965d78f279d99e61a37c5e20b`
- output/pdf/textbook/exercise/flow.pdf：`e36296d10fc7135b308decafd10790e5e4719de75455dd019ded3c03331a3e47`

比較範囲：

- 既存UI元画像の文字はSVG内の画像/図形であり、本文文字照合とは別。図版の意味内容をこの監査だけで保証しない。
- 章→合冊の本文はフッター領域を除いて順序を比較。目次頁では更新されるASCII数字を除く。
- URIはPDFの注釈の宛先・矩形・件数を比較。HTTPサーバーや外部URLへ接続しない。
- 固定頁の個別IDはnative/coverの頁所属で検査し、通常flowと区別する。
- 生成図内の文字・矢印の意味は別途目視。本監査は全34図の実寸、同頁caption、画像digest、所属元頁と原文保全を確認する。
