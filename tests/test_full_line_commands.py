import os
import unittest
import tempfile
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestFullLineCommands(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()
        self.tmp = tempfile.gettempdir()

    def tearDown(self):
        del self.ev
