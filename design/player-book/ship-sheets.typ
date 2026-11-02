#import "template.typ": *
#let band(title, subtitle: none) = block(width:100%,fill:space,inset:(x:9pt,y:6pt),above:8pt,below:6pt)[
 #text(font:"Oswald",size:12pt,fill:white,title)
 #if subtitle != none {linebreak();text(size:8pt,fill:rgb("#b8d8e2"),subtitle)}
]
#let field(title,height:35pt) = block(width:100%,height:height,inset:6pt,stroke:.5pt+rgb("#9aaeb5"),breakable:false)[#text(size:7.5pt,weight:"bold",fill:teal,title)]
#let table-blank(head,widths,count,row-height:24pt) = {
 set text(size:8pt)
 table(columns:widths,rows:(auto,)+(row-height,)*count,inset:5pt,stroke:.4pt+rgb("#9aaeb5"),
 table.header(..head.map(c=>table.cell(fill:ivory,strong(c)))),..range(count*head.len()).map(i=>[]))
}
#let title(sub) = [
 #text(font:"Oswald",size:26pt,fill:space,weight:"bold")[GALAXIES OF LEGEND]
 #linebreak()#text(font:"Oswald",size:14pt,fill:teal,sub)
 #h(1fr)#text(size:8pt,fill:crimson)[PROPOSED / DESIGN REVIEW]
 #v(6pt)#line(length:100%,stroke:1pt+teal)
]
#let sheet(body) = {
 pagebreak(weak:true)
 set page(width:612pt,height:792pt,fill:white,margin:(left:36pt,right:36pt,top:28pt,bottom:32pt),background:none,header:none,
 footer:context grid(columns:(1fr,auto),text(size:7pt)[Ship rules review · 2026-11-02 · Untested proposals],text(size:8pt,counter(page).display())))
 set text(font:"Roboto",size:9pt,fill:ink,hyphenate:false)
 set par(leading:.25em,spacing:4pt)
 body
}
#sheet([
 #title("SHIP RECORD / construction & condition")
 #v(7pt)#grid(columns:(2fr,1fr,1fr),gutter:6pt,field("SHIP NAME / REGISTRY",height:31pt),field("FRAME CLASS",height:31pt),field("SCALE",height:31pt))
 #v(6pt)#grid(columns:(1fr,1fr,1fr,1fr),gutter:6pt,field("BUDGET: USED / TOTAL"),field("MODULES: USED / MAX"),field("DIE CEILING"),field("HANDLING"))
 #v(6pt)#grid(columns:(1fr,1fr,1fr),gutter:6pt,field("HULL: CURRENT / MAX"),field("EFFECTIVE SHIELD DR"),field("EFFECTIVE JUMP RANGE"))
 #band("MODULE ALLOCATION & CONDITION",subtitle:"Required rows are marked *. Each installed die costs d4:1 / d6:2 / d8:3 / d10:4 / d12:5. Copy for continuation.")
 #set text(size:8pt)
 #table(columns:(130pt,48pt,34pt,50pt,1fr),rows:(auto,)+(18pt,)*16,inset:4pt,stroke:.4pt+rgb("#9aaeb5"),
  table.header(..([MODULE / ID],[RATED],[COST],[CURRENT],[CAPABILITY / FAULT / TEMP]).map(c=>table.cell(fill:ivory,strong(c)))),
  ..("* Sublight engines","* Navigation","* Sensors","* Life support","* Communications","","","","","","","","","","","").map(s=>([ #s ],[],[],[],[])).flatten())
 #band("WEAPON MOUNTS",subtitle:"One shot per mount per round. Effective die sets damage; targeting may replace equipment quality.")
 #table-blank(([MOUNT / TYPE],[RANGE],[WEAK / STD / STRONG],[OPERATOR]),(1.4fr,.8fr,1.2fr,1fr),2,row-height:20pt)
 #band("CREW / STATIONS")
 #grid(columns:(1fr,1fr,1fr),gutter:6pt,field("PILOT / NAVIGATOR",height:32pt),field("GUNNERS / SENSORS",height:32pt),field("ENGINEER / COMMANDER",height:32pt))
 #v(7pt)#text(size:8pt)[Effective die = lower of installed and current. d4: one Bane · d6: neutral · d8/d10/d12: 1/2/3 Boons. One equipment grade per check; core cap still applies. Resolve action, then roll load die; only 1 degrades.]
])
#sheet([
 #title("SHIP OPERATIONS / preparation & damage control")
 #v(9pt)#grid(columns:(2fr,1fr),gutter:7pt,field("SHIP NAME"),field("DATE / SCENE"))
 #band("JUMP PLAN",subtitle:"Distance 1-5 → charge and navigation each 3 × distance. Stay within effective drive and bank limits.")
 #grid(columns:(2fr,1fr,1fr),gutter:7pt,field("DESTINATION / ROUTE"),field("DISTANCE"),field("TARGET / 3 · 6 · 9 · 12 · 15"))
 #v(7pt)#grid(columns:(1fr,1fr),gutter:7pt,
 field("CAPACITOR CLOCK: MARK FILLED / STRIKE UNUSED",height:65pt),field("NAVIGATION PROGRESS / TARGET",height:65pt))
 #v(-31pt)#pad(left:8pt)[#text(size:11pt)[□ □ □ □ □ □ □ □ □ □ □ □ □ □ □]]#v(15pt)
 #grid(columns:(1fr,1fr),gutter:7pt,field("ARRIVAL BAND: WEAK / STANDARD / STRONG"),field("RECORDED COMPLICATION / NEXT-JUMP BOON"))
 #v(6pt)#block(width:100%,fill:ivory,inset:8pt)[
 Normal charge: 1 fuel per segment; d4/d6/d8/d10/d12 takes 10/8/6/4/2 minutes. Check bank after each.
 #linebreak()Emergency charge: Main Action, Knowledge, 2 fuel per segment.
 #linebreak()Weak: automatic step-down · Standard: roll capacitors · Strong: no wear.
 #linebreak()Plot: Reason, 1 / 2 / 3 progress per 10 minutes. Use suite equipment quality; no extra computer Boon.
 #linebreak()Commit: both tracks full + capacitors and drive online → Main Action → arrive → check FTL drive. Clear both tracks. Emergency Jump Strong may include commitment.
 ]
 #band("CAPACITY & STOCK")
 #grid(columns:(1fr,1fr,1fr),gutter:6pt,field("CARGO UNITS (× SCALE)",height:28pt),field("OCCUPANTS (× SCALE)",height:28pt),field("BEDS / BERTHS / PROJECTS",height:28pt))
 #v(6pt)
 #grid(columns:(1fr,1fr,1fr),gutter:7pt,field("FUEL UNITS: CURRENT"),field("SPARE-PARTS LOTS"),field("STRUCTURAL MATERIAL LOTS"))
 #v(6pt)#table-blank(([SYSTEM / HULL],[WORK / PARTS USED],[RESTORED / EXPIRY]),(1fr,1.5fr,1fr),2,row-height:20pt)
 #band("EMERGENCIES",subtitle:"0 Hull disables engines, weapons and FTL. Declare the clock's consequence before counting.")
 #grid(columns:(1fr,1fr),gutter:7pt,field("DISABLED-SHIP CLOCK / 3 ROUNDS OR 3 × 10 MIN",height:48pt),field("AIR RESERVE / 3 × 10 MIN / SUITS",height:48pt))
 #v(6pt)#field("BREACH / FIRE / CONTAINMENT / EXPIRY / EVACUATION PLAN",height:42pt)
 #v(8pt)#text(size:8pt)[Safe service: 1 hour + 1 parts lot per restored system step, up to installed rating. Yard: 4 Hull per 8-hour shift + 1 structural lot. Repair abilities use their cards plus the proposed parts budget. Prices and cargo capacity remain open.]
])
