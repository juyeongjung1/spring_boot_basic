# 教材85ページのMarkdownとPDFの試作

章扉・通常本文・表・演習の追加試作と自動改ページの検証は、[追加試作の説明](extended/README.md)にまとめています。

既存PDFの85ページ「3.4. 全件検索」を、MarkdownとTypstのテンプレートから再現する試作です。スライド・見出し・行番号付きコード・ファイル名の赤枠・注釈矢印が同じページにあるため、代表例に選びました。教材内容やコードの仕様は変更していません。

## 編集元と生成物

- `page85.md`：章見出し、手順見出し、スライド参照、15行のJavaコード、ページ番号。
- `layout.typ`：書体・ページサイズ・配置用の共通関数。
- `build.py`：PandocでMarkdownを読み、85ページ用の配置を適用してTypstでPDFを生成。比較用の画像と数値も出力。
- `assets/findall-slide.svg`：元PDFのスライド領域を抽出したベクター図版。文字も輪郭として保持し、フォント置換による崩れを防止。
- `assets/findall-slide.sldx`：Word内に埋め込まれていたPowerPointスライドの元データ。
- `generated.typ`：自動生成される中間ファイル。直接編集しません。

生成物はリポジトリ直下の `output/pdf/prototype/` に出力します。

| ファイル | 内容 |
| --- | --- |
| `page85.pdf` | Markdownから生成した試作PDF |
| `reference-page85.pdf` | 元PDFから取り出した比較基準の85ページ |
| `comparison.pdf` | 左が元PDF、右が試作PDFの見開き比較 |
| `comparison.png` | 同じ見開き比較の144dpi画像 |
| `overlay.png` | 元PDFと試作PDFを50%ずつ重ねた画像 |
| `difference.png` | 差が一定のしきい値を超えた画素を黒で表示 |
| `comparison.json` | 元PDFのハッシュ、領域別の画素差、主要文字列の座標 |

## 再生成

Windowsと元教材のWord・PDFが必要です。フォントはWindowsのMS ゴシック、MS Pゴシック、Meiryo UI、Times New Romanを使用します。フォントファイルはリポジトリへ複製していません。今回確認したPandocは3.9.0.2、Typstは0.15.0です。

Python 3.12での実行例です。環境構築後、最後のコマンドで再生成できます。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r docs/prototype/requirements.txt
.\.venv\Scripts\python.exe docs/prototype/build.py
```

Pandocは別途インストールしてPATHへ登録します。元教材はルートにある次の2ファイルを使用します。

- `JAC0177G-T1-04(260715).pdf`
- `JAC0177G-T1-04(260715修正).docx`

## 比較結果と適用範囲

スライドは既存図版を保持し、見出しとコードはMarkdownの文字から再組版しています。ページ全体を画像にして貼り付ける方式ではありません。生成PDF内のJavaコードは文字として検索できます。

主要コード文字列の横位置は元PDFと一致し、縦の文字境界の差は約0.005ptです。章見出しの測定領域は144dpiの画像比較で差がありませんでした。スライド内の輪郭描画、MS Pゴシックの細かい字間や太さには差が残ります。比較画像とJSONは再生成ごとに更新されます。

画素差はRGB各成分の絶対差の平均で、0は画素が一致、255は最大差です。白地も含むため、一致率や文書全体の品質点数としては扱いません。

この試作は85ページの配置を測定した固定レイアウトです。本文の追加や行数変更に伴う自動改ページ、他ページへの展開、索引は未実装です。全体移行では、章扉・通常本文・表・演習ページも試作して共通の組版規則を確立します。

スライド内の文章や図を修正する場合は、保持したPowerPoint元データまたは図版自体の編集が必要です。SVGは既存PDFから抽出しているため、PowerPointを再描画した際の互換性までは検証していません。
