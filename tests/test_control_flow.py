import pytest


# ── IF / ELSE / THEN ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("cmd,expected_output", [
    # true branch taken
    ("true  IF 42 . THEN", "42"),
    # false branch skipped (no output)
    ("false IF 42 . THEN", ""),
    # ELSE branch taken when false
    ("false IF 1 . ELSE 2 . THEN", "2"),
    # IF branch taken, ELSE skipped
    ("true  IF 1 . ELSE 2 . THEN", "1"),
])
def test_if_else_then_output(ev, cmd, expected_output, capsys):
    ev.ev(cmd)
    out = capsys.readouterr().out
    assert expected_output in out


def test_if_leaves_stack_clean(ev):
    ev.ev("true IF 99 THEN")
    assert ev.pop().value == 99
    assert len(ev.stack) == 0


def test_if_false_stack_unchanged(ev):
    ev.ev("false IF 99 THEN")
    assert len(ev.stack) == 0


def test_if_else_true_branch_stack(ev):
    ev.ev("true IF 10 ELSE 20 THEN")
    assert ev.pop().value == 10


def test_if_else_false_branch_stack(ev):
    ev.ev("false IF 10 ELSE 20 THEN")
    assert ev.pop().value == 20


def test_nested_if_outer_false(ev):
    # outer IF takes false → ELSE branch → 3
    ev.ev("false IF true IF 1 ELSE 2 THEN ELSE 3 THEN")
    assert ev.pop().value == 3


def test_nested_if_outer_true_inner_true(ev):
    # outer IF takes true → inner IF takes true → 1
    ev.ev("true IF true IF 1 ELSE 2 THEN ELSE 3 THEN")
    assert ev.pop().value == 1


def test_nested_if_outer_true_inner_false(ev):
    # outer IF takes true → inner IF takes false → 2
    ev.ev("true IF false IF 1 ELSE 2 THEN ELSE 3 THEN")
    assert ev.pop().value == 2


def test_if_inside_define(ev, capsys):
    ev.ev("define abs-val dup 0 < IF -1 * THEN")
    ev.ev("-5 abs-val .")
    out = capsys.readouterr().out
    assert "5" in out


def test_if_else_inside_define(ev, capsys):
    ev.ev("define sign dup 0 > IF drop 1 ELSE drop -1 THEN")
    ev.ev("7  sign .")
    out = capsys.readouterr().out.strip()
    assert "1" in out
    ev.ev("-3 sign .")
    out = capsys.readouterr().out.strip()
    assert "-1" in out


# ── BEGIN / WHILE / REPEAT ───────────────────────────────────────────────────

def test_loop_counts_down(ev, capsys):
    # count from 3 down to 1, printing each value; exits when 0
    ev.ev("3 BEGIN dup . 1 - dup 0 > WHILE REPEAT drop")
    out = capsys.readouterr().out
    assert "3" in out
    assert "2" in out
    assert "1" in out
    assert len(ev.stack) == 0


def test_loop_zero_iterations(ev):
    # flag already false → body runs once then exits immediately after WHILE check
    ev.ev("0 BEGIN 1 - dup 0 > WHILE REPEAT drop")
    assert len(ev.stack) == 0


def test_loop_inside_define(ev, capsys):
    ev.ev("define countdown BEGIN dup . 1 - dup 0 > WHILE REPEAT drop")
    ev.ev("3 countdown")
    out = capsys.readouterr().out
    assert "3" in out
    assert "2" in out
    assert "1" in out


def test_loop_accumulates(ev):
    # sum 1..5 = 15.  Stack layout: ( n acc )
    # BEGIN..WHILE checks n>0; WHILE..REPEAT adds n to acc then decrements n.
    ev.ev("5 0 BEGIN over 0 > WHILE over + swap 1 - swap REPEAT swap drop")
    assert ev.pop().value == 15


# ── Error cases ───────────────────────────────────────────────────────────────

def test_if_without_then(ev):
    with pytest.raises(RuntimeError, match="IF without matching THEN"):
        ev.ev("true IF 1")


def test_begin_without_repeat(ev):
    with pytest.raises(RuntimeError, match="BEGIN without matching REPEAT"):
        ev.ev("1 BEGIN dup 0 > WHILE 1 -")


def test_begin_without_while(ev):
    with pytest.raises(RuntimeError, match="missing WHILE"):
        ev.ev("1 BEGIN 1 - REPEAT")


def test_unexpected_then(ev):
    with pytest.raises(RuntimeError, match="Unexpected token"):
        ev.ev("THEN")


def test_unexpected_repeat(ev):
    with pytest.raises(RuntimeError, match="Unexpected token"):
        ev.ev("REPEAT")
