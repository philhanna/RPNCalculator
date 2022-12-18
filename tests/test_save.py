import pytest


def test_ev_save_no_filename(ev):
    ev.ev("const meaning 42")
    with pytest.raises(RuntimeError) as ae:
        ev.ev("save")
    assert "No file name" in str(ae.value)


def test_ev_good_save(ev, capsys, tmp_path):
    filename = tmp_path / "good_save"
    ev.ev("const meaning 42")
    ev.ev("var addr")
    ev.ev("7500 addr !")
    ev.ev("define double dup 2 *")
    ev.ev(f"save {filename}")
    output = capsys.readouterr().out
    assert "saved to" in output
