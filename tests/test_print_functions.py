import math
import unittest

from mpmath import log10

from evaluator import Evaluator


class TestPrintFunctions(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_log5(self):
        self.ev.ev('2 log ')
        x = self.ev.pop()
        actual = x
        expected = log10(2)
        self.assertEqual(expected, actual)
