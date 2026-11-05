#let forest = rgb("#0A0A0C")
#let space = forest
#let teal = rgb("#176f8c")
#let gold = rgb("#d4af37")
#let ivory = rgb("#eaf3f4")
#let paper = rgb("#ffffff")
#let ink = rgb("#0A0A0C")
#let crimson = rgb("#D92027")
#let chapter-name = state("chapter-name", "Player’s Book")
#let setup(book-title: "Player’s Book", body) = {
  set document(title: "Galaxies of Legend — " + book-title, author: "Bruce A. Moser")
  set text(font: "Roboto", size: 10.5pt, fill: ink, lang: "en", hyphenate: true)
  set par(leading: 0.42em, spacing: 0.65em, justify: false)
  set page(width: 612pt, height: 792pt, margin: (left: 42pt, right: 42pt, top: 52pt, bottom: 46pt), fill: paper,
    background: none,
    header: context {
      grid(columns: (1fr, 1fr), text(font: "Oswald", size: 8.5pt, fill: teal, tracking: .65pt)[GALAXIES OF LEGEND],
        align(right, text(size: 8pt, fill: forest, {
          let hs = query(heading.where(level: 1)).filter(h => h.location().page() <= here().page())
          if hs.len() > 0 { hs.last().body } else { book-title }
        })))
      v(5pt); line(length:100%,stroke:.45pt+rgb("#8baab8"))
    },
    footer: context {
      line(length:100%,stroke:.45pt+rgb("#8baab8"))
      v(3pt)
      grid(columns: (1fr, 1fr), text(size: 8pt)[#book-title · Starter Kit Review],
        align(right, box(fill: teal, inset: (x: 6pt, y: 1pt), text(font: "Oswald", size: 9pt, fill: white, counter(page).display()))))
    })
  set heading(numbering: none)
  show heading.where(level: 1): it => block(above: 0pt, below: 13pt)[
    #text(font: "Oswald", size: 26pt, fill: teal, weight: "bold", it.body)
    #v(7pt)#line(length:52pt,stroke:3pt+crimson)
  ]
  show heading.where(level: 2): it => block(above: 12pt, below: 6pt, sticky: true)[
    #text(font: "Oswald", size: 14pt, fill: teal, weight: "bold", it.body)
  ]
  show heading.where(level: 3): it => block(above: 9pt, below: 4pt, sticky: true)[
    #text(size: 11.5pt, fill: forest, weight: "bold", it.body)
  ]
  show link: set text(fill: rgb("#0e7a85"))
  set list(indent: 10pt, body-indent: 5pt, spacing: 4pt)
  set enum(indent: 11pt, body-indent: 5pt, spacing: 4pt)
  body
}
#let chapter(n, title) = {
  pagebreak(weak: true)
  chapter-name.update(title)
  block(below: 8pt)[#text(font: "Oswald", size: 9pt, fill: crimson)[#(if n == "A" { "APPENDIX" } else { "CHAPTER" }) #n]]
  heading(level: 1, title)
}
#let entry(title, key) = {
  [#heading(level: 2, title)#label(key)]
}
#let xref(key, body) = link(label(key), body)
#let pageref(key) = context link(label(key), str(counter(page).at(label(key)).first()))
#let twocol(body) = columns(2, gutter: 18pt, body)
#let note(body) = block(width: 100%, inset: 9pt, fill: ivory, stroke: (left: 2pt + gold), radius: 2pt, above: 6pt, below: 8pt, breakable: true)[
  #set text(size: 10pt)
  #body
]
#let art-files = json("generated/art-files.json")
#let illustration(asset, width: 100%, height: 160pt, fit: "contain") = block(width: width, height: if asset in art-files {height} else {0pt}, above: if asset in art-files {8pt} else {0pt}, below: if asset in art-files {14pt} else {0pt})[
  #layout(size => context { let pos=here().position(); [#metadata((asset:asset,page:pos.page,x:pos.x/1pt,y:pos.y/1pt,width:size.width/1pt,height:height/1pt)) <art-placement>] })
  #if asset in art-files {
    image("art/interior/" + asset + ".png", width: 100%, height: height, fit: fit, alt: asset.replace("-", " "))
  } else {
    none
  }
]
// A fractional block gives the remaining page height without making a new page.
#let tail-art(asset, limit: 340pt) = if asset in art-files {
  block(height: 1fr, layout(size => {
    if size.height >= 120pt {
      align(center+horizon, illustration(asset, height: calc.min(size.height - 26pt, limit), fit: "cover"))
    }
  }))
}
#let rule-table(cols, head, rows, widths: auto, pad: 5pt, font-size: 9.3pt, numeric: ()) = {
  set text(size: font-size)
  set par(leading: 0.28em, spacing: 3pt)
  set table.cell(breakable: false)
  let whole = table(columns: if widths == auto { cols } else { widths }, inset: (x: 6pt, y: pad),
    align: (x, y) => if x in numeric {right + top} else {left + top},
    stroke: (top: none, left: none, right: none, bottom: .4pt + rgb("#b5cdd0")),
    fill: (x,y) => if y == 0 { forest } else if calc.odd(y) { rgb("#e7eef0") } else { paper },
    table.header(repeat: true, ..head.map(c => text(fill: ivory, weight: "bold", c))),
    ..rows.flatten())
  layout(size => {
    let h = measure(block(width:size.width,whole)).height
    // Keep a short reference together. Long references retain repeated headers.
    block(breakable:h > 620pt)[#whole]
  })
}

