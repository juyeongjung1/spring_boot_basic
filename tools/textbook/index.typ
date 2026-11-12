// 見本の索引に合わせたページ家具、二段組みと24ptの行送り。
#let data = json("index-data.json")
#let at(x, y, body) = place(top + left, dx: x * 1pt, dy: y * 1pt, body)

#set text(font: ("Times New Roman", "MS PMincho"), size: 10.98pt, lang: "ja",
  top-edge: 0pt, bottom-edge: 0pt, cjk-latin-spacing: none, kerning: false, overhang: false)
#set par(leading: 0pt, spacing: 0pt)

#set page(width: 595.32pt, height: 841.92pt,
  margin: (left: 85.08pt, right: 85.92pt, top: 86.04pt, bottom: 47.8pt),
  background: context [
    #at(287.64, 52.68, text(font: "MS PGothic", size: 10.02pt)[索引])
    #at(83.58, 56.52, rect(width: 428.22pt, height: 0.48pt, fill: black, stroke: none))
    #place(top + center, dy: 797.16pt, text(size: 9pt, str(data.first_page + here().page() - 1)))
  ])

#let title_char(value) = text(font: "MS PGothic", size: 24pt, stroke: 0.69pt, value)
#block(width: 100%, height: 72pt, above: 0pt, below: 0pt, breakable: false)[
  #at(168.48, 37.68, title_char("索"))
  #at(212.58, 37.68, title_char("引"))
]

#let section(label) = {
  v(6pt, weak: true)
  block(width: 100%, height: 24pt, above: 0pt, below: 0pt, sticky: true, breakable: false,
    inset: (top: 12pt), text(font: "MS PGothic", stroke: 0.31pt, label))
}

#let row(entry) = {
  let numbers = entry.pages.map(n => link("https://index.invalid/" + str(n), str(n))).join(", ")
  block(width: 100%, height: 24pt, above: 0pt, below: 0pt, breakable: false,
    inset: (top: 12pt), grid(columns: (auto, 1fr, auto), column-gutter: 0.8pt,
      entry.term, repeat(gap: 0pt, justify: false)[.], numbers))
}

#columns(2, gutter: 36.84pt)[
  #for group in data.groups {
    section(group.section)
    for entry in group.entries {
      row(entry)
    }
  }
]
