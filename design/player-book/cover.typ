#let gold = rgb("#0E7A85")
#let ivory = rgb("#F4F4F6")
#set document(title: "Galaxies of Legend — Player's Book cover", author: "Bruce A. Moser")
#set page(width: 612pt, height: 792pt, margin: 0pt, fill: black)
#place(top + left, image("art/gol-cover-illustration.png", width: 612pt, height: 792pt, fit: "cover"))

// Native type remains editable and sharp in the PDF.
#place(top + left, dx: 0pt, dy: 42pt, block(width: 612pt)[
  #set align(center)
  #text(font: "Oswald", size: 42pt, weight: "bold", tracking: .08em, fill: ivory)[GALAXIES]
  #v(2pt)
  #text(font: "Roboto", size: 20pt, fill: gold, style: "italic")[of]
  #v(0pt)
  #text(font: "Cinzel", size: 38pt, weight: "bold", tracking: .06em, fill: ivory)[LEGEND]
])
#place(top + left, dx: 206pt, dy: 232pt, image("art/gol-crest.png", width: 200pt))
#place(top + left, dx: 160pt, dy: 410pt, block(width: 292pt)[
  #set align(center)
  #text(font: "Oswald", size: 15pt, fill: gold, tracking: .12em)[PLAYER’S BOOK]
  #v(6pt)
  #line(length: 112pt, stroke: .6pt + gold)
  #v(6pt)
  #text(font: "Roboto", size: 11pt, fill: ivory)[Levels 1–10 · Starter Kit Review]
])
#place(bottom + center, dy: -14pt, block(fill: black.transparentize(25%), inset: (x: 12pt, y: 5pt))[
  #text(font: "Oswald", size: 9pt, fill: ivory, tracking: .12em)[BRUCE A. MOSER]
])
