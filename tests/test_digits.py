import pytest


def test_do_digits(ev, capsys):
    ev.ev("digits")
    output = capsys.readouterr().out.strip()
    assert output.isdecimal()


def test_set_digits(ev, capsys):
    ev.ev("digits 15")
    ev.ev("pi .")
    output = capsys.readouterr().out.strip()
    assert "3.14159265358979" == output


def test_bad_digits(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("digits asdf")
    assert "'asdf'" in str(ae.value)
