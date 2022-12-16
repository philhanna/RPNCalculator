from evaluator import Evaluator, NumberEntry


class TestStackFunctions:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_clear(self):
        self.ev.ev("1 2 3")
        assert len(self.ev.stack) == 3
        self.ev.ev("clear")
        assert len(self.ev.stack) == 0

    def test_depth(self):
        self.ev.ev("45 11 depth")
        expected = 2
        actual = self.ev.pop().value
        assert actual == expected

    def test_drop(self):
        self.ev.ev("1 2 3 drop")
        assert self.ev.stack == [NumberEntry(1), NumberEntry(2)]

    def test_dup(self):
        self.ev.ev("5 dup")
        assert self.ev.stack == [NumberEntry(5), NumberEntry(5)]

    def test_over(self):
        self.ev.ev("1 2 over")
        assert self.ev.stack == [NumberEntry(1), NumberEntry(2), NumberEntry(1)]

    def test_rot(self):
        self.ev.ev("10 20 30 rot")
        assert self.ev.stack == [NumberEntry(20), NumberEntry(30), NumberEntry(10)]

    def test_swap(self):
        self.ev.ev("10 20 30 swap")
        assert self.ev.stack == [NumberEntry(10), NumberEntry(30), NumberEntry(20)]

