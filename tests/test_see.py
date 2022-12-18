import pytest


def test_f(ev, capsys):
    ev.ev("define even 2 mod 0 =")
    ev.ev("see even")
    actual = capsys.readouterr().out.strip()
    expected = "function EVEN: 2 mod 0 ="
    assert actual == expected


def test_v(ev, capsys):
    ev.ev("var stop")
    ev.ev("false stop !")
    ev.ev("see stop")
    actual = capsys.readouterr().out.strip()
    expected = "variable STOP"
    assert expected in actual


def test_c(ev, capsys):
    ev.ev("const k 25")
    ev.ev("see k")
    actual = capsys.readouterr().out.strip()
    expected = "constant K: 25.0"
    assert expected in actual


def test_bogus(ev, capsys):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("see bogus")
    actual = str(ae.value)
    expected = "SEE must be followed"
    assert expected in actual
