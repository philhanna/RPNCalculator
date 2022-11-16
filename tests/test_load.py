import os
import tempfile
import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected

tmp = tempfile.gettempdir()


class TestLoad(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_ev_bad_load(self):
        with self.assertRaises(RuntimeError) as ae:
            self.ev.ev("load bogus")
        self.assertIn("Could not", str(ae.exception))

    def test_ev_good_load(self):
        filename = os.path.join(tmp, "file1")
        with open(filename, "w") as fp:
            print(" ", file=fp)
            print("const meaning 42", file=fp)
            print("# quit", file=fp)
        try:
            with StringIO() as fp, stdout_redirected(fp):
                self.ev.ev(f"load {filename}")
                self.ev.ev("meaning .")
                output = fp.getvalue()
            self.assertIn("42", output)
        finally:
            os.remove(filename)
