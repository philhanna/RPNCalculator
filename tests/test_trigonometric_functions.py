from mpmath import e, pi, radians, sin, cos
import pytest
from evaluator import Evaluator


class TestTrigonometricFunctions:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_e(self):
        self.ev.ev("e")
        expected = e
        actual = self.ev.pop().value
        assert actual == expected

    def test_todegrees(self):
        self.ev.ev("pi toDegrees")
        expected = 180
        actual = self.ev.pop().value
        assert actual == expected

    def test_toradians(self):
        self.ev.ev("90 toRadians")
        expected = pi / 2.0
        actual = self.ev.pop().value
        pytest.approx(expected, actual)

    def test_acos(self):
        self.ev.ev("0.5 acos toDegrees")
        expected = 60
        actual = self.ev.pop().value
        pytest.approx(expected, actual)

    def test_asin(self):
        self.ev.ev("3 sqrt 2 / asin toDegrees")
        expected = 60
        actual = self.ev.pop().value
        pytest.approx(expected, actual)

    def test_atan(self):
        self.ev.ev("1 atan")
        actual = self.ev.pop().value
        expected = pi / 4
        pytest.approx(expected, actual)

    def test_atan2(self):
        self.ev.ev("-1 -1 atan2")
        actual = self.ev.pop().value
        expected = -3 * pi / 4
        pytest.approx(expected, actual)

    def test_cos(self):
        self.ev.ev("55 toRadians cos")
        actual = self.ev.pop().value
        expected = cos(radians(55))
        pytest.approx(expected, actual)

    def test_sin(self):
        self.ev.ev("14 toRadians sin")
        actual = self.ev.pop().value
        expected = sin(radians(14))
        pytest.approx(expected, actual)

    def test_tan(self):
        self.ev.ev("45 toRadians tan")
        actual = self.ev.pop().value
        expected = 1
        pytest.approx(expected, actual)
