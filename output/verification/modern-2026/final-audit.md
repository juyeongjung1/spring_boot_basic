# 最終教材の独立監査

判定：合格。問題0件。

原本373頁→430物理頁、元頁対応373件、空白17頁。

原本ID2853、基準230d71fの既存ID2854、許可追加25、現在ID2879。

構文解説46カード/84表示行のsource本文復元、全ID所属・改ページ・合冊本文・ヘッダー430頁・URI89件を確認。

localhost:8080/login3宛の実URI注釈は1件。

詳細な頁対応はfinal-audit.jsonとboundary-detail/source-page-boundary-audit.md、URI全件はfinal-links.json/mdを参照。

| 最終PDF | SHA-256 |
| --- | --- |
| output/pdf/textbook/textbook/flow.pdf | `d35ef77c96e228f9229ea8a2f23c5f9a58827e3f0cec2c9638be57a2e0250d79` |
| output/pdf/textbook/exercise/flow.pdf | `c46433c040fb5fbb24fc12184d0e8791768b125c10dd5998aa45da734a68a669` |

比較範囲：

- 既存UI元画像の文字はSVG内の画像/図形であり、本文文字照合とは別。図版の意味内容をこの監査だけで保証しない。
- 章→合冊の本文はフッター領域を除いて順序を比較。目次頁では更新されるASCII数字を除く。
- URIはPDFの注釈の宛先・矩形・件数を比較。HTTPサーバーや外部URLへ接続しない。
- 固定頁の個別IDはnative/coverの頁所属で検査し、通常flowと区別する。
