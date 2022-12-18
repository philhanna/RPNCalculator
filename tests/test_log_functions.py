import pytest
from pytest import approx


@pytest.mark.parametrize("test_input, expected", [
    ("2 exp", approx(7.389056098)),
    ("2 ln", approx(0.6931471805599453)),
    ("2 log", approx(0.301029995663981))
])
def test_log_function(ev, test_input, expected):
    ev.ev(test_input)
    actual = ev.pop().value
    assert actual == expected