#let cost-matrix(head,rows) = {
  assert(rows.all(row => row.len() == head.len()), message:"Class-cost matrix row/header mismatch")
  set text(size:10pt,hyphenate:false)
  set par(leading:.45em)
  table(columns:(112pt,)+(1fr,)*(head.len()-1),inset:(x:6pt,y:7pt),align:(x,y)=>if x==0 {left} else {center},
    stroke:.4pt+rgb("#b5cdd0"),fill:(x,y)=>if y==0 {forest} else if calc.odd(y) {ivory} else {paper},
    table.header(..head.map(c=>text(fill:ivory,weight:"bold",c))), ..rows.flatten())
}
#let action-code(action) = (("Main Action": "A", "Maneuver": "M", "Reaction": "R", "Passive": "P").at(action, default: "—"))
#let action-mark(action) = box(inset:(x:4pt,y:2pt),radius:2pt,fill:ivory)[#text(size:8pt,weight:"bold",fill:forest,action-code(action))]
#let ability-directory(rows) = {
  set text(size:9pt,hyphenate:false)
  set par(leading:.25em,spacing:3pt)
  table(columns:(110pt,120pt,76pt,1fr),inset:(x:5pt,y:3.5pt),stroke:.3pt+rgb("#b5cdd0"),
    fill:(x,y)=>if y==0 {forest} else if calc.odd(y) {ivory} else {paper},
    table.header(repeat:true,..([Ability],[Requirements],[Action],[Target / range]).map(c=>text(fill:ivory,weight:"bold",c))),
    ..rows.flatten())
}
#let diamond(tier) = box(width: 23pt, height: 23pt)[
  #place(center + horizon, rotate(45deg, square(size: 17pt, fill: forest, stroke: .7pt + teal)))
  #place(center + horizon, text(size: 9pt, fill: ivory, weight: "bold", tier))
]
#let discipline-mark(name, rank, size: 29pt) = box(width: size + 2pt, height: size)[
  #place(center+horizon, circle(radius: size/2 - 1pt, fill: rgb("#0e7a85").transparentize(82%), stroke: .6pt + teal))
  #place(center+horizon, image("art/disciplines/" + name + ".svg", width:size*0.68))
  #if rank != "" {
    place(right+bottom, rect(width:12pt,height:13pt,radius:2pt,fill:ivory,stroke:.5pt+forest,
      align(center+horizon,text(size:11pt,weight:"bold",fill:forest,rank))))
  }
]

