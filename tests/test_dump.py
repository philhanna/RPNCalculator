import re


def test_dump_stack(ev, capsys):
    ev.ev("1 5 2")
    ev.ev(".S")
    actual = capsys.readouterr().out
    expected = "1.0\n5.0\n2.0\n"
    assert actual == expected


def test_dump_functions(ev, capsys):
    ev.ev("define meaning 42")
    ev.ev(".F")
    actual = capsys.readouterr().out
    expected = r"FUNCTION\s+DEFINITION.*meaning\s+42"
    assert re.search(expected, actual, re.DOTALL)


def test_dump_functions_none_defined(ev, capsys):
    ev.ev(".F")
    actual = capsys.readouterr().out
    expected = ""
    assert actual == expected


def test_dump_variables_none_defined(ev, capsys):
    ev.ev(".V")
    actual = capsys.readouterr().out
    expected = ""
    assert actual == expected


def test_dump_constants_none_defined(ev, capsys):
    ev.ev(".C")
    actual = capsys.readouterr().out
    expected = ""
    assert actual == expected
