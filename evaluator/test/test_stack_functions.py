import unittest
from evaluator.Evaluator import Evaluator


class TestStackFunctions(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_clear(self):
        self.ev.ev("1 2 3")
        self.assertEqual(len(self.ev.stack), 3)
        self.ev.ev("clear")
        self.assertEqual(len(self.ev.stack), 0)

    def test_depth(self):
        self.ev.ev("45 11 depth")
        expected = 2
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_drop(self):
        self.ev.ev("1 2 3 drop")
        self.assertListEqual(self.ev.stack, [1.0, 2.0])

    def test_dup(self):
        self.ev.ev("5 dup")
        self.assertListEqual(self.ev.stack, [5, 5])

    def test_over(self):
        self.ev.ev("1 2 over")
        self.assertListEqual(self.ev.stack, [1, 2, 1])

    def test_rot(self):
        self.ev.ev("10 20 30 rot")
        self.assertListEqual(self.ev.stack, [20, 30, 10])

    def test_swap(self):
        self.ev.ev("10 20 30 swap")
        self.assertListEqual(self.ev.stack, [10, 30, 20])
