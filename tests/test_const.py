import pytest


def test_ev_bad_const(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("const bogus")
    assert "Invalid syntax" in str(ae.value)


def test_ev_good_const(ev):
    ev.ev("const meaning-of-the-universe 42")
    ev.ev("meaning-of-the-universe 42 =")


def test_ev_bad_constp(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("const bogus 47 45 ")
    assert "Invalid syntax" in str(ae.value)


def test_ev_good_constp(ev, capsys):
    ev.ev("const meaning-of-the-universe 21 2 *")
    ev.ev("meaning-of-the-universe .")
    output = capsys.readouterr().out
    assert "42" in output
