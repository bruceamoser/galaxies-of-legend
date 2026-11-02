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
      grid(columns: (1fr, 1fr), text(font: "Oswald", size: 8pt, fill: forest)[Galaxies of Legend],
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
        align(right, text(font: "Oswald", size: 9pt, counter(page).display())))
    })
  set heading(numbering: none)
  show heading.where(level: 1): it => block(above: 0pt, below: 13pt)[
    #text(font: "Oswald", size: 26pt, fill: teal, weight: "bold", it.body)
    #v(7pt)#line(length:52pt,stroke:3pt+crimson)
  ]
  show heading.where(level: 2): it => block(above: 12pt, below: 6pt)[
    #text(font: "Oswald", size: 14pt, fill: teal, weight: "bold", it.body)
  ]
  show heading.where(level: 3): it => block(above: 9pt, below: 4pt)[
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
  block(below: 8pt)[#text(font: "Oswald", size: 9pt, fill: crimson)[CHAPTER #n]]
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
#let tail-art(asset) = block(height: 1fr, layout(size => {
  if size.height >= 110pt { align(center+horizon, illustration(asset, height: calc.min(size.height - 12pt, 340pt))) }
}))
#let rule-table(cols, head, rows, widths: auto, pad: 5pt, font-size: 9.3pt) = {
  set text(size: font-size)
  set par(leading: 0.28em, spacing: 3pt)
  let whole = table(columns: if widths == auto { cols } else { widths }, inset: (x: 5pt, y: pad),
    stroke: .3pt + rgb("#b5cdd0"),
    fill: (x,y) => if y == 0 { forest } else if calc.odd(y) { rgb("#e7eef0") } else { paper },
    table.header(repeat: true, ..head.map(c => text(fill: ivory, weight: "bold", c))),
    ..rows.flatten())
  layout(size => {
    let h = measure(block(width:size.width,whole)).height
    // Keep a short reference together. Long references retain repeated headers.
    block(breakable:h > 620pt)[#whole]
  })
}

#let signature-menu(body) = block(width:100%,stroke:.5pt+teal,inset:7pt,breakable:false)[
  #set text(size:9pt)
  #set par(leading:.2em,spacing:3pt)
  #set list(spacing:1pt)
  #show heading.where(level:2): it => block(above:0pt,below:4pt,text(size:10pt,weight:"bold",fill:forest,it.body))
  #body
]
#let cost-matrix(head,rows) = {
  assert(rows.all(row => row.len() == head.len()), message:"Class-cost matrix row/header mismatch")
  set text(size:10pt,hyphenate:false)
  set par(leading:.45em)
  table(columns:(112pt,)+(1fr,)*(head.len()-1),inset:(x:6pt,y:7pt),align:(x,y)=>if x==0 {left} else {center},
    stroke:.4pt+rgb("#b5cdd0"),fill:(x,y)=>if y==0 {forest} else if calc.odd(y) {ivory} else {paper},
    table.header(..head.map(c=>text(fill:ivory,weight:"bold",c))), ..rows.flatten())
}
#let ability-directory(rows) = {
  set text(size:9pt,hyphenate:false)
  set par(leading:.25em,spacing:3pt)
  table(columns:(125pt,105pt,77pt,1fr),inset:(x:5pt,y:3.5pt),stroke:.3pt+rgb("#b5cdd0"),
    fill:(x,y)=>if y==0 {forest} else if calc.odd(y) {ivory} else {paper},
    table.header(repeat:true,..([Ability],[Requirements],[Action],[What it does]).map(c=>text(fill:ivory,weight:"bold",c))),
    ..rows.flatten())
}
#let diamond(tier) = box(width: 23pt, height: 23pt)[
  #place(center + horizon, rotate(45deg, square(size: 17pt, fill: forest, stroke: .7pt + teal)))
  #place(center + horizon, text(size: 9pt, fill: ivory, weight: "bold", tier))
]
#let discipline-mark(name, rank, size: 29pt) = box(width: size + 2pt, height: size)[
  #place(center+horizon, circle(radius: size/2 - 1pt, fill: rgb("#0e7a85").transparentize(82%), stroke: .6pt + teal))
  #place(center+horizon, text(size: size*0.32, weight: "bold", fill: white, upper(name.slice(0, 1))))
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
#let outcome-rows(rows) = {
  for row in rows {
    block(width:100%,fill:rgb("#eef4f6"),inset:(x:7pt,y:6pt),above:4pt,below:4pt,breakable:false)[#row]
  }
}
#let card(title, tier, req, action, attr, tags, price, key, body, icons: []) = {
  let whole = block(width:100%,stroke:.7pt+teal,radius:0pt,clip:true,fill:rgb("#ffffff"),above:9pt,below:9pt)[
    #card-heading(title,key,tier:tier,icons:icons)
    #block(inset:(x:10pt,y:9pt))[
      #set text(size:10.5pt,hyphenate:false)
      #set par(leading:.46em,spacing:.7em)
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
