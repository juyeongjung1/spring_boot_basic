# URI注釈分割数と論理リンク保持の独立照合

判定：合格。

旧/新の各URLを章・同じHTML部品ID/consume元ID（部品外は元ブロック、境界未確定時は元頁）へ対応付け、注釈矩形で取得できる可視文字を連結。空白とゼロ幅文字を除き、宛先URL全字が各論理出現でクリック可能であり、その出現数と所属元IDが同一であることを要求する。矩形に隣接する引用符・句読点が入る場合も、URL本体の全字を必須とする。

|冊子|旧矩形数|新矩形数|旧論理URL数|新論理URL数|
|---|---:|---:|---:|---:|
|textbook|70|63|59|59|
|exercise|19|19|19|19|

矩形数だけが変わった部品：

|章|部品|宛先|旧矩形|新矩形|論理出現|
|---|---|---|---:|---:|---:|
|02|02-explanation-11|http://www.thymeleaf.org|2|1|1|
|02|02-explanation-2|http://www.thymeleaf.org|2|1|1|
|05|05-explanation-1|http://www.thymeleaf.org|2|1|1|
|05|05-explanation-2|http://www.ultraq.net.nz/thymeleaf/layout|3|1|1|
|05|05-explanation-3|http://www.ultraq.net.nz/thymeleaf/layout|3|1|1|
