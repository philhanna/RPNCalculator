import pytest


def test_ev_bad_define(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("define bogus")
    assert "No function" in str(ae.value)


def test_ev_good_define(ev, capsys):
    ev.ev("define double dup 2 *")
    ev.ev("7 double .")
    output = capsys.readouterr().out
    assert "14" in output
