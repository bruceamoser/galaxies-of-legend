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
 set text(font:"Roboto",size:9pt,fill:ink)
 set par(leading:.25em,spacing:4pt)
 body
}
#sheet([
 #title("SHIP RECORD / condition & crew")
 #v(9pt)#grid(columns:(2fr,1fr),gutter:7pt,field("SHIP NAME / REGISTRY"),field("PROFILE / OWNER"))
 #v(7pt)#grid(columns:(1fr,1fr,1fr,1fr),gutter:7pt,field("HULL: CURRENT / MAX",height:44pt),field("SHIELD DR: ONLINE / OFF",height:44pt),field("HANDLING",height:44pt),field("JUMP RATING",height:44pt))
 #band("SYSTEM CONDITION",subtitle:"Mark current die; write installed rating. Offline is below d4. Temporary adjustments never erase wear.")
 #set text(size:8pt)
 #table(columns:(105pt,50pt,1fr,130pt),inset:(x:5pt,y:6pt),stroke:.4pt+rgb("#9aaeb5"),
  table.header(..([SYSTEM],[RATED],[CURRENT: CIRCLE ONE],[TEMPORARY / FAULT / REPAIR]).map(c=>table.cell(fill:ivory,strong(c)))),
  ..("Capacitors","FTL drive","Navigation","Sensors","Sublight engines","Weapons","Defences","Life support","Communications").map(s=>([ #s ],[],[d12 | d10 | d8 | d6 | d4 | OFF],[])).flatten())
 #band("WEAPON MOUNTS",subtitle:"One shot per mount per round. Printed damage is ship scale; die size is endurance.")
 #table-blank(([MOUNT / TYPE],[RANGE],[WEAK / STD / STRONG],[FIRED THIS ROUND]),(1.6fr,.8fr,1.1fr,1fr),2,row-height:25pt)
 #band("CREW STATIONS")
 #table-blank(([PILOT],[GUNNER],[ENGINEER]),(1fr,1fr,1fr),1,row-height:24pt)
 #v(5pt)#table-blank(([NAVIGATOR],[SENSORS],[COMMANDER]),(1fr,1fr,1fr),1,row-height:24pt)
 #v(9pt)#block(width:100%,fill:ivory,inset:8pt)[
 #strong[Resolve action → roll load die → on 1, step down.]
 #linebreak()Incoming attack: resistance → shield DR → Hull → defences load → wound if Hull lost.
 #linebreak()Wound d6: 1–2 Hull only · 3 sensors · 4 engines · 5 weapons · 6 capacitors or life support.
 ]
])
#sheet([
 #title("SHIP OPERATIONS / preparation & damage control")
 #v(9pt)#grid(columns:(2fr,1fr),gutter:7pt,field("SHIP NAME"),field("DATE / SCENE"))
 #band("JUMP PLAN",subtitle:"Distance 1 / 2 / 3 → charge 3 / 6 / 9 and navigation 3 / 6 / 9. Stay within Jump rating.")
 #grid(columns:(2fr,1fr,1fr),gutter:7pt,field("DESTINATION / ROUTE"),field("DISTANCE"),field("TARGET / 3 · 6 · 9"))
 #v(7pt)#grid(columns:(1fr,1fr),gutter:7pt,
 field("CAPACITOR CLOCK: MARK FILLED / STRIKE UNUSED",height:65pt),field("NAVIGATION PROGRESS / TARGET",height:65pt))
 #v(-31pt)#pad(left:8pt)[#text(size:15pt)[□ □ □ □ □ □ □ □ □]]#v(15pt)
 #grid(columns:(1fr,1fr),gutter:7pt,field("ARRIVAL BAND: WEAK / STANDARD / STRONG"),field("RECORDED COMPLICATION / NEXT-JUMP BOON"))
 #v(6pt)#block(width:100%,fill:ivory,inset:8pt)[
 Normal charge: 1 fuel + 10 minutes per segment; check capacitors after each.
 #linebreak()Emergency charge: Main Action, Knowledge, 2 fuel per segment.
 #linebreak()Weak: automatic step-down · Standard: roll capacitors · Strong: no wear.
 #linebreak()Plot: Reason, 1 / 2 / 3 progress per 10 minutes. Online suite grants a Boon.
 #linebreak()Commit: both tracks full + capacitors and drive online → Main Action → arrive → check FTL drive. Clear both tracks. Emergency Jump Strong may include commitment.
 ]
 #band("STOCK & SERVICE")
 #grid(columns:(1fr,1fr,1fr),gutter:7pt,field("FUEL UNITS: CURRENT"),field("SPARE-PARTS LOTS"),field("STRUCTURAL MATERIAL LOTS"))
 #v(6pt)#table-blank(([SYSTEM / HULL],[WORK / PARTS USED],[RESTORED / EXPIRY]),(1fr,1.5fr,1fr),3,row-height:22pt)
 #band("EMERGENCIES",subtitle:"0 Hull disables engines, weapons and FTL. Declare the clock's consequence before counting.")
 #grid(columns:(1fr,1fr),gutter:7pt,field("DISABLED-SHIP CLOCK / 3 ROUNDS OR 3 × 10 MIN",height:48pt),field("AIR RESERVE / 3 × 10 MIN / SUITS",height:48pt))
 #v(6pt)#field("BREACH / FIRE / CONTAINMENT / EXPIRY / EVACUATION PLAN",height:42pt)
 #v(8pt)#text(size:8pt)[Safe service: 1 hour + 1 parts lot per restored system step, up to installed rating. Yard: 4 Hull per 8-hour shift + 1 structural lot. Repair abilities use their cards plus the proposed parts budget. Prices and cargo capacity remain open.]
])
