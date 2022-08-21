from unittest import TestCase

from evaluator import Evaluator


class TestVariable(TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_store(self):
        self.ev.ev("var amount")
        self.ev.ev("25 amount !")
        self.ev.ev("amount")
        expected = 1
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_fetch(self):
        self.ev.ev("var amount")
        self.ev.ev("1 3 / amount !")
        self.ev.ev("amount @")
        expected = .3333333333333333
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)