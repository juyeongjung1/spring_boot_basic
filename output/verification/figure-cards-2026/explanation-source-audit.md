# コードの読み方：原文と表示加工の独立調査

結果：意味本文の字句の新規改稿は検出されず、原文の84行と完全一致。問題は列幅と表示側の強調・改行処理にある。

| 項目 | 件数 |
| --- | ---: |
| passed | True |
| cards | 46 |
| rows | 84 |
| source_ids | 163 |
| meaning_rows_exact_from_current_fragments | 84 |
| baseline_contains_all_meaning_fragments | 81 |
| sources_current_equals_baseline | 155 |
| sources_baseline_equals_layout | 163 |
| rows_with_auto_first_sentence_emphasis | 83 |
| rows_with_added_emphasis_on_original_regular_text | 81 |
| problems | 0 |

## 表示側で行っていた変更

- 意味・補足の字句はsource_fragmentsの原文断片から作られ、84行すべてで完全一致する。
- 変更は表示側。explanation_htmlはWordの1行改行を除去し、第n引数の前へ空段落を作り、最初の句点までを新規strongへ包んでいる。
- 元のSpan書式は意味セルでは使われず、原文にあった局所の強調もHTMLへ継承されていない。
- 今回の復旧対象は、意味本文の改稿ではなく、狭い3列・先頭文の自動強調・元の強調の欠落。原文と元Spanを通常幅へ戻すのが適切。

## 原文との差

- 03/p129-b08：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 04/p137-b04：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 04/p140-b04：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 04/p140-b05：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 04/p140-b06：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 04/p150-b06：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 07/p266-b11：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。
- 07/p267-b01：baselineと現在本文に差がある。今回作業以前の修正と区別し、JSONに全文を記録。

## 代表例

- 02/p060-b04 2 行目：元の意味本文と書式SpanをJSONへ記録。
- 02/p060-b04 10 行目：元の意味本文と書式SpanをJSONへ記録。
