from io import StringIO
import pytest

import evaluator
from tests import stdout_redirected


class TestBoolean:

    def setup_method(self) -> None:
        self.ev = evaluator.Evaluator()

    def teardown_method(self) -> None:
        del self.ev

    def test_do_greater_than_when_false(self):
        ev = self.ev
        ev.ev("2 3")
        ev.do_greater_than()
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_do_greater_than_when_true(self):
        ev = self.ev
        ev.ev("3 2")
        ev.do_greater_than()
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_greater_than_when_false(self):
        ev = self.ev
        ev.ev("10 11 >")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_greater_than_when_true(self):
        ev = self.ev
        ev.ev("11 3 >")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_do_less_than_when_false(self):
        ev = self.ev
        ev.ev("3 2")
        ev.do_less_than()
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_do_less_than_when_true(self):
        ev = self.ev
        ev.ev("2 3")
        ev.do_less_than()
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_less_than_when_false(self):
        ev = self.ev
        ev.ev("11 10 <")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_less_than_when_true(self):
        ev = self.ev
        ev.ev("3 11 <")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_do_equal_to_when_true(self):
        ev = self.ev
        ev.ev("3 3")
        ev.do_equal_to()
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_do_equal_to_when_false(self):
        ev = self.ev
        ev.ev("1 3")
        ev.do_equal_to()
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_equal_to_when_true(self):
        ev = self.ev
        ev.ev("11 11 =")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_equal_to_when_false(self):
        ev = self.ev
        ev.ev("111 112 =")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_do_not_equal_to_when_true(self):
        ev = self.ev
        ev.ev("3 4")
        ev.do_not_equal_to()
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_do_not_equal_to_when_false(self):
        ev = self.ev
        ev.ev("3 3")
        ev.do_not_equal_to()
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_not_equal_to_when_true(self):
        ev = self.ev
        ev.ev("11 12 !=")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_not(self):
        ev = self.ev
        ev.ev("2 not")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_not_when_false(self):
        ev = self.ev
        ev.ev("False not")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_not_idempotent(self):
        ev = self.ev
        ev.ev("42 not not")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_not_equal_to_when_false(self):
        ev = self.ev
        ev.ev("1 1 !=")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_true(self):
        with StringIO() as out, stdout_redirected(out):
            ev = self.ev
            ev.ev("true .")
            actual = out.getvalue()
        expected = "True"
        assert expected in actual

    def test_and_when_false(self):
        ev = self.ev
        ev.ev("True 2 3 > and")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_and_when_true(self):
        ev = self.ev
        ev.ev("2 3 < 4 5 < and")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_or_when_false(self):
        ev = self.ev
        ev.ev("True 2 3 > or")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_or_when_true(self):
        ev = self.ev
        ev.ev("2 3 < 4 5 < or")
        expected = True
        actual = ev.pop().value
        assert actual == expected

    def test_xor_when_false(self):
        ev = self.ev
        ev.ev("False False xor")
        expected = False
        actual = ev.pop().value
        assert actual == expected

    def test_xor(self):
        ev = self.ev
        ev.ev("2 6 xor")
        expected = False
        actual = ev.pop().value
        assert actual == expected