#let card-heading(title, key, tier: none, icons: [], title-size: 13pt) = block(width:100%,fill:forest,inset:7pt)[
  #set text(fill:ivory)
  #show heading.where(level:3): it => block(above:0pt,below:0pt,text(size:title-size,weight:"bold",fill:ivory,it.body))
  #grid(columns: if tier == none {(1fr,auto)} else {(24pt,1fr,auto)},gutter:6pt,
    ..if tier == none {()} else {(diamond(tier),)},
    [#heading(level:3,outlined:true,title)#label(key)],
    box(icons))
]
#let outcome-rows(rows, compact: false) = {
  for row in rows {
    block(width:100%,fill:rgb("#eef4f6"),inset:(x:7pt,y:if compact {3pt} else {6pt}),above:if compact {2pt} else {4pt},below:if compact {2pt} else {4pt},breakable:false)[#row]
  }
}
#let card(title, tier, req, action, attr, tags, price, key, body, icons: [], compact: false) = {
  let whole = block(width:100%,stroke:.7pt+teal,radius:0pt,clip:true,fill:rgb("#ffffff"),above:9pt,below:9pt)[
    #card-heading(title,key,tier:tier,icons:[#action-mark(action)#icons],title-size:if compact {11pt} else {13pt})
    #block(inset:(x:if compact {8pt} else {10pt},y:if compact {6pt} else {9pt}))[
      #set text(size:if compact {10pt} else {10.5pt},hyphenate:false)
      #set par(leading:if compact {.32em} else {.46em},spacing:if compact {.45em} else {.7em})
      #set list(indent:10pt,body-indent:4pt,spacing:5pt)
      #text(size:10pt,weight:"bold")[#action · #attr]
      #h(1fr)#text(size:9pt,price)
      #v(4pt)#text(size:9pt)[#req]
      #v(6pt)#line(length:100%,stroke:.4pt+teal)#v(6pt)
      #body
    ]
  ]
  layout(size => {
    let height = measure(block(width: size.width, whole)).height
    [#metadata((key: key, height: height / 1pt)) <card-size>]
    block(breakable: height > 675pt, whole)
  })
}
#let catalog-card(title,key,body,icons:[]) = block(width:100%,stroke:.7pt+teal,radius:0pt,clip:true,fill:rgb("#ffffff"),above:9pt,below:9pt,breakable:false)[
  #card-heading(title,key,icons:icons)
  #block(inset:7pt)[
    #set text(size:10.5pt,hyphenate:false)
    #set par(leading:.46em,spacing:.7em)
    #set list(indent:10pt,body-indent:4pt,spacing:5pt)
    #body
  ]
]
#let companion-card(title,key,asset,intro,body) = block(width:100%,stroke:.8pt+teal,radius:0pt,clip:true,fill:rgb("#ffffff"),breakable:false,above:6pt,below:8pt)[
  #card-heading(title,key,title-size:16pt)
  #block(inset:9pt)[
    #set text(size:9.5pt)
    #set par(leading:.3em,spacing:.45em)
    #grid(columns:(1.5fr,1fr),gutter:12pt,[#intro],[#illustration(asset,height:165pt)])
    #v(5pt)#line(length:100%,stroke:.5pt+teal)#v(3pt)
    #body
  ]
]
#let form-field(title, height: 30pt) = block(width: 100%, height: height, stroke: .5pt + teal, inset: 5pt)[#text(size: 8pt, weight: "bold", title)]
#let sheet-page(title, body) = {
  pagebreak(weak: true)
  set page(fill: white)
  heading(level: 2, title)
  body
  pagebreak()
}

#let form-table(cols, head, rows) = {
  set text(size: 8pt)
  table(columns: (1fr,) * cols, rows: (auto,) + (17pt,) * rows.len(), inset: 4pt,
    stroke: .4pt + rgb("#9ebbc0"), fill: (x,y) => if y == 0 { ivory } else { white },
    table.header(..head.map(c => strong(c))), ..rows.flatten())
}

#let class-panel(title,key,body) = block(width:100%,stroke:.7pt+teal,radius:0pt,clip:true,breakable:false)[
  #card-heading(title,key,title-size:18pt)
  #block(inset:10pt)[
    #set text(size:9.5pt)
    #set par(leading:.28em,spacing:.5em)
    #show heading.where(level:2): it => block(above:7pt,below:4pt,text(size:11pt,weight:"bold",it.body))
    #body
  ]
]

// Native columns use actual layout widths; whole cards move to the next column/page.
#let reading-columns(items,gap:8pt) = columns(2,gutter:20pt)[
  #for item in items { item; v(gap) }
]

