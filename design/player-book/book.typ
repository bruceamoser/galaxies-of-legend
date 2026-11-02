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
  #text(size: 13pt)[Levels 1–10 · Design Review]
  #v(18pt)
  #text(font: "Oswald", size: 13pt)[Game design by Bruce A. Moser]
]
#v(22pt)
#block(width: 100%, inset: 12pt, fill: ivory)[
  This book contains the player rules and the initial character catalog for
  *Galaxies of Legend*: character creation, advancement, abilities, equipment,
  harm and recovery, starships, and FTL travel.

  This is a reading and visual design review, dated 2 November 2026. The ship chapter expands the proposed mechanics with examples and a two-page ship record. The expanded roster, class affinities and ship construction rules are untested proposals. Ancestries remain placeholders awaiting Bruce's material. Structural checks do not certify balance or readiness for table playtesting. Interior artwork remains in development.
]
#v(14pt)
#text(size: 9pt)[Manuscript and layout prepared with Codex under Bruce’s direction.
Starter Kit v#release.version · #release.date.
Ship systems review · 2026-11-02.]
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
