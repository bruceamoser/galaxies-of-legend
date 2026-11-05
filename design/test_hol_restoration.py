"""Content-integrity gates for the complete inherited HOL wound foundation."""
import hashlib,itertools,json,re,unittest
from pathlib import Path
D=Path(__file__).parent

class HOLRestorationTests(unittest.TestCase):
    def test_280_rows_match_recorded_hol_baseline(self):
        text=(D/'rules/wounds.md').read_text()
        rows=[row for row in re.findall(r'^\| [1-6]{3} \|.*$',text,re.M) if row.count('|')==6]
        baseline=json.loads((D/'rules/hol-restoration.json').read_text())
        self.assertEqual(len(rows),280)
        self.assertEqual(hashlib.sha256('\n'.join(rows).encode()).hexdigest(),baseline['wound_rows_sha256'])
    def test_every_family_has_all_56_sorted_results(self):
        text=(D/'rules/wounds.md').read_text()
        families=re.split(r'^## (Physical|Elemental|Mental|Radiant|Life/Necrotic)\s*$',text,flags=re.M)
        self.assertEqual(len(families),11)
        expected={''.join(map(str,t)) for t in itertools.combinations_with_replacement(range(1,7),3)}
        for name,section in zip(families[1::2],families[2::2]):
            rolls=re.findall(r'^\| ([1-6]{3}) \|',section,re.M)
            self.assertEqual(len(rolls),56,name)
            self.assertEqual(set(rolls),expected,name)
            self.assertEqual(rolls[-1],'666',name)
    def test_all_six_treatment_capabilities_keep_time_attribute_and_economy(self):
        for slug,attribute in [('soft-tissue','Knowledge'),('bone','Knowledge'),('mental-trauma','Reason'),('elemental-injury','Knowledge'),('radiant-injury','Reason'),('life-injury','Reason')]:
            text=(D/'cards'/f'treat-{slug}.md').read_text()
            self.assertIn('**Time:** One hour.',text)
            self.assertIn('**Attribute:** '+attribute,text)
            self.assertIn('**DP:** 2',text)
            self.assertIn('Medicine 1',text)
            self.assertIn('One attempt per wound per day across all healers',text)
            for n in [1,2,3]:self.assertIn(f'Add {n} recovery progress',text)
    def test_stabilization_is_universal_maneuver_not_a_medicine_roll(self):
        text=(D/'cards/stabilize.md').read_text()
        self.assertIn('**Action:** Maneuver',text)
        self.assertIn('**Attribute:** None',text)
        self.assertIn('**Tier / minimum level:** Universal',text)
        self.assertIn('clear death marks',text)
    def test_once_only_grit_grant_is_not_a_refill(self):
        text=(D/'cards/one-more-dawn.md').read_text()
        self.assertIn('Purchase once ever',text)
        self.assertIn('does not replenish previously spent Grit',text)
        self.assertIn('**Tier / minimum level:** 7',text)
    def test_healing_costs_are_present_on_existing_medical_cards(self):
        for slug,cost in [('patch-wounds',1),('field-triage',1),('combat-medic',3),('signature-medic-triage',1),('signature-medic-field-surgery',3),('signature-medic-last-light',7)]:
            text=(D/'cards'/f'{slug}.md').read_text()
            self.assertIn(f'Pay {cost} HP before rolling',text)
            self.assertIn('Life resistance',text)
            self.assertIn('Last Words',text)
    def test_field_surgery_does_not_bypass_rv(self):
        text=(D/'cards/signature-medic-field-surgery.md').read_text()
        self.assertIn('one full hour',text)
        self.assertIn('Only reaching the wound\'s RV',text)
        self.assertNotIn('remove one wound penalty',text)
    def test_consumable_healing_keeps_hol_values_and_d4(self):
        for slug,hp in [('basic-medical-dose',6),('greater-medical-dose',10),('superior-medical-dose',16)]:
            text=(D/'equipment'/f'{slug}.md').read_text()
            self.assertIn('Inventory d4',text)
            self.assertIn(f'restore {hp} HP before Life resistance',text)
            self.assertIn('No outcome roll or healer HP cost',text)

if __name__=='__main__':unittest.main()
