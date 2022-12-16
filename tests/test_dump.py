import re
from io import StringIO

import evaluator
from tests import stdout_redirected


class TestDump:

    def setup_method(self) -> None:
        self.ev = evaluator.Evaluator()

    def teardown_method(self) -> None:
        del self.ev

    def test_dump_stack(self):
        with StringIO() as fpout, stdout_redirected(fpout):
            ev = self.ev
            ev.ev("1 5 2")
            ev.ev(".S")
            actual = fpout.getvalue()
        expected = "1.0\n5.0\n2.0\n"
        assert actual == expected

    def test_dump_functions(self):
        with StringIO() as fpout, stdout_redirected(fpout):
            ev = self.ev
            ev.ev("define meaning 42")
            ev.ev(".F")
            actual = fpout.getvalue()
        expected = r"FUNCTION\s+DEFINITION.*meaning\s+42"
        assert re.search(expected, actual, re.DOTALL)

    def test_dump_functions_none_defined(self):
        with StringIO() as fpout, stdout_redirected(fpout):
            ev = self.ev
            ev.ev(".F")
            actual = fpout.getvalue()
        expected = ""
        assert actual == expected

    def test_dump_variables_none_defined(self):
        with StringIO() as fpout, stdout_redirected(fpout):
            ev = self.ev
            ev.ev(".V")
            actual = fpout.getvalue()
        expected = ""
        assert actual == expected

    def test_dump_constants_none_defined(self):
        with StringIO() as fpout, stdout_redirected(fpout):
            ev = self.ev
            ev.ev(".C")
            actual = fpout.getvalue()
        expected = ""
        assert actual == expected
