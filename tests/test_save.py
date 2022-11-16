import os
import tempfile
import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected

tmp = tempfile.gettempdir()


class TestSave(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()
        self.tmp = tempfile.gettempdir()

    def tearDown(self):
        del self.ev

    def test_ev_save_no_filename(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("const meaning 42")
            self.ev.ev(f"save")
            output = fp.getvalue()
        self.assertIn("No file name", output)

    def test_ev_good_save(self):
        filename = os.path.join(tmp, "good_save")
        try:
            with StringIO() as fp, stdout_redirected(fp):
                self.ev.ev("const meaning 42")
                self.ev.ev("var addr")
                self.ev.ev("7500 addr !")
                self.ev.ev("define double dup 2 *")
                self.ev.ev(f"save {filename}")
                output = fp.getvalue()
            self.assertIn("saved to", output)
        finally:
            """ os.remove(filename) """
