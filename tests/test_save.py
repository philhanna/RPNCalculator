import os
import tempfile
import unittest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestSave(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()
        self.tmp = tempfile.gettempdir()

    def tearDown(self):
        del self.ev

    def test_ev_save_no_filename(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                self.ev.ev("const meaning 42")
                self.ev.ev(f"save")
                output = fp.getvalue()
        self.assertIn("No file name", output)

    def test_ev_good_save(self):
        _, filename = tempfile.mkstemp()
        try:
            with StringIO() as fp:
                with stdout_redirected(fp):
                    self.ev.ev("const meaning 42")
                    self.ev.ev("var foo")
                    self.ev.ev("define double dup 2 *")
                    self.ev.ev(f"save {filename}")
                    output = fp.getvalue()
        finally:
            os.remove(filename)