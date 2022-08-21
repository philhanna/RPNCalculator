import os
import unittest
import tempfile
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

    def test_ev_bad_define(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("define bogus")
                output = fp.getvalue()
        self.assertIn("No function", output)

    def test_ev_good_define(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("define double dup 2 *")
                self.ev.ev("7 double .")
                output = fp.getvalue()
        self.assertIn("14", output)

    def test_ev_bad_load(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("load bogus")
                output = fp.getvalue()
        self.assertIn("Could not", output)

    def test_ev_good_load(self):
        _, filename = tempfile.mkstemp()
        with open(filename, "w") as fp:
            print(" ", file=fp)
            print("const meaning 42", file=fp)
            print("# quit", file=fp)
        try:
            with StringIO() as fp:
                with stdout_redirected(fp):
                    self.ev.ev(f"load {filename}")
                    self.ev.ev("meaning .")
                    output = fp.getvalue()
            self.assertIn("42", output)
        finally:
            os.remove(filename)