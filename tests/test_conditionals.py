from unittest import TestCase

import evaluator


class TestConditionals(TestCase):

    def setUp(self) -> None:
        self.ev = evaluator.Evaluator()

    def tearDown(self) -> None:
        del self.ev

    def test_IF_outside_of_definition(self):
        """Should fail, because I'm only allowing IF-THEN-ELSE inside a function definition"""
        ev = self.ev
        with self.assertRaises(RuntimeError) as ae:
            ev.ev("2 sqrt 1 > if")
        errmsg = str(ae.exception)
        self.assertIn("Unrecognized token", errmsg)