// The wound reference needs real reading columns and a repeated family/band caption.
#let wound-table(caption,head,rows) = {
  set text(size:10pt,hyphenate:false)
  set par(leading:.4em,spacing:4pt)
  set table.cell(breakable:false)
  table(columns:(32pt,128pt,152pt,186pt,30pt),inset:(x:5pt,y:5pt),stroke:.35pt+rgb("#b5cdd0"),
    fill:(x,y)=>if y < 2 {forest} else if calc.odd(y) {ivory} else {paper},
    table.header(repeat:true,
      table.cell(colspan:5,fill:teal,text(font:"Oswald",size:12pt,fill:white,caption)),
      ..head.map(c=>text(fill:white,weight:"bold",c))), ..rows.flatten())
}

// Ancestry profiles reserve space for a scene portrait and keep the trait menu together.
#let ancestry-profile(title, key, asset, traits, intro) = {
  pagebreak(weak: true)
  block(width: 100%, fill: space, inset: 12pt)[
    #text(font: "Oswald", size: 9pt, fill: rgb("#77c4d8"))[LINEAGE PROFILE]
    #linebreak()
    #text(font: "Oswald", size: 29pt, weight: "bold", fill: white, title)#label(key)
  ]
  v(8pt)
  block(width: 100%, fill: ivory, inset: 10pt)[#intro]
  v(6pt)
  grid(columns: (1fr, 1.2fr), gutter: 18pt,
    [#illustration(asset, height: 420pt)],
    [
      #text(weight: "bold")[Choose two of five.] Use each trait’s stated action and limits.
      #v(8pt)
      #for t in traits {
        block(width: 100%, breakable: false, below: 6pt,
          stroke: .5pt + rgb("#a9c4cb"), [
            #block(width: 100%, fill: teal, inset: (x: 8pt, y: 4pt), below: 0pt)[
              #text(fill: white, weight: "bold", size: 10pt, t.at(0))
            ]
            #block(width: 100%, inset: 7pt)[#t.at(1)]
          ])
      }
    ])
}

#let ancestry-society(title, asset, origins, society, paths, example) = {
  pagebreak(weak: true)
  heading(level: 2, title + " communities")
  grid(columns: (1fr, 1fr), gutter: 20pt,
    [#origins],
    [#society])
  v(7pt)
  grid(columns: (1fr, 1fr), gutter: 20pt,
    [#note[#strong[Common paths] #parbreak() #paths]],
    [#note[#strong[At the table] #parbreak() #example]])
  tail-art(asset, limit: 235pt)
}

#let ancestry-lineup(people) = {
  pagebreak(weak: true)
  heading(level: 2)[Ten lineages, side by side]
  [These ten individuals show the range of bodies a crew might bring aboard. Both rows use the same scale. Individual size and appearance vary. Select a name to read its profile.]
  let metrics = json("art/lineage-cutout-metrics.json")
  let rows = (people.slice(0, 5), people.slice(5))
  let figure-width(p) = {
    let asset = p.at(2)
    if asset in metrics {
      let (_, _, x0, y0, x1, y1) = metrics.at(asset)
      calc.max(58pt, p.at(3) * 96pt * (x1 - x0) / (y1 - y0) + 4pt)
    } else { 58pt }
  }
  layout(size => {
    let largest-row = calc.max(..rows.map(row => row.map(figure-width).sum()))
    let factor = calc.min(1, (size.width - 28pt) / largest-row)
    let person(p) = {
      let (title, key, asset, stature) = p
      block(width: 100%, height: 211pt * factor, {
        if asset in metrics {
          let (w, h, x0, y0, x1, y1) = metrics.at(asset)
          let scale = stature * 96pt * factor / (y1 - y0)
          place(center + bottom,
            dx: (w - x0 - x1) * scale / 2,
            dy: (h - y1) * scale,
            image("art/interior/" + asset + ".png", height: h * scale, alt: title))
        }
      })
      line(length: 100%, stroke: .55pt + teal)
      align(center)[
        #xref(key, text(font: "Oswald", size: 11pt, title))
        #linebreak()
        #text(size: 8pt, str(stature) + " m")
      ]
    }
    v(8pt)
    for row in rows {
      align(center, grid(columns: row.map(p => figure-width(p) * factor), gutter: 7pt, ..row.map(person)))
      v(9pt)
    }
    text(size: 8.5pt, fill: teal)[Height is measured from the deck to the top of the standing figure.]
  })
}


// Keep cards in aligned pairs so the next row starts together.
#let ability-pages(cards) = grid(columns: (1fr, 1fr), column-gutter: 18pt, row-gutter: 3pt, ..cards)
