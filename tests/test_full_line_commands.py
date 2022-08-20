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
