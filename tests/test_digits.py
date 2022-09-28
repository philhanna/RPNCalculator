from io import StringIO
from unittest import TestCase

from evaluator import Evaluator
from tests import stdout_redirected


class TestDigits(TestCase):

    def test_do_digits(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("digits")
            output = fp.getvalue().strip()
        self.assertTrue(output.isdecimal())

    def test_set_digits(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("digits 15")
            ev.ev("pi .")
            output = fp.getvalue().strip()
        self.assertEqual("3.14159265358979", output)

    def test_bad_digits(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("digits asdf")
            output = fp.getvalue().strip()
        self.assertEqual("'asdf' is not a valid value for digits", output)
