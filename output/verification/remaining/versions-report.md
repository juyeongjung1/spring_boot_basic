# 年表記・Bootstrap更新報告

基準日: 2026-11-05。対象HEAD: 18e89c0。

Bootstrapの最新安定版は5.3.8（公式ブログの公開日2025-08-25）。6.0.0-alpha.1は予告版のため採用していません。
公式GitHub releaseのpublished_atは2025-08-26T02:04:48Zです。ブログの日付とは別の値として記録しています。

- [公式Versions](https://getbootstrap.com/docs/versions/)
- [公式5.3.8公開記事](https://blog.getbootstrap.com/2025/08/25/bootstrap-5-3-8/)
- [公式導入ガイド・SRI](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [公式配布ZIP](https://github.com/twbs/bootstrap/releases/download/v5.3.8/bootstrap-5.3.8-dist.zip)

更新は教材4ファイル、第5・7章のサンプルHTML18ファイル、第7章4プロジェクトのBootstrap資材88ファイル、計110ファイルです。
教材コード・サンプルHTML・奥付のcopyright年を2027へ統一し、発行/改訂履歴の日付と第三者ライブラリの著作権表記は保存しました。
教材p241-b08は元の文型へ戻し、基準日と版名のみを2026年11月5日・5.3.8へ更新しました。新しい解説は加えていません。

## 検証

- ZIPのSHA-256はGitHub公式asset.digestと一致: `3258c873cbcb1e2d81f4374afea2ea6437d9eee9077041073fd81dd579c5ba6b`。
- コピーした88ファイルはすべて公式ZIP内の同名ファイルとバイト単位で一致。
- 教材4タグ＋プロジェクト10タグ、計14 CDNタグの版名/SRI/crossoriginを照合。
- 配布src内HTMLに2023/2024の年および旧bootstrap@5.3.0の残存なし。
- 本文・演習奥付の発行/改訂履歴はbaselineと一致。
- 奥付のnative更新IDはp296-b04、p077-b04。root側の厳格な年置換対応が必要。
- SRI追加によりp246-b07/b10、p248-b02のコード行数が増加。rootの全体buildで高さを確認。
- 配布ZIPの再生成は完了（852ファイル、全entry bytes/CRC検証済み）。更新対象全パスと前後SHA-256は下表・JSONに収録。

## 本担当で変更していない図版の更新候補

|章|図版ID|原本頁|対象文字|対応|
|---|---|---:|---|---|
|05|p182-f14|182|Copyright © 2023 Trainocate Spring. All rights reserved.|copyright年のみ2027へ|
|05|p186-f17|186|Copyright © 2023 Trainocate Spring. All rights reserved.|copyright年のみ2027へ|
|05|p186-f18|186|Copyright © 2023 Trainocate Spring. All rights reserved.|copyright年のみ2027へ|
|ex05|p041-f04|41|Copyright © 2023 Trainocate Spring. All rights reserved.|copyright年のみ2027へ|
|ex05|p041-f05|41|Copyright © 2023 Trainocate Spring. All rights reserved.|copyright年のみ2027へ|
|appendix-a|p285-f07|285|Finished at: 2024-01-23T21:27:55+09:00|ユーザー指摘の2024→2027。元画像は本担当では変更せずroot判断へ|
|07|p245-f05|245|bootstrap@5.3.0（CSSとJSのCDN各1か所）|5.3.8へ。CDN/SRIも本文と整合|

## 更新ファイルとSHA-256

|ファイル|種別|更新後SHA-256|
|---|---|---|
|docs/textbook/chapters/05/chapter.md|chapter-version-or-year|`1977502b0c2a3a28cfe8e1e918877bbe3ec37ab0833324f52c614f3a688e61d8`|
|docs/textbook/chapters/07/chapter.md|chapter-version-or-year|`f95a194f70dc8b7366def8e8d5d1a12e1fa503b9ba2ce426217e73d47a80e758`|
|docs/textbook/chapters/appendix-b/chapter.md|chapter-version-or-year|`0333a8031402361ca8dae9751aa9d2501bd5fb12b2a5377099a991455bb3b04d`|
|docs/textbook/chapters/ex-back/chapter.md|chapter-version-or-year|`d5bb1243ca35bcc7489d06a8dc436c94e13b9d08b889c2d5ba996211341cca61`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-grid.css|bootstrap-local|`debef2607bc18da92921bd9559ec954a397ba5439d295e4face3e76f98dab9f3`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-grid.min.css|bootstrap-local|`8d09c629f0198c538a1f46908e742b247d2b1398e95669c4a820ab3d65c92ffc`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-grid.rtl.css|bootstrap-local|`76a8a1d40131b5b25964ea91c691cb86f272c528e99b497201c7ce0bf8412d99`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-grid.rtl.min.css|bootstrap-local|`0cf051030566300dbe5c37316e51741de3f1070c99d69b6ab451454c88740fd1`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-reboot.css|bootstrap-local|`aab39007c15ae7165880653e69a970e48d561049f8633ac31bba21aea46c412e`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-reboot.min.css|bootstrap-local|`0b56cde507cfa4d5d219f71df2e2d0a9b14bd6f589583818b874fb026f0f47f7`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-reboot.rtl.css|bootstrap-local|`7fc078a56fb233e9a0cdf681cbd0efab514c121ef958818afc293b6f5e920492`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-reboot.rtl.min.css|bootstrap-local|`34dd5626c71e17acb8a2b1912d99b83d4d2a1b8e8bffab35942c7af43d4a06b4`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-utilities.css|bootstrap-local|`390f9de7afef4c3a68368f96899fa0ef6a08c3afb1599c7ea288d97ac89a23ff`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-utilities.min.css|bootstrap-local|`ed4cbc75169db612c3c73279698890dcdadc514094798686cae1cadda536bced`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-utilities.rtl.css|bootstrap-local|`2ea67a2d49c828015ef5f5f0988e2f9815625a13db312b459ea4c07602c8e2da`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap-utilities.rtl.min.css|bootstrap-local|`1bc8db7e861d1eb6a6ed461dd1a4e081f30a5714b980129d1d54589f21bc822a`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap.css|bootstrap-local|`4a50207b956a4ab943640ee993118b554a34e96a23261cfe58b9aa1807a7849b`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap.min.css|bootstrap-local|`d85327d99c7a3ee1f9b5d0500d1370acea3ad2db39c163c2f51f232baedbdede`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap.rtl.css|bootstrap-local|`39911412c957c60512a4b23a0ea1903ed5f3a0f9f7bb7446c55a99bb2e5f7463`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/css/bootstrap.rtl.min.css|bootstrap-local|`b9048c83571ab73da54395b6b307219f9eb9c5447f4f8edb17a069eb0f19465a`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.bundle.js|bootstrap-local|`69566344cf5722be51acbc90fdb26c24eb01cc1c153f738b16b2fa87ccd3b510`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.bundle.min.js|bootstrap-local|`e4fd49181388c48ec5040bd3fe66f57c29c8e67fcd8502b3354b96ec7ab47cc7`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.esm.js|bootstrap-local|`3c36e18ebe2539579edf7e440f3e02bcc46c2ad9efbc55b219b732af355d0aab`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.esm.min.js|bootstrap-local|`f9280841ae00ff8c36baa9e829833dd9fc893c70d67b63c552f601a88fdfbc81`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.js|bootstrap-local|`1b6e856e8a636bcdde4588e63a1061ced96edbb468127b25243629634d402079`|
|projects/spring_answer/spring_answer_7/src/main/resources/static/js/bootstrap.min.js|bootstrap-local|`7b0f14895d69247fd88e93840489cfd47c55bd3fd27eb0a6c12a14cc5f492207`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-grid.css|bootstrap-local|`debef2607bc18da92921bd9559ec954a397ba5439d295e4face3e76f98dab9f3`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-grid.min.css|bootstrap-local|`8d09c629f0198c538a1f46908e742b247d2b1398e95669c4a820ab3d65c92ffc`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-grid.rtl.css|bootstrap-local|`76a8a1d40131b5b25964ea91c691cb86f272c528e99b497201c7ce0bf8412d99`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-grid.rtl.min.css|bootstrap-local|`0cf051030566300dbe5c37316e51741de3f1070c99d69b6ab451454c88740fd1`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-reboot.css|bootstrap-local|`aab39007c15ae7165880653e69a970e48d561049f8633ac31bba21aea46c412e`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-reboot.min.css|bootstrap-local|`0b56cde507cfa4d5d219f71df2e2d0a9b14bd6f589583818b874fb026f0f47f7`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-reboot.rtl.css|bootstrap-local|`7fc078a56fb233e9a0cdf681cbd0efab514c121ef958818afc293b6f5e920492`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-reboot.rtl.min.css|bootstrap-local|`34dd5626c71e17acb8a2b1912d99b83d4d2a1b8e8bffab35942c7af43d4a06b4`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-utilities.css|bootstrap-local|`390f9de7afef4c3a68368f96899fa0ef6a08c3afb1599c7ea288d97ac89a23ff`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-utilities.min.css|bootstrap-local|`ed4cbc75169db612c3c73279698890dcdadc514094798686cae1cadda536bced`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-utilities.rtl.css|bootstrap-local|`2ea67a2d49c828015ef5f5f0988e2f9815625a13db312b459ea4c07602c8e2da`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap-utilities.rtl.min.css|bootstrap-local|`1bc8db7e861d1eb6a6ed461dd1a4e081f30a5714b980129d1d54589f21bc822a`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap.css|bootstrap-local|`4a50207b956a4ab943640ee993118b554a34e96a23261cfe58b9aa1807a7849b`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap.min.css|bootstrap-local|`d85327d99c7a3ee1f9b5d0500d1370acea3ad2db39c163c2f51f232baedbdede`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap.rtl.css|bootstrap-local|`39911412c957c60512a4b23a0ea1903ed5f3a0f9f7bb7446c55a99bb2e5f7463`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/css/bootstrap.rtl.min.css|bootstrap-local|`b9048c83571ab73da54395b6b307219f9eb9c5447f4f8edb17a069eb0f19465a`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.bundle.js|bootstrap-local|`69566344cf5722be51acbc90fdb26c24eb01cc1c153f738b16b2fa87ccd3b510`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.bundle.min.js|bootstrap-local|`e4fd49181388c48ec5040bd3fe66f57c29c8e67fcd8502b3354b96ec7ab47cc7`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.esm.js|bootstrap-local|`3c36e18ebe2539579edf7e440f3e02bcc46c2ad9efbc55b219b732af355d0aab`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.esm.min.js|bootstrap-local|`f9280841ae00ff8c36baa9e829833dd9fc893c70d67b63c552f601a88fdfbc81`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.js|bootstrap-local|`1b6e856e8a636bcdde4588e63a1061ced96edbb468127b25243629634d402079`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/static/js/bootstrap.min.js|bootstrap-local|`7b0f14895d69247fd88e93840489cfd47c55bd3fd27eb0a6c12a14cc5f492207`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-grid.css|bootstrap-local|`debef2607bc18da92921bd9559ec954a397ba5439d295e4face3e76f98dab9f3`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-grid.min.css|bootstrap-local|`8d09c629f0198c538a1f46908e742b247d2b1398e95669c4a820ab3d65c92ffc`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-grid.rtl.css|bootstrap-local|`76a8a1d40131b5b25964ea91c691cb86f272c528e99b497201c7ce0bf8412d99`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-grid.rtl.min.css|bootstrap-local|`0cf051030566300dbe5c37316e51741de3f1070c99d69b6ab451454c88740fd1`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-reboot.css|bootstrap-local|`aab39007c15ae7165880653e69a970e48d561049f8633ac31bba21aea46c412e`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-reboot.min.css|bootstrap-local|`0b56cde507cfa4d5d219f71df2e2d0a9b14bd6f589583818b874fb026f0f47f7`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-reboot.rtl.css|bootstrap-local|`7fc078a56fb233e9a0cdf681cbd0efab514c121ef958818afc293b6f5e920492`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-reboot.rtl.min.css|bootstrap-local|`34dd5626c71e17acb8a2b1912d99b83d4d2a1b8e8bffab35942c7af43d4a06b4`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-utilities.css|bootstrap-local|`390f9de7afef4c3a68368f96899fa0ef6a08c3afb1599c7ea288d97ac89a23ff`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-utilities.min.css|bootstrap-local|`ed4cbc75169db612c3c73279698890dcdadc514094798686cae1cadda536bced`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-utilities.rtl.css|bootstrap-local|`2ea67a2d49c828015ef5f5f0988e2f9815625a13db312b459ea4c07602c8e2da`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap-utilities.rtl.min.css|bootstrap-local|`1bc8db7e861d1eb6a6ed461dd1a4e081f30a5714b980129d1d54589f21bc822a`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap.css|bootstrap-local|`4a50207b956a4ab943640ee993118b554a34e96a23261cfe58b9aa1807a7849b`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap.min.css|bootstrap-local|`d85327d99c7a3ee1f9b5d0500d1370acea3ad2db39c163c2f51f232baedbdede`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap.rtl.css|bootstrap-local|`39911412c957c60512a4b23a0ea1903ed5f3a0f9f7bb7446c55a99bb2e5f7463`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/css/bootstrap.rtl.min.css|bootstrap-local|`b9048c83571ab73da54395b6b307219f9eb9c5447f4f8edb17a069eb0f19465a`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.bundle.js|bootstrap-local|`69566344cf5722be51acbc90fdb26c24eb01cc1c153f738b16b2fa87ccd3b510`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.bundle.min.js|bootstrap-local|`e4fd49181388c48ec5040bd3fe66f57c29c8e67fcd8502b3354b96ec7ab47cc7`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.esm.js|bootstrap-local|`3c36e18ebe2539579edf7e440f3e02bcc46c2ad9efbc55b219b732af355d0aab`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.esm.min.js|bootstrap-local|`f9280841ae00ff8c36baa9e829833dd9fc893c70d67b63c552f601a88fdfbc81`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.js|bootstrap-local|`1b6e856e8a636bcdde4588e63a1061ced96edbb468127b25243629634d402079`|
|projects/enshu_answer/enshu_answer_7/src/main/resources/static/js/bootstrap.min.js|bootstrap-local|`7b0f14895d69247fd88e93840489cfd47c55bd3fd27eb0a6c12a14cc5f492207`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-grid.css|bootstrap-local|`debef2607bc18da92921bd9559ec954a397ba5439d295e4face3e76f98dab9f3`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-grid.min.css|bootstrap-local|`8d09c629f0198c538a1f46908e742b247d2b1398e95669c4a820ab3d65c92ffc`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-grid.rtl.css|bootstrap-local|`76a8a1d40131b5b25964ea91c691cb86f272c528e99b497201c7ce0bf8412d99`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-grid.rtl.min.css|bootstrap-local|`0cf051030566300dbe5c37316e51741de3f1070c99d69b6ab451454c88740fd1`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-reboot.css|bootstrap-local|`aab39007c15ae7165880653e69a970e48d561049f8633ac31bba21aea46c412e`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-reboot.min.css|bootstrap-local|`0b56cde507cfa4d5d219f71df2e2d0a9b14bd6f589583818b874fb026f0f47f7`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-reboot.rtl.css|bootstrap-local|`7fc078a56fb233e9a0cdf681cbd0efab514c121ef958818afc293b6f5e920492`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-reboot.rtl.min.css|bootstrap-local|`34dd5626c71e17acb8a2b1912d99b83d4d2a1b8e8bffab35942c7af43d4a06b4`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-utilities.css|bootstrap-local|`390f9de7afef4c3a68368f96899fa0ef6a08c3afb1599c7ea288d97ac89a23ff`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-utilities.min.css|bootstrap-local|`ed4cbc75169db612c3c73279698890dcdadc514094798686cae1cadda536bced`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-utilities.rtl.css|bootstrap-local|`2ea67a2d49c828015ef5f5f0988e2f9815625a13db312b459ea4c07602c8e2da`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap-utilities.rtl.min.css|bootstrap-local|`1bc8db7e861d1eb6a6ed461dd1a4e081f30a5714b980129d1d54589f21bc822a`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap.css|bootstrap-local|`4a50207b956a4ab943640ee993118b554a34e96a23261cfe58b9aa1807a7849b`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap.min.css|bootstrap-local|`d85327d99c7a3ee1f9b5d0500d1370acea3ad2db39c163c2f51f232baedbdede`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap.rtl.css|bootstrap-local|`39911412c957c60512a4b23a0ea1903ed5f3a0f9f7bb7446c55a99bb2e5f7463`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/css/bootstrap.rtl.min.css|bootstrap-local|`b9048c83571ab73da54395b6b307219f9eb9c5447f4f8edb17a069eb0f19465a`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.bundle.js|bootstrap-local|`69566344cf5722be51acbc90fdb26c24eb01cc1c153f738b16b2fa87ccd3b510`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.bundle.min.js|bootstrap-local|`e4fd49181388c48ec5040bd3fe66f57c29c8e67fcd8502b3354b96ec7ab47cc7`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.esm.js|bootstrap-local|`3c36e18ebe2539579edf7e440f3e02bcc46c2ad9efbc55b219b732af355d0aab`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.esm.min.js|bootstrap-local|`f9280841ae00ff8c36baa9e829833dd9fc893c70d67b63c552f601a88fdfbc81`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.js|bootstrap-local|`1b6e856e8a636bcdde4588e63a1061ced96edbb468127b25243629634d402079`|
|projects/enshu_exercise/enshu_exercise_7/src/main/resources/static/js/bootstrap.min.js|bootstrap-local|`7b0f14895d69247fd88e93840489cfd47c55bd3fd27eb0a6c12a14cc5f492207`|
|projects/enshu_answer/enshu_answer_5/src/main/resources/templates/layout.html|html-year-or-cdn|`fdca7e6ad4b15950f63e08106ab79909a1cd2c8c7036f476f7fb345398de6a40`|
|projects/enshu_exercise/enshu_exercise_5/src/main/resources/templates/layout.html|html-year-or-cdn|`c24210557decff3322009298910c75b66115d270434603e2932d9a676ca88edc`|
|projects/spring_answer/spring_answer_5/src/main/resources/templates/layout.html|html-year-or-cdn|`ba51804d652187e110f1a15cc1387cd6107f30a69f6f95309f01aa933f22ca2b`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/bootstrap_setup.html|html-year-or-cdn|`bdcf59a3c9ce9f7fc86d517ccd96815f653a69bf07e562e64c1278b82d026d41`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/form_sample.html|html-year-or-cdn|`4776244cda76502fabe6347c3a017009d3c0fba88729c03302eb5732d188967c`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/grid_sample.html|html-year-or-cdn|`3e3801c6bc159c787005dcb2b80f676c4ef13a8d6101218269cdd0a5bedfa752`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/grid_sample2.html|html-year-or-cdn|`d89cbdd425418fcf92bc5701ffa562fa80a691a0e7d2ade67724eef94660c11d`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/layout.html|html-year-or-cdn|`ba51804d652187e110f1a15cc1387cd6107f30a69f6f95309f01aa933f22ca2b`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/product/product_search.html|html-year-or-cdn|`4d92f4c947da5fe2d618b07423e237df08a8308c5d3ba468c11c61447ae20d05`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/style_sample.html|html-year-or-cdn|`7d0cfc4eb9366519e4d7fe49b43cf5df69f41ca2222b0b62514299c466c72e33`|
|projects/spring_exercise/spring_exercise_5/src/main/resources/templates/layout.html|html-year-or-cdn|`ba51804d652187e110f1a15cc1387cd6107f30a69f6f95309f01aa933f22ca2b`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/templates/form_sample.html|html-year-or-cdn|`aa9bac7788a3f11b73cca44a004f1c93b1e514022c79ebda3d2eca26f587f355`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/templates/grid_sample.html|html-year-or-cdn|`d01b06509280332b41ecb084ad64e8c229935bdbde5d4a57d02a0e420d6dc4c7`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/templates/grid_sample2.html|html-year-or-cdn|`d89cbdd425418fcf92bc5701ffa562fa80a691a0e7d2ade67724eef94660c11d`|
|projects/spring_exercise/spring_exercise_7/src/main/resources/templates/style_sample.html|html-year-or-cdn|`3d0ef0d414792856acf3301db351c0381bd936bb55d7da40a9072c690b316557`|
|projects/spring_answer/spring_answer_5/src/main/resources/templates/product/layout.html|html-year-or-cdn|`e7c39c66058d468576a6c1a56e55b6528831029ca26e47675f6d6e219d5fcbf2`|
|projects/spring_answer/spring_answer_7/src/main/resources/templates/product/layout.html|html-year-or-cdn|`e7c39c66058d468576a6c1a56e55b6528831029ca26e47675f6d6e219d5fcbf2`|
|projects/spring_exercise/spring_exercise_5/src/main/resources/templates/product/layout.html|html-year-or-cdn|`e7c39c66058d468576a6c1a56e55b6528831029ca26e47675f6d6e219d5fcbf2`|

## 第7章4アプリのパッケージ検証（追加）

Java 21（Temurin 21.0.13+9）・Maven 3.9.9で `mvn -B -ntp -DskipTests package` を4アプリ順次実行し、全てBUILD SUCCESSでした。
既存targetの削除やcleanは行っていません。MAVEN_OPTSは `-Xmx384m -Dfile.encoding=UTF-8` です。

生成JAR内のBootstrap CSS/JS計88ファイルは、各srcおよび公式5.3.8配布ZIPとバイト単位で一致し、全ファイルの版ヘッダーも5.3.8でした。
更新した第7章HTML 12ファイルもJAR内とsrcが一致しました。各JARのBuild-Jdk-Spec:21、Spring-Boot-Version:4.0.2を確認しました。

今回はJavaコード不変の資材更新の確認です。JUnit実行はskipし、DB検証・HTTP起動・全27アプリのJUnit再実行は実施していません。配布ZIPはtargetを除外して再生成・全件検証済みです。

既存targetの復元時刻により一部HTMLのコピーが省略されたため、対象src HTML12件の内容/SHAを維持して更新時刻だけを更新し、spring側2本を再packageしました。以下は修正後の最終JARの結果です。

|アプリ|package|Bootstrap資材数|更新HTML数|処理秒|JAR SHA-256|
|---|---|---:|---:|---:|---|
|spring_answer_7|成功|22|8|21.03|`1d32e526baf9b89a87500899e2fb9a826b12edf524740ded5f62b2598dc1fedd`|
|spring_exercise_7|成功|22|4|19.77|`4dcc30f3f87b5e695a75e0dd62127632a9d5e5452ea79dd2445dbf1e8a7ecaf4`|
|enshu_answer_7|成功|22|0|13.21|`6e3ff6e885e585606dfe234174ba85f1e16b855bff3f53dac275e6cc2b5df960`|
|enshu_exercise_7|成功|22|0|11.1|`faf61758120f540a9c921c1c564235ea3ee0c09e65df9fafeda8ea221252cdc1`|

## 最終配布ZIP（LF設定を含む）

`SpringBootBasic_Java21_Boot4.0.2.zip` を852ファイルで最終再生成しました。`.gitattributes` のCSS/JS用 `text eol=lf` 2行を含み、前回ZIPから変わったファイルはこの1件のみです。Bootstrap 88資材のSHAは公式配布物と同じ値を維持しています。

最終SHA-256: `8dff9ef63b0dc5f24a147e9a19e6624045bcde3b1ff86428c9010a23432c1202`。全852エントリのbytes一致・CRCエラー0を再確認しました。JARの再packageは行っていません。
