# 括弧・小見出し・ファイル名修正後の独立監査

判定：合格。問題0件。

元373頁/空白17頁/既存2897IDを保持。全431物理頁のheader・章→合冊本文・URI89件を照合。

MDの【】215組を全nativeへ対応。native個別配置24組は各glyphをsource-layoutの明示x/yと照合。PPT65枚、挿絵10図の実寸/digest/caption同頁、filename114件の原文字を確認。

基準530b12756c6cb323beb964d557ff9f306dc75c3cに対しMD/source設定/baseline/layout/画像/catalog/解説JSON/filenameJSONの変更0。README.mdとverification.mdの公開報告更新だけを明示許容。

字体差の分類：

- 02/p051-b04：['MS-Gothic'] 12.00pt→['MS-Gothic'] 10.51pt、承認済みHTML化の字体/サイズ変更。
- 02/p056-b04：['MS-Gothic'] 12.00pt→['MS-Gothic'] 10.50pt、承認済みHTML化の字体/サイズ変更。
- 03/p129-b03：['MS-PMincho'] 11.04pt→['MS-PGothic'] 10.50pt、承認済みHTML化の字体/サイズ変更。
- 05/p184-b05：['MS-PMincho'] 11.04pt→['MS-PGothic'] 10.50pt、承認済みHTML化の字体/サイズ変更。
- 06/p232-b03：['MS-Gothic'] 12.00pt→['MS-Gothic'] 10.51pt、承認済みHTML化の字体/サイズ変更。
- 06/p232-b04：['MS-Gothic'] 12.00pt→['MS-Gothic'] 10.51pt、承認済みHTML化の字体/サイズ変更。

native修正の影響外13章は、時刻だけで再生成を要求しない限定互換検査を実施。現bookからnative【prefixとそのコメントのみを戻した全文が生成flow.typ内と完全一致、native【呼出し0、他入力が新しくないこと、章PDF/checks SHAがnative修正前と同じことを全条件で確認した。mtimeの書換えや他の入力の除外は行っていない。

図内の【】11組/10図は輪郭化されているため現fontを文字抽出できない。資材のGit一致とPPT配置を確認し、native字間検査とは区別する。ラスタ層もOCRによる字体断定をしていない。

最終PDF：

- output/pdf/textbook/textbook/flow.pdf：`e59623eefe51d8785aa573261a6ea9d3db3ca4aac2f0ae34160175385c0dacf2`
- output/pdf/textbook/exercise/flow.pdf：`ee833a175c2c711bba65823b1caa07a38c4de0c52a69731abe5f624487c0abb7`

全【】source ID/元頁/物理頁/font/字送りはinventory-final.json/md、native全glyphはfinal-audit.jsonを参照。
