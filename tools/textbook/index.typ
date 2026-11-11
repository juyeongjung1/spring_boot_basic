#let data = json("index-data.json")
#set page(width: 595.32pt, height: 841.92pt,
  margin: (left: 85.104pt, right: 83.664pt, top: 86pt, bottom: 68pt),
  header: stack(spacing: 3pt,
    align(center, text(font: "Meiryo UI", size: 9.96pt)[索引]),
    line(length: 100%, stroke: 0.48pt)),
  footer: context align(center, text(font: "Times New Roman", size: 11.04pt, counter(page).display())))
#counter(page).update(data.first_page)

#set text(font: "MS PMincho", size: 10.8pt, lang: "ja", cjk-latin-spacing: none)
#set par(leading: 3pt)
#let ink = rgb("#263a51")
#let section(label) = block(width: 100%, above: 5.3pt, below: 3pt, sticky: true,
  inset: (left: 5pt, top: 2pt, bottom: 2pt), fill: rgb("#eef2f6"),
  text(font: "Meiryo UI", weight: "bold", fill: ink, label))
#let row(entry) = block(width: 100%, above: 0pt, below: 2pt, breakable: false,
  grid(columns: (1fr, auto), align: (left + top, right + top), column-gutter: 7pt,
    entry.term,
    text(font: "Times New Roman", fill: ink,
      entry.pages.map(n => link("https://index.invalid/" + str(n), str(n))).join(", "))))

#block(below: 7pt, text(font: "Meiryo UI", weight: "bold", size: 23pt)[索引])
#block(below: 12pt)[英数字順・五十音順。ページ番号をクリックすると本文の該当ページに移動します。]
#columns(2, gutter: 23pt)[
  #for group in data.groups {
    section(group.section)
    for entry in group.entries {
      row(entry)
    }
  }
]
