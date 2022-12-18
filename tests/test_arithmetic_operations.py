import pytest
from pytest import approx


# Tests for operations fully performed in the interpreter
@pytest.mark.parametrize("test_input,expected", [
    ("2 3 +", 5),
    ("3 5 -", -2),
    ("2 ++", 3),
    ("4 1+", 5),
    ("2 --", 1),
    ("4 1-", 3),
    ("14 5 %", 4),
    ("7 3 / int", 2),
    ("9 sqrt", 3),
    ("2 3 **", 8),
    ("2 4 ^", 16),
    ("10 1.8 *", approx(18)),
    ("10 1.8 /", approx(5.55555555)),
    ("2 1 3 / **", approx(1.259921049894873)),
])
def test_by_command(ev, test_input, expected):
    ev.ev(test_input)
    assert ev.pop().value == expected


# Tests for operations performed here in the test method
@pytest.mark.parametrize("test_input,fname,expected", [
    ("2 3", "do_add", 5),
    ("3 5", "do_sub", -2),
    ("10 11", "do_mult", 110),
])
def test_operation(ev, test_input, fname, expected):
    ev.ev(test_input)
    exec(f"ev.{fname}()")
    assert ev.pop().value == expected


# Tests which fail and produce error messages
@pytest.mark.parametrize("test_input,errmsg", [
    ("10 0 /", "divide by zero"),
    ("14 0 %", "divide by zero"),
    ("-3 sqrt", "negative"),
    ("-3 2 **", "Cannot exponentiate"),
    ("0 2 **", "Cannot exponentiate"),
])
def tests_with_errors(ev, test_input, errmsg):
    with pytest.raises(RuntimeError) as ae:
        ev.ev(test_input)
    assert errmsg in str(ae.value)


def test_empty_stack(ev, capsys):
    ev.ev("2")
    ev.do_add()
    captured = capsys.readouterr()
    assert "Stack empty" in captured.out
