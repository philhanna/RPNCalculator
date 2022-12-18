import pytest


@pytest.mark.parametrize("cmdline,fname,expected", [
    ("2 3", "do_greater_than", False),
    ("3 2", "do_greater_than", True),
    ("3 2", "do_less_than", False),
    ("2 3", "do_less_than", True),
    ("3 3", "do_equal_to", True),
    ("1 3", "do_equal_to", False),
    ("3 4", "do_not_equal_to", True),
    ("3 3", "do_not_equal_to", False),
])
def test_boolean(ev, cmdline, fname, expected):
    ev.ev(cmdline)
    exec(f"ev.{fname}()")
    actual = ev.pop().value
    assert actual == expected


@pytest.mark.parametrize("cmdline,expected", [
    ("10 11 >", False),
    ("10 11 >=", False),
    ("11 3 >", True),
    ("11 10 <", False),
    ("3 11 <", True),
    ("11 11 =", True),
    ("111 112 =", False),
    ("11 12 !=", True),
    ("2 not", False),
    ("False not", True),
    ("42 not not", True),
    ("1 1 !=", False),
    ("True 2 3 > and", False),
    ("2 3 < 4 5 < and", True),
    ("True 2 3 > or", True),
    ("2 3 < 4 5 < or", True),
    ("False false xor", False),
    ("2 6 xor", False),
])
def test_boolean_by_command(ev, cmdline, expected):
    ev.ev(cmdline)
    actual = ev.pop().value
    assert actual == expected


@pytest.mark.parametrize("test_input,expected", [
    ("true .", "True"),
    ("false .", "False"),
])
def test_output(ev, test_input, expected, capsys):
    ev.ev(test_input)
    actual = capsys.readouterr().out
    assert expected in actual

