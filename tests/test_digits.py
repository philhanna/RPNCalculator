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
        ev = Evaluator()
        with self.assertRaises(RuntimeError) as ae:
            ev.ev("digits asdf")
        self.assertIn("'asdf'", str(ae.exception))
