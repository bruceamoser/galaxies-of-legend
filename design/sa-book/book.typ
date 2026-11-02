#import "../player-book/template.typ": *
#show: setup.with(book-title:"Sector Architect's Book")
#let release = json("../../release/version.json")
#{ include "cover.typ"; pagebreak() }
#set document(title: "Galaxies of Legend — Sector Architect's Book",author:"Bruce A. Moser")
#align(center)[
 #v(30pt)#image("../player-book/art/gol-crest.png",width:115pt)
 #v(20pt)#text(font:"Oswald",size:30pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:24pt,fill:teal)[Sector Architect's Book]
 #v(16pt)#text(size:12pt)[First three-book Starter Kit · Design Review]
 #v(12pt)#text(size:11pt)[Game design by Bruce A. Moser]
]
#v(28pt)#note[A base SA book for preparing and adjudicating a lived-in frontier. Threat profiles, hazard values and encounter guidance are authoring seeds, not calibrated encounters.]
#v(12pt)#text(size:9pt)[Version #release.version · #release.date. Companion volumes: Player's Book, Starship Manual and Sector Architect's Book. Ancestries remain placeholders; new ship and SA numbers are untested proposals.]
#pagebreak()#outline(title:[Contents],depth:1)#pagebreak()
#include "generated/body.typ"
#include "sheets.typ"
#pagebreak(weak:true)
#align(center+horizon)[
 #text(font:"Oswald",size:24pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:16pt,fill:teal)[Sector Architect's Book]
 #v(10pt)#text(size:10pt)[Starter Kit v#release.version · Design Review]
]
