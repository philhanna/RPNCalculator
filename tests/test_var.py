import pytest


def test_store(ev):
    ev.ev("var amount")
    ev.ev("25 amount !")
    ev.ev("amount")
    expected = 1
    actual = ev.pop()
    assert actual == expected


def test_bad_store(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("4 -14 !")
    assert "Invalid memory reference" in str(ae.value)


def test_fetch(ev):
    ev.ev("var amount")
    ev.ev("1 3 / amount !")
    ev.ev("amount @")
    expected = .3333333333333333
    actual = ev.pop().value
    pytest.approx(expected, actual)


def test_fetch_bad(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("-3 @")
    assert "Invalid memory reference, index=-3" in str(ae.value)


def test_fetch_bad2(ev):
    with pytest.raises(RuntimeError) as ae:
        ev.ev("1000 @")
    assert "Invalid memory reference, index=1000" in str(ae.value)
