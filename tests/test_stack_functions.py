from evaluator import NumberEntry


def test_clear(ev):
    ev.ev("1 2 3")
    assert len(ev.stack) == 3
    ev.ev("clear")
    assert len(ev.stack) == 0


def test_depth(ev):
    ev.ev("45 11 depth")
    expected = 2
    actual = ev.pop().value
    assert actual == expected


def test_drop(ev):
    ev.ev("1 2 3 drop")
    assert ev.stack == [NumberEntry(1), NumberEntry(2)]


def test_dup(ev):
    ev.ev("5 dup")
    assert ev.stack == [NumberEntry(5), NumberEntry(5)]


def test_over(ev):
    ev.ev("1 2 over")
    assert ev.stack == [NumberEntry(1), NumberEntry(2), NumberEntry(1)]


def test_rot(ev):
    ev.ev("10 20 30 rot")
    assert ev.stack == [NumberEntry(20), NumberEntry(30), NumberEntry(10)]


def test_swap(ev):
    ev.ev("10 20 30 swap")
    assert ev.stack == [NumberEntry(10), NumberEntry(30), NumberEntry(20)]
