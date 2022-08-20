import sys
from io import StringIO
from unittest import TestCase
from evaluator import Evaluator
from tests import stdin_redirected, stdout_redirected


class TestRun(TestCase):

    def test_run(self):
        with StringIO() as out:
            with stdout_redirected(out):
                with StringIO("quit") as fp:
                    with stdin_redirected(fp):
                        ev = Evaluator()
                        ev.run()
                        output = out.getvalue()
        self.assertIn("ev>", output)

    def test_version(self):
        try:
            sys.argv.append("-v")
            with StringIO() as out:
                with stdout_redirected(out):
                    with StringIO("quit") as fp:
                        with stdin_redirected(fp):
                            ev = Evaluator()
                            ev.run()
                            output = out.getvalue()
            self.assertIn("Version", output)
        finally:
            sys.argv.remove("-v")

    def test_command_line_tokens(self):
        try:
            sys.argv.append("-c")
            sys.argv.append("2 3 * .")
            with StringIO() as out:
                with stdout_redirected(out):
                    with StringIO("quit") as fp:
                        with stdin_redirected(fp):
                            ev = Evaluator()
                            ev.run()
                            output = out.getvalue()
            self.assertIn("6", output)
        finally:
            sys.argv = sys.argv[:-2]
