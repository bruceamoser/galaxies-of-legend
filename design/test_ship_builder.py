"""Structural tests for the proposed allocation rules, not balance tests."""
import copy, json, unittest
from pathlib import Path
from ship_builder import DATA, validate

EXAMPLES=json.loads((Path(__file__).parent/'ships/examples.json').read_text())

class ShipBuilderTests(unittest.TestCase):
    def ship(self):return copy.deepcopy(EXAMPLES[0])
    def reject(self,ship,fragment):
        result=validate(ship)
        self.assertFalse(result['valid'])
        self.assertTrue(any(fragment in error for error in result['errors']),result)
    def test_examples_use_exact_budgets(self):
        for ship in EXAMPLES:
            result=validate(ship)
            self.assertTrue(result['valid'],result)
            self.assertEqual(result['spent'],result['budget'])
    def test_required_system_not_free_or_omittable(self):
        ship=self.ship();ship['modules']=ship['modules'][1:]
        self.reject(ship,'Required system engines')
    def test_budget_overrun(self):
        ship=self.ship();ship['modules'].append({'id':'extra-hold','type':'cargo','die':'d10'})
        self.reject(ship,'Allocation budget exceeded')
    def test_unique_system_cannot_be_duplicated(self):
        ship=self.ship();ship['modules'].append({'id':'second-nav','type':'navigation','die':'d4'})
        self.reject(ship,'not repeatable')
    def test_ids_are_unique(self):
        ship=self.ship();ship['modules'][1]['id']='engines'
        self.reject(ship,'unique non-empty id')
    def test_frame_die_ceiling(self):
        ship=copy.deepcopy(EXAMPLES[2]);ship['modules'][0]['die']='d12'
        self.reject(ship,'die ceiling')
    def test_ftl_needs_capacitors(self):
        ship=self.ship();ship['modules']=[m for m in ship['modules'] if m['type']!='capacitors']
        self.reject(ship,'installed together')
    def test_capacitors_need_ftl(self):
        ship=self.ship();ship['modules']=[m for m in ship['modules'] if m['type']!='ftl']
        self.reject(ship,'installed together')
    def test_targeting_needs_mount(self):
        ship=copy.deepcopy(EXAMPLES[2]);ship['modules'][-1]={'id':'aim','type':'targeting','die':'d4'}
        self.reject(ship,'requires a weapon')
    def test_module_limit(self):
        ship=copy.deepcopy(EXAMPLES[2]);ship['modules'].append({'id':'hold-2','type':'cargo','die':'d4'})
        self.reject(ship,'Module limit')
    def test_hangar_size_and_minimum(self):
        ship=self.ship();ship['modules'][-1]={'id':'hangar','type':'hangar','die':'d4'}
        result=validate(ship);self.assertFalse(result['valid'])
        self.assertTrue(any('at least d6' in e for e in result['errors']))
        self.assertTrue(any('medium frame' in e for e in result['errors']))
    def test_unknown_module_and_die(self):
        ship=self.ship();ship['modules'][0]['type']='magic';self.reject(ship,'unknown system')
        ship=self.ship();ship['modules'][0]['die']='d20';self.reject(ship,'invalid die')
    def test_d6_sensors_improve_capability_and_quality(self):
        self.assertEqual(DATA['performance']['sensor_reach']['d4'],'Near')
        self.assertEqual(DATA['performance']['sensor_reach']['d6'],'Far')
        self.assertGreater(DATA['grades']['d6'],DATA['grades']['d4'])
    def test_upgrade_cost_is_difference(self):
        self.assertEqual(DATA['die_cost']['d8']-DATA['die_cost']['d6'],1)

if __name__=='__main__':unittest.main()
