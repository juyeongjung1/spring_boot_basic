// 作業手順の番号と補足の本文を、折り返しても同じ位置に揃える。
#let exercise-step(id, label, body, above: 22pt) = block(sticky: true, above: above, below: 9pt)[
  #mark(id, "heading")
  #grid(columns: (15pt, 1fr), gutter: 3pt, label, body)
]
#let exercise-item(label, body, left: 11pt, above: 4pt, below: 9pt) = block(
  above: above, below: below, inset: (left: left),
)[
  #grid(columns: (9pt, 1fr), gutter: 4pt,
    text(font: "MS Gothic", size: 9pt, fill: rgb("42586A"), label), body)
]
#let exercise-hint(id, label, body) = block(width: 100%, breakable: false,
  above: 12pt, below: 12pt, inset: (x: 9pt, y: 7pt), fill: rgb("F3F6F8"),
  stroke: (left: 1pt + rgb("8199AE")),
)[
  #mark(id, "hint")
  #text(font: "MS PGothic", size: 11pt, stroke: 0.28pt + rgb("2D4253"), fill: rgb("2D4253"), label)
  #if body != [] {v(5pt); body}
]
#let exercise-check(id, body) = block(sticky: true, above: 30.96pt, below: 7pt)[
  #mark(id, "start")#body#mark(id, "end")
]
