#import "../player-book/template.typ": *
#let field(title,height:40pt) = block(width:100%,height:height,inset:7pt,stroke:.5pt+teal,breakable:false)[#text(size:8pt,weight:"bold",title)]
#let rows(head,widths,count,height:30pt) = {
 set text(size:9pt,hyphenate:false)
 table(columns:widths,rows:(auto,)+(height,)*count,inset:6pt,stroke:.4pt+rgb("#9ebbc0"),
 table.header(..head.map(c=>table.cell(fill:ivory,strong(c)))),..range(count*head.len()).map(i=>[]))
}
#let sheet(title,body) = {
 pagebreak(weak:true)
 set page(fill:white,margin:(left:36pt,right:36pt,top:32pt,bottom:34pt),header:none,background:none,
 footer:context grid(columns:(1fr,auto),text(size:8pt)[Sector Architect's Book · Starter Kit Review],text(size:8pt,counter(page).display())))
 set text(font:"Roboto",size:10pt,hyphenate:false)
 heading(level:1,title)
 body
}
#sheet("Sector record",[
 #field("SECTOR / SESSION / ESTABLISHED TONE")#v(8pt)
 #rows(([PLACE],[NEED / ACCESS],[PRESSURE],[ROUTES]),(1fr,1.4fr,1.4fr,1fr),5,height:50pt)
 #v(12pt)#rows(([FACTION / CONTACT],[GOAL / LEVERAGE],[LIMIT / NEXT MOVE]),(1fr,1.5fr,1.5fr),4,height:42pt)
 #v(12pt)#field("CONFIRMED FACTS / RUMOURS / OPEN ANCESTRY OR TECHNOLOGY QUESTIONS",height:95pt)
])
#sheet("Scene preparation",[
 #field("PLACE / IMMEDIATE SITUATION / WHAT THE CREW CAN PERCEIVE",height:65pt)#v(8pt)
 #grid(columns:(1fr,1fr),gutter:8pt,field("CREW OBJECTIVE / OPTIONS",height:70pt),field("OPPOSITION GOAL / LIMITS",height:70pt))#v(10pt)
 #rows(([LEAD / EVIDENCE],[ACCESS METHOD],[WHAT IT REVEALS]),(1fr,1.2fr,1.5fr),3,height:46pt)
 #v(12pt)#rows(([PRESSURE / HAZARD],[TRIGGER / INTERVAL],[CONSEQUENCE / RESPONSE]),(1fr,1.2fr,1.5fr),3,height:42pt)
 #v(12pt)#field("WAYS OUT / WHAT CHANGES IF THE CREW WAITS OR LEAVES",height:80pt)
 #v(8pt)#field("RULE OWNER / PROVISIONAL RULING TO REVIEW",height:55pt)
])
#sheet("Encounter roster",[
 #field("OBJECTIVE / INITIAL RANGE / COVER / EXITS",height:60pt)#v(10pt)
 #rows(([ACTOR / PROFILE],[HP / RESISTANCE],[ACTION / TURN USED],[GOAL / WITHDRAWAL]),(1.1fr,1fr,1.2fr,1.5fr),7,height:37pt)
 #v(12pt)#field("REINFORCEMENTS / WHEN THEY ARRIVE / WHAT THE CREW CAN KNOW",height:65pt)
 #v(10pt)#grid(columns:(1fr,1fr),gutter:8pt,field("PARTY: LEVELS / HEALING / SUPPLIES",height:65pt),field("GRIT / SCARS / LASTING EFFECTS",height:65pt))
 #v(8pt)#grid(columns:(1fr,1fr),gutter:8pt,field("SEED BUDGET / RATED TOTAL / UNRATED ACTORS",height:42pt),field("ACCESS / CONTROL / MATCHUP TO TEST",height:42pt))
 #v(8pt)#text(size:9pt)[Seed CV is provisional. Personal survival uses the full Player's Book Chapter 7.]
])
#sheet("Session and design review",[
 #field("SESSION / DATE / RULE AND PROFILE VERSIONS",height:38pt)#v(10pt)
 #rows(([OBSERVATION],[ACTUAL RESULT],[QUESTION / PROPOSED CHANGE]),(1.2fr,1.2fr,1.6fr),6,height:42pt)
 #v(12pt)#grid(columns:(1fr,1fr,1fr),gutter:8pt,field("ROUNDS / ACTIONS DENIED",height:55pt),field("GRIT SPENT / NEW WOUNDS",height:55pt),field("SUPPLIES / HP RECOVERY",height:55pt))
 #v(10pt)#field("FACTION / ROUTE / OBLIGATION CHANGES",height:75pt)
 #v(10pt)#field("PAY / EXPENSES / SALVAGE / PROMISED REWARDS",height:65pt)
 #v(10pt)#field("ESTABLISHED FACTS VERSUS UNAPPROVED MECHANICAL PROPOSALS",height:60pt)
])
