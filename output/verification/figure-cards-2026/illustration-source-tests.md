# 図改訂の原文回帰テスト

判定：合格。IllustrationSourceTestsの6件が成功（157.562秒）。

実行：`python -m unittest test_illustrations.IllustrationSourceTests -v`

確認範囲：

- 合計33新図＋既存DI図1、既存9図の記録・画像比率・寸法を保全。
- 元の全19章の本文・コード・表・Span・元ID順序を保全。
- Git 96a99882326d65ec048100b2f20fa0ed4aaa72d2から、導入DI図/caption追加、managed図/caption削除、Bean図/captionの差替えと指定位置移動だけを許可。
- 旧32図record・共通source設定・総2945 IDを保持。
- 元baseline/source-layoutと原図資材を保持し、旧managed PNGの削除・新DI PNGの追加・Bean同名PNGの差替えを許可。

PDF側の2件は全章・合冊の完成後に実行する。
