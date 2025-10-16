import unittest
from planets.tests import PlanetAPITestCase
from goodreads.tests import GoodreadsAPITestCase


def test_run_planet_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(PlanetAPITestCase)
    unittest.TextTestRunner().run(suite)


def test_run_goodreads_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(GoodreadsAPITestCase)
    unittest.TextTestRunner().run(suite)