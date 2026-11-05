// 章に依存しない書体・ページ・本文・図版・コードの組版規則。
// 箇条書き記号は、光沢のあるカラー絵文字へ代替されない通常の文字にする。
#show regex("[■●•▪○]"): it => text(font: "MS Gothic", fallback: false,
  weight: "regular", style: "normal", stroke: none, it.text)
#let at(x, y, body) = place(top + left, dx: x * 1pt, dy: y * 1pt, body)
#let styled(style, body, emphasis: false) = {
  let s = styles.at(style)
  let outline = if emphasis {calc.max(s.stroke, s.size / 35)} else {s.stroke}
  text(font: if emphasis {"MS PGothic"} else {s.font}, size: s.size * 1pt,
    weight: s.weight, style: s.slant, fill: rgb(s.color),
    stroke: if outline > 0 {outline * 1pt + rgb(s.color)} else {none}, body)
}
// 比例書体の括弧を全角の字幅で組み、文字が詰まることを防ぐ。
// 原本座標の一字配置には適用せず、本文の自動組版だけで使用する。
#let flowing(body) = {
  show regex("[「」『』【】（）]"): it => context {
    let gothic = repr(text.font).contains("Gothic") or repr(text.font).contains("Meiryo")
    text(font: if gothic {"MS Gothic"} else {"MS Mincho"}, fallback: false,
      features: (halt: 0, palt: 0), it.text)
  }
  body
}
#let glyph(x, y, value, style) = at(x, y, text(top-edge: 0pt, bottom-edge: 0pt)[#styled(style, value)])
#let mark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), y: here().position().y / 1pt)) <book-check>]
// 本文の行送り18ptに対し、段落境界は24ptにする。
#let paragraph(id, body, indent: 11.04pt) = block(above: 0pt, below: 12.96pt)[
  #set par(first-line-indent: (amount: indent, all: true))
  #mark(id, "start")#body#mark(id, "end")
]
#let bullet-paragraph(id, marker, body, continuing: false) = block(
  above: 12.96pt, below: if continuing {6.96pt} else {12.96pt}, inset: (left: 11.04pt))[
  #mark(id, "start")#grid(columns: (12pt, 1fr), column-gutter: 6pt, marker, body)#mark(id, "end")
]
#let list-continuation(id, body, continuing: false) = block(
  above: 0pt, below: if continuing {6.96pt} else {12.96pt}, inset: (left: 29.04pt))[
  #mark(id, "start")#body#mark(id, "end")
]
#let section-heading(id, body, above: 18pt) = block(sticky: true, above: above, below: 12pt)[
  #mark(id, "heading")#body
]
#let step(id, body) = block(sticky: true, above: 8pt, below: 6pt)[
  #mark(id, "heading")#body
]
#let list-item(id, body) = block(above: 12.96pt, below: 12.96pt, inset: (left: 11.04pt))[
  #mark(id, "start")#body#mark(id, "end")
]
#let code-label(id, body) = block(sticky: true, above: 6pt, below: 4pt)[
  #mark(id, "heading")#body
]
#let instruction(id, body, above: 0pt) = block(breakable: false, above: above, below: 12pt)[
  #mark(id, "start")#body#mark(id, "end")
]
#let slide-header(height, body) = block(width: 100%, height: height * 1pt,
  breakable: false, above: 0pt, below: 0pt)[#body]
#let illustration(id, path, width) = block(width: 100%, breakable: false, above: 8pt, below: 12pt)[
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
#let table-panel(id, rows, widths, has_header) = block(above: 8pt, below: 12pt, breakable: true)[#layout(size => {
 let grid = [
  #set text(font: "MS PGothic", size: if widths.len() > 4 {8.5pt} else {9.5pt})
  #set par(leading: 4pt, spacing: 0pt)
  #let cells = ()
  #for (i,row) in rows.enumerate() {
    let current = row.enumerate().map(((j,c)) => table.cell(breakable: false)[#if i == 0 and j == 0 and has_header {mark(id, "table-header")}#text(c.replace("\n", " ").clusters().join("\u{200b}"))])
    if i == 0 and has_header {cells.push(table.header(repeat: true, ..current))}
    else {cells += current}
  }
  #flowing[#table(columns: widths, inset: 3pt, stroke: 0.65pt + rgb("404040"), ..cells)]
 ]
 let short = measure(block(width: size.width, grid)).height <= 600pt
 block(above: 0pt, below: 0pt, breakable: not short)[
   #mark(id, if short {"short-table"} else {"long-table"})
   #mark(id, "start")#grid#mark(id, "end")
 ]
})]
