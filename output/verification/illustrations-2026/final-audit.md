# 小型挿絵追加後の最終独立監査

判定：合格。問題0件。

新規9図＋縮小1図を確認。元373頁、既存2879ID＋追加18ID＝2897ID、空白17頁。

全431物理頁の元頁所属・header・章→合冊本文、URI89件を確認。

既存Markdown本文/コード/表/Span/図行/順序、baseline/layout38件、記録資材738件を比較。

| 図 | 元頁 | 章物理頁 | 合冊物理頁 | 幅×高さpt |
| --- | ---: | ---: | ---: | --- |
| illustration-2026-maven-libraries | 28 | 14 | 28 | 280.00×116.64 |
| illustration-2026-model-transfer | 58 | 33 | 63 | 280.00×116.64 |
| illustration-2026-repository-results | 90 | 36 | 106 | 280.00×116.64 |
| illustration-2026-session-separation | 142 | 13 | 170 | 280.00×117.17 |
| illustration-2026-validation-branch | 148 | 20 | 177 | 280.00×116.64 |
| illustration-2026-layout-reuse | 181 | 20 | 217 | 280.00×116.64 |
| illustration-2026-foreign-key-reference | 201 | 11 | 241 | 280.00×116.64 |
| illustration-2026-responsive-switch | 269 | 36 | 316 | 280.00×116.64 |
| illustration-2026-error-cause-chain | 291 | 3 | 343 | 280.00×117.11 |
| revision-di-remote | 80 | 23 | 93 | 260.00×133.12 |

全図とcaptionは同一物理頁。章→合冊の画像digestと画像矩形を照合。商標の記載は両冊2pで確認。

最終PDF：

- output/pdf/textbook/textbook/flow.pdf：`94251c704132f990984f8a1d1f2d99b94857ad8d0d34c259245365c93ef6c1b7`
- output/pdf/textbook/exercise/flow.pdf：`0c768357553f1d3c6c60d30a939d46a21a9a943a0a08eabfa38b9d3e5f48fb33`

比較範囲：

- 既存UI元画像の文字はSVG内の画像/図形であり、本文文字照合とは別。図版の意味内容をこの監査だけで保証しない。
- 章→合冊の本文はフッター領域を除いて順序を比較。目次頁では更新されるASCII数字を除く。
- URIはPDFの注釈の宛先・矩形・件数を比較。HTTPサーバーや外部URLへ接続しない。
- 固定頁の個別IDはnative/coverの頁所属で検査し、通常flowと区別する。
- 生成画像内のラベルや矢印の意味は別途目視する。本監査は画像SHA、実寸、本文保全、caption、章→合冊の同一画像を検査する。
