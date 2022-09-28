import builtins
import os
import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch

from evaluator import Evaluator
from tests import stdin_redirected, stdout_redirected


class TestRun(TestCase):

    def test_run(self):
        with (StringIO() as out,
              stdout_redirected(out),
              StringIO("quit") as fp,
              stdin_redirected(fp)):
            ev = Evaluator()
            ev.run()
            output = out.getvalue()
        self.assertIn("ev>", output)

    def test_version(self):
        try:
            sys.argv.append("-v")
            with (StringIO() as out,
                  stdout_redirected(out),
                  StringIO("quit") as fp,
                  stdin_redirected(fp)):
                ev = Evaluator()
                ev.run()
                output = out.getvalue()
            self.assertIn("Version", output)
        finally:
            sys.argv.remove("-v")

    def test_command_line_tokens(self):
        try:
            sys.argv.append("-c")
            sys.argv.append("2 3 * . quit")
            with StringIO() as out, stdout_redirected(out):
                with patch.object(builtins, "input", return_value="EXIT"):
                    ev = Evaluator()
                    ev.run()
                output = out.getvalue()
            self.assertIn("6", output)
        finally:
            sys.argv = sys.argv[:-2]

    def test_ev_no_command(self):
        ev = Evaluator()
        rc = ev.ev(None)
        self.assertIsNone(rc)

    def test_ev_comment_command(self):
        ev = Evaluator()
        rc = ev.ev("# DEFINE")
        self.assertIsNone(rc)

    def test_do_shell(self):
        os.system = MagicMock()
        ev = Evaluator()
        ev.ev("shell")
        os.system.assert_called_with("/usr/bin/gnome-terminal")

    def test_do_shell_windows(self):
        os.system = MagicMock()
        sys.platform = MagicMock(return_value="windows")
        ev = Evaluator()
        ev.ev("shell")
        os.system.assert_called_with("cmd /k")

    def test_bad_token(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = Evaluator()
            ev.ev("bogus")
            output = fp.getvalue()
        self.assertIn("Unrecognized token BOGUS", output)
