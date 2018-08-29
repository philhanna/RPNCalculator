#! /usr/bin/python3

import unittest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Evaluator import Evaluator

class TestTrigonometricFunctions(unittest.TestCase):

    pi = 3.14159265358979

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_todegrees(self):
        self.ev.ev("pi toDegrees")
        expected = 180
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_toradians(self):
        self.ev.ev("90 toRadians")
        expected = self.pi / 2.0
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)

    def test_acos(self):
        self.ev.ev("0.5 acos toDegrees")
        expected = 60
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)

    def test_asin(self):
        self.ev.ev("3 sqrt 2 / asin toDegrees")
        expected = 60
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)

    def test_atan(self):
        self.ev.ev("1 atan")
        actual = self.ev.pop()
        expected = self.pi / 4
        self.assertAlmostEqual(expected, actual)

    def test_atan2(self):
        self.ev.ev("-1 -1 atan2")
        actual = self.ev.pop()
        expected = -3 * self.pi / 4
        self.assertAlmostEqual(expected, actual)

    def test_cos(self):
        self.ev.ev("55 toRadians cos")
        actual = self.ev.pop()
        expected = 0.573576436351
        self.assertAlmostEqual(expected, actual)

    def test_sin(self):
        self.ev.ev("14 toRadians sin")
        actual = self.ev.pop()
        expected = 0.2419218956
        self.assertAlmostEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
