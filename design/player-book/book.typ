#import "template.typ": *
#show: setup
#let release = json("../../release/version.json")

// Full-bleed cover illustration with editable native type.
#{
  set page(width: 612pt, height: 792pt, margin: 0pt, fill: black, header: none, footer: none)
  include "cover.typ"
  pagebreak()
}

#set document(title: "Galaxies of Legend — Player’s Book", author: "Bruce A. Moser")
#align(center)[
  #v(24pt)
  #image("art/gol-crest.png", width: 150pt)
  #v(14pt)
  #text(font: "Oswald", size: 34pt, weight: "bold", fill: space)[Galaxies of Legend]
  #v(10pt)
  #text(font: "Oswald", size: 18pt, fill: teal)[Player’s Book]
  #v(10pt)
  #text(size: 13pt)[Levels 1–10 · Starter Kit Review]
  #v(18pt)
  #text(font: "Oswald", size: 13pt)[Game design by Bruce A. Moser]
]
#v(22pt)
#block(width: 100%, inset: 12pt, fill: ivory)[
  This book contains character creation, advancement, abilities, equipment and the complete Legend rules for personal damage, Grit, wounds, conditions, healing and recovery.

  The *Starship Manual* contains ship construction and operation, crew stations, ship combat, FTL and ship sheets. The *Sector Architect’s Book* supports adjudication, preparation, encounters, hazards, threats and campaigns. Chapter 10 provides the companion-book reading guide.

  This is the first three-book Starter Kit review edition. The Working Ten ancestry profiles, ship construction and SA values are provisional. This edition is for reading and design review.

]
#v(14pt)
#text(size: 9pt)[Legend System rules and original game design by Bruce A. Moser. Manuscript and layout prepared with Codex under Bruce’s direction. Interior artwork generated with AI assistance.
Starter Kit v#release.version · #release.date.
Three-book Starter Kit · Design review.]
#pagebreak()
#outline(title: [Contents], depth: 1)
#pagebreak()
#include "generated/body.typ"

#pagebreak(weak: true)
#align(center + horizon)[
  #image("art/gol-crest.png", width: 76pt)
  #v(14pt)
  #text(font: "Oswald", size: 20pt, fill: space)[Galaxies of Legend]
  #v(4pt)
  #text(font: "Oswald", size: 11pt, fill: teal)[Player’s Book · Design Review]
  #v(8pt)
  #text(size: 9pt)[Version #release.version · #release.date]
  #v(2pt)
  #text(size: 9pt)[Built from the editable Markdown catalog.]
]
