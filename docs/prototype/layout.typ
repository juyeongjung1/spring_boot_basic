// 本文85ページの位置と書体を検証する試作専用テンプレート。
// 座標は元PDFを測定したpt値。全章共通の組版規則は別途検証する。
#set page(width: 595.32pt, height: 841.92pt, margin: 0pt)
#set text(lang: "ja", font: "Meiryo UI", cjk-latin-spacing: none, kerning: false, overhang: false)
#let red = rgb("FF0000")
#let blue = rgb("0000FF")
#let at(x, y, body) = place(top + left, dx: x * 1pt, dy: y * 1pt, body)
#let label(x, y, value, font: "Meiryo UI", size: 9.96, weight: "regular", fill: black, stroke: none, tracking: 0pt) = at(x, y, text(font: font, size: size * 1pt, weight: weight, fill: fill, stroke: stroke, tracking: tracking, top-edge: 0pt, bottom-edge: 0pt, value))
#let panel(x, y, w, h, fill: none, stroke: none) = at(x, y, rect(width: w * 1pt, height: h * 1pt, fill: fill, stroke: stroke))
