"""Regression checks for the SA book's printed comparison fixtures."""
from fractions import Fraction
from pathlib import Path
import runpy
import unittest

BOOK = Path(__file__).parent / "sa-book"
CV = runpy.run_path(str(BOOK / "cv.py"))


class EncounterCVTests(unittest.TestCase):
    def test_reference_dice_and_net_modifiers(self):
        probabilities = CV["outcome_probabilities"]
        self.assertEqual(probabilities(), tuple(Fraction(n, 216) for n in (35, 146, 35)))
        self.assertGreater(probabilities(net_dice=1)[2], probabilities()[2])
        self.assertGreater(probabilities(net_dice=-1)[0], probabilities()[0])
        self.assertEqual(sum(probabilities(net_dice=3)), 1)

    def test_minimum_damage_and_anchor(self):
        damage = CV["expected_damage"]
        self.assertEqual(damage((1, 2, 3), 3, CV["outcome_probabilities"]()), 1)
        catalog = CV["read_catalog"](BOOK)
        self.assertEqual(catalog["dock-watch"][2].value, 11)
        self.assertIsNone(catalog["field-medic"][2])
        self.assertEqual(sum(row[2] is not None for row in catalog.values()), len(catalog) - 1)

    def test_mixed_levels_and_unrated_roster(self):
        self.assertEqual(CV["party_budget"]([1, 1, 3, 3], 11), 52)
        self.assertEqual(CV["party_budget"]([1, 1, 1], 11, "easy"), Fraction(99, 4))
        catalog = CV["read_catalog"](BOOK)
        expected = [(44, [], 44), (32, [], 33), (44, [], 52), (50, [], 60),
                    (46, ["1 × Field Medic"], 90), (87, [], 92)]
        paths = sorted((BOOK / "encounters").glob("*.md"))
        self.assertEqual([CV["encounter_roster"](p, catalog) for p in paths], expected)
