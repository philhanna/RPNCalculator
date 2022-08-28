import io
import re
from io import StringIO
from unittest import TestCase

import evaluator
from tests import stdout_redirected


class TestDump(TestCase):

    def setUp(self) -> None:
        self.ev = evaluator.Evaluator()

    def tearDown(self) -> None:
        del self.ev

    def test_dump_stack(self):
        with StringIO() as fpout:
            with stdout_redirected(fpout):
                ev = self.ev
                ev.ev("1 5 2")
                ev.ev(".S")
                output = fpout.getvalue()
        self.assertEqual("1.0\n5.0\n2.0\n", output)

    def test_dump_functions(self):
        with StringIO() as fpout:
            with stdout_redirected(fpout):
                ev = self.ev
                ev.ev("define meaning 42")
                ev.ev(".F")
                output = fpout.getvalue()
        self.assertIsNotNone(re.search(r"FUNCTION\s+DEFINITION.*meaning\s+42", output, re.DOTALL))

    def test_dump_variables(self):
        with StringIO() as fpout:
            with stdout_redirected(fpout):
                ev = self.ev
                ev.ev("var interest")
                ev.ev("0.08 interest !")
                ev.ev("var term")
                ev.ev("30 term !")
                ev.ev(".V")
                output = fpout.getvalue()
        fp = io.StringIO(output)
        for i, line in enumerate(fp):
            tokens = line.split()
            if i == 0:
                self.assertListEqual(["VAR", "ADDR", "VALUE"], tokens)
            elif i == 1:
                self.assertListEqual(["interest", "0001", "0.08"], tokens)
            elif i == 2:
                self.assertListEqual(["term", "0002", "30.0"], tokens)
        fp.close()