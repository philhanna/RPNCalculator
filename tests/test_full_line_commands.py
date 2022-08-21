import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestFullLineCommands(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_help(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev('help')
                output = fp.getvalue()
        self.assertTrue("Reverse Polish Notation" in output)

    def test_ev_bad_const(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("const bogus")
                output = fp.getvalue()
        self.assertIn("Invalid syntax", output)

    def test_ev_good_const(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("const meaning-of-the-universe 42")
                self.ev.ev("meaning-of-the-universe .")
                output = fp.getvalue()
        self.assertIn("42", output)

    def test_ev_bad_constp(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("const bogus 47 45 ")
                output = fp.getvalue()
        self.assertIn("Invalid syntax", output)

    def test_ev_good_constp(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("const meaning-of-the-universe 21 2 *")
                self.ev.ev("meaning-of-the-universe .")
                output = fp.getvalue()
        self.assertIn("42", output)