import pytest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestDefine:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_ev_bad_define(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("define bogus")
        assert "No function" in str(ae.value)

    def test_ev_good_define(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("define double dup 2 *")
            self.ev.ev("7 double .")
            output = fp.getvalue()
        assert "14" in output
