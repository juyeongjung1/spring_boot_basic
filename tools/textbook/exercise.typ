#let exercise-title(label, size: 15pt) = text(font: "Meiryo UI", weight: "bold",
  size: size, cjk-latin-spacing: none, label)
#let exercise-toc-title(x, y, number-x, label, size) = context {
  let body = text(top-edge: 0pt, bottom-edge: 0pt, exercise-title(label, size: size))
  let start = x + measure(body).width + 4pt
  let length = number-x - start - 4pt
  assert(length > 4pt, message: "演習目次の見出しが幅に収まりません")
  at(x / 1pt, y / 1pt, body)
  at(start / 1pt, (y - 1.4pt) / 1pt,
    line(length: length, stroke: (paint: black, thickness: 0.85pt, cap: "round", dash: "dotted")))
}
// 作業手順の番号と補足の本文を、折り返しても同じ位置に揃える。
#let exercise-step(id, label, body, above: 22pt) = block(sticky: true, above: above, below: 9pt)[
  #mark(id, "heading")
  #grid(columns: (15pt, 1fr), gutter: 3pt, label, body)
]
#let exercise-item(label, body, left: 11pt, above: 4pt, below: 9pt) = block(
  above: above, below: below, inset: (left: left),
)[
  #let numbered = "➀➁➂➃➄➅➆➇➈➉".contains(label)
  #grid(columns: (if numbered {11pt} else {9pt}, 1fr), gutter: if numbered {2pt} else {4pt},
    text(font: if numbered {"Segoe UI Symbol"} else {"MS Gothic"},
      size: if numbered {10.5pt} else {9pt}, fill: black, label), body)
]
#let exercise-hint(id, body) = block(width: 100%, breakable: false,
  above: 11pt, below: 11pt, inset: (left: 11pt),
)[
  #block(width: 100%, inset: (x: 8pt, y: 5pt), fill: rgb("F3F6FA"),
    stroke: 0.55pt + rgb("C6D3DF"), radius: 3pt)[
    #mark(id, "hint")
    #box(baseline: -1pt, circle(radius: 2.4pt, stroke: 0.8pt + rgb("24526E")))#h(5pt)
    #text(fill: rgb("24526E"), exercise-title("ヒント", size: 11pt))
    #if body != [] {v(4pt); body}
  ]
]
#let exercise-warning(id, label, body) = block(inset: (left: 11pt), above: 8pt, below: 9pt)[
  #mark(id, "start")
  #set par(leading: 5pt)
  #set text(fill: rgb("FF0000"))
  #grid(columns: (auto, 1fr), gutter: 6pt,
    underline(evade: false, exercise-title(label, size: 16pt)),
    underline(evade: false, exercise-title(body, size: 16pt)))
  #mark(id, "end")
]
#let exercise-check(id, body) = block(sticky: true, above: 30.96pt, below: 7pt)[
  #mark(id, "start")#body#mark(id, "end")
]
