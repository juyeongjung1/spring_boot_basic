// 固定配置版と自動改ページ版で共有する本文の書式。
#let red = rgb("FF0000")
#let body-style(body) = {
  set text(font: "MS PMincho", size: 11.04pt, lang: "ja", cjk-latin-spacing: none, kerning: false, overhang: false, top-edge: 0pt, bottom-edge: 0pt)
  set par(leading: 18pt, spacing: 6pt, justify: false)
  show strong: it => text(font: "MS PGothic", stroke: 0.22pt, it.body)
  body
}
#let checkpoint(id, edge) = context {
  [#metadata((id: id, edge: edge, page: here().page(), y: here().position().y / 1pt)) <checkpoint>]
}
#let fit-line(body) = layout(size => {
  let width = measure(body).width
  if width > size.width {
    scale(x: size.width / width * 100%, y: 100%, reflow: true, origin: top + left, box(body))
  } else { box(body) }
})
#let flow-heading(id, body) = block(sticky: true, above: 24pt, below: 12pt)[
  #checkpoint(id, "heading")
  #text(font: "MS PGothic", stroke: 0.22pt, body)
]
#let flow-paragraph(id, body) = block(above: 0pt, below: 6pt)[
  #checkpoint(id, "start")
  #h(11.04pt)#body#checkpoint(id, "end")
]
#let flow-question(id, title, items) = block(breakable: false, above: 24pt, below: 12pt)[
  #checkpoint(id, "start")
  #text(font: "MS PGothic", stroke: 0.22pt, title)
  #v(12pt)
  #for item in items [
    #block(above: 0pt, below: 12pt)[#h(5pt)●#h(12pt)#item]
  ]
  #checkpoint(id, "end")
]
