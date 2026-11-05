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
#let code-label(id, body) = block(sticky: true, above: 6pt, below: 4pt)[
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
#let code-panel(id, lines, language) = block(breakable: true, above: 8pt, below: 12pt)[#layout(size => {
  let code = [
    #set text(font: "MS Gothic", size: 12pt)
    #set par(leading: 6pt, spacing: 0pt)
    #show raw: set text(font: "MS Gothic", size: 12pt)
    #show raw.where(block: true): set block(breakable: true)
    #show regex("[A-Za-z0-9_]{20,}"): it => it.text.clusters().join("\u{200b}")
    #raw(lines.join("\n"), block: true, lang: language, theme: "/tools/textbook/code.tmTheme")
  ]
  // 見出しとファイル名にも領域を残し、大きなコードは行間で継続させる。
  let short = measure(block(width: size.width, inset: 6pt, code)).height <= 600pt
  block(breakable: not short, fill: rgb("FFFBF0"), stroke: 0.48pt, inset: 6pt, above: 0pt, below: 0pt)[
    #mark(id, if short {"short-code"} else {"long-code"})
    #mark(id, "start")#code#mark(id, "end")
  ]
})]
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
#let native-cover(body) = at(-85.104, -86, box(width: 595.32pt, height: 841.92pt)[#body])
#let table-panel(id, rows, widths, has_header) = layout(size => {
 let grid = [
  #set text(font: "MS PGothic", size: if widths.len() > 4 {8.5pt} else {9.5pt})
  #set par(leading: 4pt, spacing: 0pt)
  #let cells = ()
  #for (i,row) in rows.enumerate() {
    let current = row.enumerate().map(((j,c)) => table.cell(breakable: false)[#if i == 0 and j == 0 and has_header {mark(id, "table-header")}#text(c.replace("\n", " ").clusters().join("\u{200b}"))])
    if i == 0 and has_header {cells.push(table.header(repeat: true, ..current))}
    else {cells += current}
  }
  #table(columns: widths, inset: 3pt, stroke: 0.5pt + rgb("C8CBD5"), ..cells)
 ]
 let short = measure(block(width: size.width, grid)).height <= 600pt
 block(above: 8pt, below: 12pt, breakable: not short)[
   #mark(id, if short {"short-table"} else {"long-table"})
   #mark(id, "start")#grid#mark(id, "end")
 ]
})
