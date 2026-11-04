// 章に依存しない書体・ページ・本文・図版・コードの組版規則。
#let at(x, y, body) = place(top + left, dx: x * 1pt, dy: y * 1pt, body)
#let styled(style, body) = {
  let s = styles.at(style)
  text(font: s.font, size: s.size * 1pt, weight: s.weight, style: s.slant,
    fill: rgb(s.color), stroke: if s.stroke > 0 {s.stroke * 1pt + rgb(s.color)} else {none}, body)
}
#let glyph(x, y, value, style) = at(x, y, text(top-edge: 0pt, bottom-edge: 0pt)[#styled(style, value)])
#let mark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), y: here().position().y / 1pt)) <book-check>]
#let paragraph(id, body) = block(above: 0pt, below: 6pt)[
  #mark(id, "start")#h(11.04pt)#body#mark(id, "end")
]
#let section-heading(id, body) = block(sticky: true, above: 18pt, below: 12pt)[
  #mark(id, "heading")#body
]
#let step(id, body) = block(sticky: true, above: 8pt, below: 6pt)[
  #mark(id, "heading")#body
]
#let instruction(id, body) = block(breakable: false, above: 0pt, below: 0pt)[
  #mark(id, "start")#body#mark(id, "end")
]
#let illustration(id, path, width) = block(breakable: false, above: 8pt, below: 12pt)[
  #mark(id, "start")
  #align(center, image(path, width: calc.min(width * 1pt, 426.672pt)))
  #mark(id, "end")
]
#let code-panel(id, lines, language) = block(breakable: lines.len() * 18pt + 12pt > 687.92pt,
  fill: rgb("FFFBF0"), stroke: 0.48pt, inset: 6pt, above: 8pt, below: 12pt)[
  #set text(font: "MS Gothic", size: 12pt)
  #set par(leading: 6pt, spacing: 0pt)
  #mark(id, "start")
  #show raw: set text(font: "MS Gothic", size: 12pt)
  #raw(lines.join("\n"), block: true, lang: language, theme: "/tools/textbook/code.tmTheme")
  #mark(id, "end")
]
#let cover-content(number, title, goal_title, goals) = {
  at(461.38, 0.12, rect(width: 132.26pt, height: 127.7pt, stroke: none, fill: rgb(91.4%, 29.4%, 13.3%)))
  at(513.7, 88.46, text(font: "Arial", weight: "black", size: 72pt, fill: white, top-edge: 0pt, bottom-edge: 0pt, number))
  at(85.104, 328.25, text(font: "Meiryo UI", weight: "bold", size: 24pt, top-edge: 0pt, bottom-edge: 0pt, title))
  at(83.664, 333.89, rect(width: 428.11pt, height: 0.48pt, fill: black, stroke: none))
  at(85.104, 372.17, text(font: "Meiryo UI", weight: "bold", size: 18pt, top-edge: 0pt, bottom-edge: 0pt, goal_title))
  for (i, goal) in goals.enumerate() {
    at(96.144, 401.69 + i * 24.01, text(font: "Meiryo UI", weight: "bold", size: 14.04pt, top-edge: 0pt, bottom-edge: 0pt)[■#h(14pt)#goal])
  }
}
#let cover(number, title, goal_title, goals) = at(-85.104, -86,
  box(width: 595.32pt, height: 841.92pt)[#cover-content(number, title, goal_title, goals)])
