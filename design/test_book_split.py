"""Protect the three-volume ownership boundary and base SA profile schema."""
import re,unittest
from pathlib import Path
D=Path(__file__).parent
class BookSplitTests(unittest.TestCase):
    def test_player_only_has_ship_orientation(self):
        build=(D/'player-book/build.py').read_text()
        self.assertIn('11-starship-reference.md',build)
        self.assertNotIn('11-starships.md',build)
        self.assertNotIn('ship-sheets.typ',build)
        self.assertFalse((D/'player-book/manuscript/11-starships.md').exists())
        self.assertFalse((D/'player-book/ship-sheets.typ').exists())
    def test_canonical_ship_source_and_records_moved_together(self):
        source=(D/'starship-manual/manuscript/02-rules.md').read_text()
        sections=re.findall(r'^## (\d+)\.',source,re.M)
        self.assertEqual(sections,[str(i) for i in range(1,13)])
        self.assertTrue((D/'starship-manual/ship-sheets.typ').exists())
        for name in ['Scout Cutter','Free Trader','System Shuttle']:self.assertIn(name,source)
    def test_player_still_builds_full_harm_reference(self):
        text=(D/'player-book/build.py').read_text()
        self.assertIn('wound_reference()',text)
        self.assertIn('08-recovery.md',text)
        self.assertIn('rules/healing.md',text)
    def test_sa_has_nine_authored_chapters_and_four_worksheets(self):
        self.assertEqual(len(list((D/'sa-book/manuscript').glob('*.md'))),9)
        sheets=(D/'sa-book/sheets.typ').read_text()
        for title in ['Sector record','Scene preparation','Encounter roster','Session and design review']:self.assertIn(title,sheets)
    def test_adversary_catalog_is_complete_and_explicitly_unrated(self):
        profiles=list((D/'sa-book/threats').glob('*.md'));self.assertGreaterEqual(len(profiles),60)
        ids=set()
        families=set()
        for p in profiles:
            text=p.read_text()
            self.assertRegex(text,r'(?mi)^\*\*Status:\*\* .*untested.*(?:uncalibrated|no calibrated CV)')
            families.add(re.search(r'(?m)^\*\*Family:\*\* (.+)$',text)[1])
            self.assertGreater(int(re.search(r'\*\*HP:\*\* (\d+)',text)[1]),0)
            self.assertRegex(text,r'\*\*Defence:\*\* (?:Brawn|Fortitude|Agility|Guile|Knowledge|Reason) [+-]?\d+')
            self.assertGreaterEqual(len(re.findall(r'^- \*\*Weak:',text,re.M)),1)
            for band in ['Weak','Standard','Strong']:
                self.assertEqual(len(re.findall(r'^- \*\*'+band+':',text,re.M)),len(re.findall(r'^\*\*Action:.*\*\*Attribute:\*\* (?!None)',text,re.M)))
            ident=re.search(r'\*\*ID:\*\* (\S+)',text)[1];self.assertNotIn(ident,ids);ids.add(ident)
        self.assertEqual(families, {"Crews", "Security and synthetics", "Station fauna", "Void entities", "Alien ecology", "The Slop"})
    def test_sa_adversary_library_assignments(self):
        library = D / "sa-book/adversary-abilities"
        abilities = {p.stem: p for p in library.glob("*.md")}
        self.assertGreaterEqual(len(abilities), 80)
        assigned = set()
        ids = set()
        for threat in (D / "sa-book/threats").glob("*.md"):
            links = re.findall(r"(?m)^- \[([^]]+)\]\(\.\./adversary-abilities/([^/)]+)\.md\)$",
                               threat.read_text())
            self.assertTrue(links, threat.name)
            self.assertEqual(len(links), len({slug for _, slug in links}), threat.name)
            for title, slug in links:
                self.assertIn(slug, abilities, threat.name)
                self.assertEqual(abilities[slug].read_text().splitlines()[0], "# " + title)
                assigned.add(slug)
        self.assertEqual(assigned, set(abilities))
        for ability in abilities.values():
            text = ability.read_text()
            self.assertRegex(text, r"\*\*Action:\*\* (Maneuver|Reaction|Passive) · \*\*Attribute:\*\* None")
            self.assertIn("**Target / trigger:**", text)
            self.assertIn("untested", text)
            identifier = re.search(r"(?m)^\*\*ID:\*\* (adversary-\S+)$", text)[1]
            self.assertNotIn(identifier, ids)
            ids.add(identifier)
    def test_personal_companions_cover_each_family_and_tier(self):
        from collections import Counter

        profiles = D / "sa-book/companions"
        counts = Counter()
        ids = set()
        for path in profiles.glob("*.md"):
            text = path.read_text()
            family, level = re.search(
                r"\*\*Family:\*\* (Drone|Sprite|Hire) · \*\*Minimum controller level:\*\* ([137])",
                text,
            ).groups()
            counts[family, level] += 1
            self.assertIn("untested", text)
            self.assertIn("No independent activity or Reaction", text)
            ident = re.search(r"(?m)^\*\*ID:\*\* (companion-\S+)$", text)[1]
            self.assertNotIn(ident, ids)
            ids.add(ident)
        for family in ("Drone", "Sprite", "Hire"):
            for level in ("1", "3", "7"):
                self.assertGreaterEqual(counts[family, level], 3)
    def test_companion_references_point_to_actual_character_chapters(self):
        text=(D/'player-book/manuscript/11-starship-reference.md').read_text()
        self.assertIn('Chapters 4 and 8',text)
        for n in [2,3,4,5,6]:self.assertIn(f'Chapter {n}',text)
if __name__=='__main__':unittest.main()
