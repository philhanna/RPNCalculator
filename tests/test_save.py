import tempfile
from io import StringIO
from pathlib import Path

import pytest

from evaluator import Evaluator
from tests import stdout_redirected

tmp = tempfile.gettempdir()


class TestSave:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_ev_save_no_filename(self):
        self.ev.ev("const meaning 42")
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev(f"save")
        assert "No file name" in str(ae.value)

    def test_ev_good_save(self):
        filename = Path(tmp).joinpath("good_save")
        try:
            with StringIO() as fp, stdout_redirected(fp):
                self.ev.ev("const meaning 42")
                self.ev.ev("var addr")
                self.ev.ev("7500 addr !")
                self.ev.ev("define double dup 2 *")
                self.ev.ev(f"save {filename}")
                output = fp.getvalue()
            assert "saved to" in output
        finally:
            filename.unlink()
