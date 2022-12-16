from pathlib import Path
import tempfile
from io import StringIO
import pytest
from evaluator import Evaluator
from tests import stdout_redirected

tmp = tempfile.gettempdir()


class TestLoad:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_ev_bad_load(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("load bogus")
        assert "Could not" in str(ae.value)

    def test_ev_good_load(self):
        filename = Path(tmp).joinpath("file1")
        with open(filename, "w") as fp:
            print(" ", file=fp)
            print("const meaning 42", file=fp)
            print("# quit", file=fp)
        try:
            with StringIO() as fp, stdout_redirected(fp):
                self.ev.ev(f"load {filename}")
                self.ev.ev("meaning .")
                output = fp.getvalue()
            assert "42" in output
        finally:
            filename.unlink()
