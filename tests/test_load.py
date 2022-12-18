from pathlib import Path

import pytest

from tests import tmp


def test_ev_bad_load(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("load bogus")
    assert "Could not" in str(ae.value)


def test_ev_good_load(ev, capsys, tmp_path):
    filename = tmp_path / "file1"
    with open(filename, "w") as fp:
        print(" ", file=fp)
        print("const meaning 42", file=fp)
        print("# quit", file=fp)
    try:
        ev.ev(f"load {filename}")
        ev.ev("meaning .")
        output = capsys.readouterr().out
        assert "42" in output
    finally:
        filename.unlink()
