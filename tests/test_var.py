from io import StringIO
from unittest import TestCase

from evaluator import Evaluator
from tests import stdout_redirected


class TestVariable(TestCase):

    def setUp(self):
        self.ev = Evaluator()

    def tearDown(self):
        del self.ev

    def test_store(self):
        self.ev.ev("var amount")
        self.ev.ev("25 amount !")
        self.ev.ev("amount")
        expected = 1
        actual = self.ev.pop()
        self.assertEqual(expected, actual)

    def test_bad_store(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("4 -14 !")
            output = fp.getvalue()
        self.assertIn("Invalid memory reference", output)

    def test_fetch(self):
        self.ev.ev("var amount")
        self.ev.ev("1 3 / amount !")
        self.ev.ev("amount @")
        expected = .3333333333333333
        actual = self.ev.pop()
        self.assertAlmostEqual(expected, actual)

    def test_fetch_bad(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("-3 @")
            output = fp.getvalue()
        self.assertIn("Invalid memory reference, index=-3", output)

    def test_fetch_bad2(self):
        with StringIO() as fp, stdout_redirected(fp):
            self.ev.ev("1000 @")
            output = fp.getvalue()
        self.assertIn("Invalid memory reference, index=1000", output)
