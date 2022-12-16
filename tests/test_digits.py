from io import StringIO

import pytest

from evaluator import Evaluator
from tests import stdout_redirected


class TestDigits:

    def test_do_digits(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("digits")
            output = fp.getvalue().strip()
        assert output.isdecimal()

    def test_set_digits(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("digits 15")
            ev.ev("pi .")
            output = fp.getvalue().strip()
        assert "3.14159265358979" == output

    def test_bad_digits(self):
        ev = Evaluator()
        with pytest.raises(RuntimeError) as ae:
            ev.ev("digits asdf")
        assert "'asdf'" in str(ae.value)
