# Raster ship-sheet art

Generated with the built-in image-generation tool. These painted hulls replace the visual direction of the rejected vector-sheet prototype. Blank panels represent module positions; required equipment must still be purchased with SP. Ship geometry adds no new rules.

`light-cutter-spatial-v2.png`: Light Cutter, twelve blank system panels.

`medium-frigate-spatial-v2.png`: Medium Frigate, sixteen blank system panels.

Generation prompts are recorded in `prompts.json`.

Launch (8 panels), Heavy (22) and Capital (30) complete the family. `panels.json` records typesetting bounds in original PNG pixels; the builder does not edit the image pixels. `build-sheets.py` generates six interactive pages with 394 checked field values and widget appearances, using existing construction data and the Scout example. The publisher inserts these pages before the manual's back cover. Heavy/Capital use 17-by-11-inch pages; other hulls use US Letter portrait. SP arithmetic is manual.
