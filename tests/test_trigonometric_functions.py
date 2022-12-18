import pytest
from mpmath import e, pi
from pytest import approx


@pytest.mark.parametrize("test_input, expected", [
    ("e", e),
    ("pi", pi),
    ("pi toDegrees", 180),
    ("90 toRadians", pi / 2.0),
    ("0.5 acos toDegrees", approx(60)),
    ("3 sqrt 2 / asin toDegrees", approx(60)),
    ("1 atan", approx(pi / 4)),
    ("-1 -1 atan2", approx(-3 * pi / 4)),
    ("55 toRadians cos", approx(0.573576436)),
    ("14 toRadians sin", approx(0.241921896)),
    ("45 toRadians tan", approx(1)),
])
def test_trigonometric_function(ev, test_input, expected):
    ev.ev(test_input)
    actual = ev.pop().value
    assert actual == expected
