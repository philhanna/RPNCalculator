import pytest

from evaluator import Evaluator


class TestLogFunctions:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_exp(self):
        self.ev.ev("2 exp")
        actual = self.ev.pop().value
        expected = 7.389056098
        pytest.approx(expected, actual)

    def test_ln(self):
        self.ev.ev("2 ln")
        actual = self.ev.pop().value
        expected = 0.6931471805599453
        pytest.approx(expected, actual)

    def test_log(self):
        self.ev.ev("2 log")
        actual = self.ev.pop().value
        expected = 0.301029995663981
        pytest.approx(expected, actual)
