import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestDefine(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_ev_bad_define(self):
        with self.assertRaises(RuntimeError) as ae:
            self.ev.ev("define bogus")
        self.assertIn("No function", str(ae.exception))

    def test_ev_good_define(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("define double dup 2 *")
            self.ev.ev("7 double .")
            output = fp.getvalue()
        self.assertIn("14", output)
