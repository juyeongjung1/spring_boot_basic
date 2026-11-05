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
#let mark(id, edge) = context [#metadata((id: id, edge: edge, page: here().page(), x: here().position().x / 1pt, y: here().position().y / 1pt)) <book-check>]
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
#let html-panel(id, width, height, offset: 0pt, body) = block(width: 100%,
  breakable: false, above: 8pt, below: 12pt)[
  #block(width: width * 1pt, height: height * 1pt, inset: 0pt, above: 0pt, below: 0pt)[
    #at(offset / 1pt, 0, [#mark(id, "html-component")#body])
  ]
]
#let reference-panel(body) = block(width: 100%, breakable: true, above: 18pt,
  below: 12pt, inset: 8pt, fill: rgb("F5F8FC"), stroke: 0.65pt + rgb("A6B8CE"), radius: 4pt)[
  #body
]
#let slide-header(height, body) = block(width: 100%, height: height * 1pt,
  breakable: false, above: 0pt, below: 0pt)[#body]
#let illustration(id, path, width, offset: 0pt) = block(width: 100%, breakable: false,
  inset: (left: offset), above: 8pt, below: 12pt)[
  #mark(id, "start")
  #image(path, width: width * 1pt)
  #mark(id, "end")
]
#let code-fragment(lines, language, font-size: 12pt, leading: 6pt) = [
  #set text(font: "MS Gothic", size: font-size)
  #set par(leading: leading, spacing: 0pt)
  #show raw: set text(font: "MS Gothic", size: font-size)
  #show raw.where(block: true): set block(breakable: true)
  #show regex("[A-Za-z0-9_]{20,}"): it => it.text.clusters().join("\u{200b}")
  #raw(lines.join("\n"), block: true, lang: language, theme: "/tools/textbook/code.tmTheme")
]
#let code-panel(id, lines, language, width: auto, offset: 0pt, left: 6pt, right: 6pt,
  top: 6pt, bottom: 6pt, source-height: 0pt, framed: true, filled: true, caption: [],
  caption-height: 0pt, header-height: 0pt, underlay: [], overlay: [], tail: 0pt,
  above: 8pt, font-size: 12pt, leading: 6pt, content: none) = block(width: 100%, breakable: true, inset: (left: offset), above: above, below: 12pt)[#layout(size => {
  let panel-width = if width == auto {size.width} else {width}
  let code = if content == none {code-fragment(lines, language, font-size: font-size, leading: leading)} else {content}
  let padding = (left: left, right: right, top: top, bottom: bottom)
  let height = calc.max(source-height, measure(block(width: panel-width, inset: padding, code)).height)
  let short = height + caption-height + tail <= 650pt
  block(width: panel-width, breakable: not short, above: 0pt, below: 0pt)[
    #if caption-height > 0pt {
      block(height: caption-height, sticky: true, above: 0pt, below: 0pt)[#caption]
    }
    #block(width: panel-width, height: if short {height} else {auto}, breakable: not short,
      fill: if filled {rgb("FFFBF0")} else {none}, stroke: if framed {0.48pt} else {none},
      above: 0pt, below: 0pt)[
      #mark(id, if short {"short-code"} else {"long-code"})#mark(id, "start")
      #if header-height > 0pt {
        at(0.5, 0.5, rect(width: panel-width - 1pt, height: header-height - 0.5pt, fill: white, stroke: none))
      }
      #underlay
      #overlay
      #block(width: panel-width, inset: padding, above: 0pt, below: 0pt)[#code]
      #mark(id, "end")
    ]
    #if tail > 0pt {v(tail)}
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
#let table-panel(id, rows, widths, has_header, paint: none, width: auto, offset: 0pt,
  source-widths: none, source-heights: none, font-size: none, leading: 4pt, inset: 3pt) = block(
  width: 100%, inset: (left: offset), above: 8pt, below: 12pt, breakable: true)[#layout(size => {
 let grid = [
  #set text(font: "MS PGothic", size: if font-size != none {font-size} else if widths.len() > 4 {8.5pt} else {9.5pt})
  #set par(leading: leading, spacing: 0pt)
  #let heights = if source-heights == none {auto} else {
    rows.enumerate().map(((i,row)) => {
      let height = source-heights.at(calc.min(i, source-heights.len()-1))
      for (j,c) in row.enumerate() {
        let body = if paint == none {text(c)} else {paint.at(i).at(j).body}
        let measured = measure(block(width: source-widths.at(j)-2*inset)[#flowing[#body]]).height + 2*inset
        height = calc.max(height, measured)
      }
      height
    })
  }
  #let cells = ()
  #for (i,row) in rows.enumerate() {
    let current = row.enumerate().map(((j,c)) => {
      let original = if paint == none {none} else {paint.at(i).at(j)}
      table.cell(breakable: false, fill: if original == none {none} else {rgb(original.fill)},
        align: if original == none {auto} else {original.align})[
        #if i == 0 and j == 0 and has_header {mark(id, "table-header")}
        #if original == none {text(c.replace("\n", " ").clusters().join("\u{200b}"))} else {original.body}
      ]
    })
    if i == 0 and has_header {cells.push(table.header(repeat: true, ..current))}
    else {cells += current}
  }
  #flowing[#table(columns: widths, rows: heights, inset: inset, stroke: 0.65pt + rgb("404040"), ..cells)]
 ]
 let short = measure(block(width: if width == auto {size.width} else {width}, grid)).height <= 650pt
 block(width: width, above: 0pt, below: 0pt, breakable: not short)[
   #mark(id, if short {"short-table"} else {"long-table"})
   #mark(id, "start")#grid#mark(id, "end")
 ]
})]
