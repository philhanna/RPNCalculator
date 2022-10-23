import unittest

from evaluator import Evaluator


class TestLogFunctions(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_exp(self):
        self.ev.ev("2 exp")
        actual = self.ev.pop()
        expected = 7.389056098
        self.assertAlmostEqual(expected, actual)

    def test_ln(self):
        self.ev.ev("2 ln")
        actual = self.ev.pop()
        expected = 0.6931471805599453
        self.assertAlmostEqual(expected, actual)

    def test_log(self):
        self.ev.ev("2 log")
        actual = self.ev.pop()
        expected = 0.301029995663981
        self.assertAlmostEqual(expected, actual)
