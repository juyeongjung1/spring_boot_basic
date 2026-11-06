# 図番号・コード配色・構文解説の改訂

2026年11月6日。本文377ページ、演習84ページ。指定された図の変更と全体の表示修正を反映しました。

- [本文PDF](../../output/pdf/textbook/textbook/flow.pdf)
- [演習PDF](../../output/pdf/textbook/exercise/flow.pdf)
- [最終独立監査](../../output/verification/figure-cards-2026/final-audit.md)
- [生成プロンプト・保存先・配置カタログ](illustrations.json)

## 指定箇所の図

21pのDIの説明直後に、倉庫からAクラスへリモコンを渡し、メソッドのスイッチでBクラスの機能を使う図を追加しました。25pのBean図は、DIコンテナ内に準備されたリモコン本体を示す図へ差し替えました。旧24pの管理対象ライブラリ図とそのキャプションは削除しました。小型図は計34点を維持し、画像本体は幅300pt・高さ140pt以内です。

新しい2図は組み込みimage_genで生成し、章1のassetsへ保存しています。[今回の生成記録](../../output/verification/figure-cards-2026/generation-manifest.json)に初回・修正プロンプトと生成元パスを記録しました。

## 全体の表示

- スライド以外の独立図229点に図番号と枠を付けました。章・節・連番で採番し、図の説明文も同じ枠内に収めます。元画像の左端・幅を維持し、固定ページの番号は空き位置のタブに置きます。
- Javaのアノテーションを赤、HTMLの要素名を青、`th:`属性を紫にしました。緑のコメント、白テーマ、表の配色、右上の太字・下線付きファイル名を保持しています。
- 「コードの読み方」46箇所・84項目は3列表を廃止しました。行番号とコードを全幅の枠へ置き、下に元の説明文を通常の段落として表示します。原文の部分強調・書体・色を復元し、先頭文への自動強調と人工的な段落分割を撤回しました。
- 元Wordで一意に対応する82項目から段落境界20件・明示改行22件を復元しました。説明の意味や語句は全84項目で維持しています。

## 検証

回帰テスト74件が合格しました。全19章の文字照合、はみ出し、見出しの孤立、図・短いコード・表・手順の分断検査も合格しています。全229図を実PDFから切り出し、36枚の一覧で目視確認しました。コード解説も完成版PDFと部品PDFの本文・書式・配色を比較しています。

図番号の左端調整後に全19章を再生成済みです。その調整が適用されない12章は、合冊の対応115頁と描画を比較し、目次更新6頁を除く109頁の全画素一致を確認して合冊を保持しました。

原文IDは2945件を維持しました。DI図/captionの2件追加、不要図/captionの2件削除、Bean図/captionの差し替え・移動以外は、元の本文・コード・表・書式Span・ページ所属と順序を保っています。原本入力4件、baseline/layout38件、今回の明示指定以外の既存資材を保全しました。既存スライド65点は原位置と描画を保持しています。表示URLへのリンクは論理78箇所すべてを保持し、URI注釈82件の宛先・座標を章から合冊まで照合しました。全幅化でURLの折り返しが減ったため、5箇所で同じURLを覆う矩形数がまとまり、前版89件から82件へ減っています。全URLの文字がクリック領域に収まることも確認済みです。

- [図229点の実PDF確認](../../output/verification/figure-cards-2026/figure-frames/final-figure-review.json)
- [コード・構文解説の確認資料](../../output/verification/figure-cards-2026/code-layout/確認内容.md)
- [全テスト結果](../../output/verification/figure-cards-2026/regressions.json)
- [リンク監査](../../output/verification/figure-cards-2026/final-links.md)
- [元のURL78箇所の保持検査](../../output/verification/figure-cards-2026/logical-link-preservation.md)
- [最終PDFのSHA256と概要](../../output/verification/figure-cards-2026/summary.json)

以前の改訂の検証は[イラスト追加時](../../output/verification/illustrations-expansion-2026/final-audit.md)・[括弧などの修正時](../../output/verification/brackets-2026/final-audit.md)の記録に保持しています。
