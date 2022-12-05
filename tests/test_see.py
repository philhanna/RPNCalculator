from io import StringIO
from unittest import TestCase

from evaluator import Evaluator
from tests import stdout_redirected


class TestSee(TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self) -> None:
        del self.ev

    def test_f(self):
        self.ev.ev("define even 2 mod 0 =")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see even")
            actual = out.getvalue().strip()
        expected = "function EVEN: 2 mod 0 ="
        self.assertEqual(expected, actual)

    def test_v(self):
        self.ev.ev("var stop")
        self.ev.ev("false stop !")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see stop")
            actual = out.getvalue().strip()
        expected = "variable STOP"
        self.assertIn(expected, actual)

    def test_c(self):
        self.ev.ev("const k 25")
        with StringIO() as out, stdout_redirected(out):
            self.ev.ev("see k")
            actual = out.getvalue().strip()
        expected = "constant K: 25.0"
        self.assertIn(expected, actual)

    def test_bogus(self):
        with self.assertRaises(RuntimeError) as ae:
            self.ev.ev("see bogus")
        actual = str(ae.exception)
        expected = "SEE must be followed"
        self.assertIn(expected, actual)
