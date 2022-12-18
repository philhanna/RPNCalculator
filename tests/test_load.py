import pytest


def test_ev_bad_load(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("load bogus")
    assert "Could not" in str(ae.value)


def test_ev_good_load(ev, capsys, tmp_path):
    testfile = tmp_path / "file1"
    testfile.write_text("""\

const meaning 42
# quit
""")
    ev.ev(f"load {testfile}")
    ev.ev("meaning .")
    output = capsys.readouterr().out
    assert "42" in output
