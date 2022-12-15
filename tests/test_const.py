import pytest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestConst:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_ev_bad_const(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("const bogus")
        assert "Invalid syntax" in str(ae.value)

    def test_ev_good_const(self):
        self.ev.ev("const meaning-of-the-universe 42")
        self.ev.ev("meaning-of-the-universe 42 =")

    def test_ev_bad_constp(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("const bogus 47 45 ")
        assert "Invalid syntax" in str(ae.value)

    def test_ev_good_constp(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("const meaning-of-the-universe 21 2 *")
            self.ev.ev("meaning-of-the-universe .")
            output = fp.getvalue()
        assert "42" in output
