import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestConst(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_ev_bad_const(self):
        with self.assertRaises(RuntimeError) as ae:
            self.ev.ev("const bogus")
        self.assertIn("Invalid syntax", str(ae.exception))

    def test_ev_good_const(self):
        self.ev.ev("const meaning-of-the-universe 42")
        self.ev.ev("meaning-of-the-universe 42 =")

    def test_ev_bad_constp(self):
        with self.assertRaises(RuntimeError) as ae:
            self.ev.ev("const bogus 47 45 ")
        self.assertIn("Invalid syntax", str(ae.exception))

    def test_ev_good_constp(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("const meaning-of-the-universe 21 2 *")
            self.ev.ev("meaning-of-the-universe .")
            output = fp.getvalue()
        self.assertIn("42", output)
