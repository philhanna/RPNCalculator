import os
import tempfile
import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestLoad(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()
        self.tmp = tempfile.gettempdir()

    def tearDown(self):
        del self.ev

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
