#import "../player-book/template.typ": *
#show: setup.with(book-title:"Starship Manual")
#let release = json("../../release/version.json")
#{ include "cover.typ"; pagebreak() }
#set document(title: "Galaxies of Legend — Starship Manual",author:"Bruce A. Moser")
#align(center)[
 #v(30pt)#image("../player-book/art/gol-crest.png",width:115pt)
 #v(20pt)#text(font:"Oswald",size:30pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:24pt,fill:teal)[Starship Manual]
 #v(16pt)#text(size:12pt)[First three-book Starter Kit · Design Review]
 #v(12pt)#text(size:11pt)[Game design by Bruce A. Moser]
]
#v(28pt)#note[Ship rules and records live in this volume. The complete personal Legend foundation and learned character abilities remain in the Player's Book.]
#v(12pt)#text(size:9pt)[Version #release.version · #release.date. Companion volumes: Player's Book, Starship Manual and Sector Architect's Book. Ancestries remain placeholders; new ship and SA numbers are untested proposals.]
#v(10pt)#text(size:8.5pt)[Manuscript and layout prepared with Codex under Bruce's direction. Existing generated review illustrations are reused; font licenses and artwork notes are included in the source archive.]
#pagebreak()#outline(title:[Contents],depth:1)#pagebreak()
#include "generated/body.typ"
#include "ship-sheets.typ"
#pagebreak(weak:true)
#align(center+horizon)[
 #text(font:"Oswald",size:24pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:16pt,fill:teal)[Starship Manual]
 #v(10pt)#text(size:10pt)[Starter Kit v#release.version · Design Review]
]
