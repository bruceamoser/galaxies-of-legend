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
  #text(font: "Cinzel", size: 34pt, weight: "bold", fill: space)[Galaxies of Legend]
  #v(10pt)
  #text(font: "Cinzel", size: 18pt, fill: teal)[Player’s Book]
  #v(10pt)
  #text(size: 13pt)[Levels 1–10 · Playtest Edition]
  #v(18pt)
  #text(font: "Cinzel", size: 13pt)[Game design by Bruce A. Moser]
]
#v(22pt)
#block(width: 100%, inset: 12pt, fill: ivory)[
  This book contains the player rules and the initial character catalog for
  *Galaxies of Legend*: character creation, advancement, abilities, equipment,
  harm and recovery, starships, and FTL travel.

  This is a digital playtest edition built from editable Markdown. The cover and
  crest are original assets. Interior art is a placeholder in this first edition.
  Structural checks do not certify balance.
]
#v(14pt)
#text(size: 9pt)[Manuscript and layout prepared with Codex under Bruce’s direction.
Starter Kit v#release.version · #release.date.
Initial playtest data set.]
#pagebreak()
#outline(title: [Contents], depth: 1)
#pagebreak()
#include "generated/body.typ"

#pagebreak(weak: false)
#align(center + horizon)[
  #image("art/gol-crest.png", width: 76pt)
  #v(14pt)
  #text(font: "Cinzel", size: 20pt, fill: space)[Galaxies of Legend]
  #v(4pt)
  #text(font: "Cinzel", size: 11pt, fill: teal)[Player’s Book · Playtest Edition]
  #v(8pt)
  #text(size: 9pt)[Version #release.version · #release.date]
  #v(2pt)
  #text(size: 9pt)[Built from the editable Markdown catalog.]
]
