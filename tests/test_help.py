from io import StringIO
from unittest import TestCase

from evaluator import EVHelp, Evaluator
from tests import stdout_redirected


class TestHelp(TestCase):

    def test_help(self):
        try:
            ev = Evaluator()
            with StringIO() as fp, stdout_redirected(fp):
                ev.ev('help')
                output = fp.getvalue()
            self.assertTrue("Reverse Polish Notation" in output)
        finally:
            del ev

    def test_overview(self):
        topic = None
        with StringIO() as fp, stdout_redirected(fp):
            EVHelp(topic)
            output = fp.getvalue()
        self.assertIn("OVERVIEW:", output)

    def test_topics(self):
        topic = "topics"
        with StringIO() as fp, stdout_redirected(fp):
            EVHelp(topic)
            output = fp.getvalue()
        self.assertIn("Stack functions:", output)

    def test_cos(self):
        topic = "cos"
        with StringIO() as fp, stdout_redirected(fp):
            EVHelp(topic)
            output = fp.getvalue()
        self.assertIn("cos:", output)

    def test_not_found(self):
        topic = "bogus"
        with StringIO() as fp, stdout_redirected(fp):
            EVHelp(topic)
            output = fp.getvalue()
        self.assertIn("bogus", output)
