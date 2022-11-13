from unittest import TestCase

import evaluator


class TestBoolean(TestCase):

    def setUp(self) -> None:
        self.ev = evaluator.Evaluator()

    def tearDown(self) -> None:
        del self.ev

    def test_do_greater_than_when_false(self):
        ev = self.ev
        ev.ev("2 3")
        ev.do_greater_than()
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_greater_than_when_true(self):
        ev = self.ev
        ev.ev("3 2")
        ev.do_greater_than()
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_greater_than_when_false(self):
        ev = self.ev
        ev.ev("10 11 >")
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_greater_than_when_true(self):
        ev = self.ev
        ev.ev("11 3 >")
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_less_than_when_false(self):
        ev = self.ev
        ev.ev("3 2")
        ev.do_less_than()
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_less_than_when_true(self):
        ev = self.ev
        ev.ev("2 3")
        ev.do_less_than()
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_less_than_when_false(self):
        ev = self.ev
        ev.ev("11 10 <")
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_less_than_when_true(self):
        ev = self.ev
        ev.ev("3 11 <")
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_equal_to_when_true(self):
        ev = self.ev
        ev.ev("3 3")
        ev.do_equal_to()
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_equal_to_when_false(self):
        ev = self.ev
        ev.ev("1 3")
        ev.do_equal_to()
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_equal_to_when_true(self):
        ev = self.ev
        ev.ev("11 11 =")
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_equal_to_when_false(self):
        ev = self.ev
        ev.ev("111 112 =")
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_not_equal_to_when_true(self):
        ev = self.ev
        ev.ev("3 4")
        ev.do_not_equal_to()
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_do_not_equal_to_when_false(self):
        ev = self.ev
        ev.ev("3 3")
        ev.do_not_equal_to()
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_not_equal_to_when_true(self):
        ev = self.ev
        ev.ev("11 12 !=")
        expected = True
        actual = ev.pop().value
        self.assertEqual(expected, actual)

    def test_not_equal_to_when_false(self):
        ev = self.ev
        ev.ev("1 1 !=")
        expected = False
        actual = ev.pop().value
        self.assertEqual(expected, actual)
