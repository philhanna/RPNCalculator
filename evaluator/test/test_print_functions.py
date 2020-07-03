import math
import unittest

from evaluator.Evaluator import Evaluator


class TestPrintFunctions(unittest.TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_log5(self):
        self.ev.ev('format "%0.5f"')
        self.ev.ev('2 log ')
        x = self.ev.pop()
        actual = self.ev.format_value(x)
        expected = "%0.5f" % (math.log10(2))
        self.assertEqual(expected, actual)

    def test_print_hex(self):
        self.ev.ev('format "0x%04x"')
        self.ev.ev('50')
        x = self.ev.pop()
        actual = self.ev.format_value(x)
        expected = "0x0032"
        self.assertEqual(expected, actual)

        self.ev.ev('depth')
        actual = self.ev.pop()
        expected = 0
        self.assertEqual(expected, actual)
