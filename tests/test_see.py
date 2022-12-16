from io import StringIO

import pytest

from evaluator import Evaluator
from tests import stdout_redirected


class TestSee:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self) -> None:
        del self.ev

    def test_f(self):
        self.ev.ev("define even 2 mod 0 =")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see even")
            actual = out.getvalue().strip()
        expected = "function EVEN: 2 mod 0 ="
        assert actual == expected

    def test_v(self):
        self.ev.ev("var stop")
        self.ev.ev("false stop !")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see stop")
            actual = out.getvalue().strip()
        expected = "variable STOP"
        assert expected in actual

    def test_c(self):
        self.ev.ev("const k 25")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see k")
            actual = out.getvalue().strip()
        expected = "constant K: 25.0"
        assert expected in actual

    def test_bogus(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("see bogus")
        actual = str(ae.value)
        expected = "SEE must be followed"
        assert expected in actual
