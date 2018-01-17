#! /usr/bin/python3

import unittest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Evaluator import Evaluator

class TestArithmeticOperations(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_add(self):
        ev = self.ev
        ev.ev('2 3')
        ev.doAdd()
        expected = 5
        actual = ev.pop()
        self.assertEqual(expected, actual)

    def test_sub(self):
        ev = self.ev
        ev.ev('3 5')
        ev.doSub()
        expected = -2
        actual = ev.pop()
        self.assertEqual(expected, actual)

    def test_mult(self):
        self.ev.ev("10 1.8 *")
        expected = 18
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_div(self):
        self.ev.ev("10 1.8 /")
        expected = 5.55555555
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)

    def test_increment(self):
        self.ev.ev("2 ++")
        expected = 3
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

        self.ev.ev("4 1+")
        expected = 5
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_decrement(self):
        self.ev.ev("2 --")
        expected = 1
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

        self.ev.ev("4 1-")
        expected = 3
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_mod(self):
        self.ev.ev("7 3 mod")
        expected = 1
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

        self.ev.ev("14 5 %")
        expected = 4
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_int(self):
        self.ev.ev("7 3 / int")
        expected = 2
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_sqrt(self):
        self.ev.ev("9 sqrt")
        expected = 3
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_pow(self):
        self.ev.ev("2 3 **")
        expected = 8
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
