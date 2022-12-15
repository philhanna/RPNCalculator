import pytest
from io import StringIO

from evaluator import Evaluator
from tests import stdout_redirected


class TestArithmeticOperations:

    def setup_method(self):
        self.ev = Evaluator()

    def teardown_method(self):
        del self.ev

    def test_add(self):
        ev = self.ev
        ev.ev('2 3')
        ev.do_add()
        expected = 5
        actual = ev.pop().value
        assert actual == expected

    def test_add_by_command(self):
        ev = self.ev
        ev.ev('2 3 +')
        expected = 5
        actual = ev.pop().value
        assert actual == expected

    def test_sub(self):
        ev = self.ev
        ev.ev('3 5')
        ev.do_sub()
        expected = -2
        actual = ev.pop().value
        assert actual == expected

    def test_sub_by_command(self):
        ev = self.ev
        ev.ev('3 5 -')
        expected = -2
        actual = ev.pop().value
        assert actual == expected

    def test_mult(self):
        self.ev.ev("10 1.8 *")
        expected = 18
        actual = self.ev.pop().value
        pytest.approx(actual, expected)

    def test_div(self):
        self.ev.ev("10 1.8 /")
        expected = 5.55555555
        actual = self.ev.pop().value
        pytest.approx(actual, expected)

    def test_div_by_zero(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("10 0 /")
        expected = "divide by zero"
        actual = str(ae.value)
        assert expected in actual

    def test_increment(self):
        self.ev.ev("2 ++")
        expected = 3
        actual = self.ev.pop().value
        assert actual == expected

    def test_increment_1plus(self):
        self.ev.ev("4 1+")
        expected = 5
        actual = self.ev.pop().value
        assert actual == expected

    def test_decrement(self):
        self.ev.ev("2 --")
        expected = 1
        actual = self.ev.pop().value
        assert actual == expected

    def test_decrement_1minus(self):
        self.ev.ev("4 1-")
        expected = 3
        actual = self.ev.pop().value
        assert actual == expected

    def test_mod(self):
        self.ev.ev("14 5 %")
        expected = 4
        actual = self.ev.pop().value
        assert actual == expected

    def test_mod_div_by_zero(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("14 0 %")
        errmsg = str(ae.value)
        assert "divide by zero" in errmsg

    def test_int(self):
        self.ev.ev("7 3 / int")
        expected = 2
        actual = self.ev.pop().value
        assert actual == expected

    def test_sqrt(self):
        self.ev.ev("9 sqrt")
        expected = 3
        actual = self.ev.pop().value
        assert actual == expected

    def test_bad_sqrt(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("-3 sqrt")
        errmsg = str(ae.value)
        assert "negative" in errmsg

    def test_pow(self):
        self.ev.ev("2 3 **")
        expected = 8
        actual = self.ev.pop().value
        assert actual == expected

    def test_pow_non_integer(self):
        self.ev.ev("2 1 3 / **")
        expected = 1.259921049894873
        actual = self.ev.pop().value
        pytest.approx(expected, actual)

    def test_pow_negative_base(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("-3 2 **")
        errmsg = str(ae.value)
        assert "Cannot exponentiate" in errmsg

    def test_pow_zero_base(self):
        with pytest.raises(RuntimeError) as ae:
            self.ev.ev("0 2 **")
        errmsg = str(ae.value)
        assert "Cannot exponentiate" in errmsg

    def test_empty_stack(self):
        with StringIO() as fp, stdout_redirected(fp):
            ev = self.ev
            ev.ev('2')
            ev.do_add()
            output = fp.getvalue()
        assert "Stack empty" in output
