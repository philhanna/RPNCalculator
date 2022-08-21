from io import StringIO
from unittest import TestCase

from evaluator import EVHelp, Evaluator
from tests import stdout_redirected


class TestHelp(TestCase):

    def test_help(self):
        try:
            ev = Evaluator()
            with StringIO() as fp:
                with stdout_redirected(fp):
                    ev.ev('help')
                    output = fp.getvalue()
            self.assertTrue("Reverse Polish Notation" in output)
        finally:
            del ev

    def test_overview(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                topic = None
                EVHelp(topic)
                output = fp.getvalue()
        self.assertIn("OVERVIEW:", output)

    def test_topics(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                topic = "topics"
                EVHelp(topic)
                output = fp.getvalue()
        self.assertIn("Stack functions:", output)

    def test_cos(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                topic = "cos"
                EVHelp(topic)
                output = fp.getvalue()
        self.assertIn("cos:", output)

    def test_not_found(self):
        with StringIO() as fp:
            with stdout_redirected(fp):
                topic = "bogus"
                EVHelp(topic)
                output = fp.getvalue()
        self.assertIn("bogus", output)

