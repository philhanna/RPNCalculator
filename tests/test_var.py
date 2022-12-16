import pytest

from evaluator import Evaluator


class TestVariable:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_store(self):
        self.ev.ev("var amount")
        self.ev.ev("25 amount !")
        self.ev.ev("amount")
        expected = 1
        actual = self.ev.pop()
        assert actual == expected

    def test_bad_store(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("4 -14 !")
        assert "Invalid memory reference" in str(ae.value)

    def test_fetch(self):
        self.ev.ev("var amount")
        self.ev.ev("1 3 / amount !")
        self.ev.ev("amount @")
        expected = .3333333333333333
        actual = self.ev.pop().value
        pytest.approx(expected, actual)

    def test_fetch_bad(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("-3 @")
        assert "Invalid memory reference, index=-3" in str(ae.value)

    def test_fetch_bad2(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("1000 @")
        assert "Invalid memory reference, index=1000" in str(ae.value)
