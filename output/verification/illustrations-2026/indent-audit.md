# 全章の字下げ実測監査

結果：pass

自動組版paragraphの全先頭（内部Word段落も含む）と新図caption。固定原座標の商標/目次/付録GUI、見出し・リスト・HTML表/コードは区分して維持。

## 集計

- measured_paragraph_starts: 963
- normal_body: 873
- zero_indent_exceptions: 80
- illustration_captions: 10
- font_sizes: {11.04: 859, 12.0: 10, 14.04: 4}
- failures: 0
- unresolved: 0

全測定値はindent-audit.jsonへ保存。基準x=85.104pt、参考枠のみ8ptを加算。可視先頭文字のfont sizeを全角1文字分として比較し、許容差0.03ptで確認。

確定した3続き断片は同一の元Word段落として結合したため、段落先頭の集計は初回966から3減る。各境界markerは1回ずつ、同一カーソル座標であることを別に検査。MD・Typst・章PDF・共通エンジンの最新SHA256をJSONへ保存。

監査後の再ハッシュ照合：19章×MD/Typst/PDF＋共通2ファイル＝59件すべて一致。最大字下げ誤差は4e-06pt。

監査日時（UTC）：2026-11-06T01:05:43.792157+00:00。3断片の元Word証跡は同フォルダword-continuation-proof.jsonへ保存。
