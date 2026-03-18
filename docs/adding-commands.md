# Adding a New Command or Operator

This guide walks through adding a new token-level command to the calculator. As a worked example, imagine adding a `SQUARE` command that squares the top of the stack.

## 1. Implement the handler method in `Evaluator`

All operator methods live in [evaluator/ev.py](../evaluator/ev.py) on the `Evaluator` class. Methods follow these conventions:

- Decorated with `@stack_needs(n)` where `n` is how many values they consume.
- Pop inputs with `self.pop().value` (gets the underlying `mpmath.mpf` or `bool`).
- Push results with `self.push(NumberEntry(...))` or `self.push(BooleanEntry(...))`.
- Raise `RuntimeError` for domain errors, using a message from `Evaluator.MSG`.

```python
@stack_needs(1)
def do_square(self):
    x = self.pop().value
    result = NumberEntry(x * x)
    self.push(result)
```

## 2. Register the command in the dispatch table

Inside `ev()`, find the `commands` dict and add an entry:

```python
commands = {
    ...
    'SQUARE': self.do_square,
    ...
}
```

The key is the uppercased token users will type. `ev()` uppercases all tokens before lookup, so the user can type `square`, `SQUARE`, or `Square`.

## 3. Add a help entry

Add an entry to the `helptext` dict in [evaluator/ev_help.py](../evaluator/ev_help.py):

```python
"square": """
square:  Pops x from the stack and pushes x².
""",
```

See [adding-help.md](adding-help.md) for full details.

## 4. Write tests

Add a test in the appropriate file under `tests/`, or create a new file if the command doesn't fit an existing group. See [testing.md](testing.md) for patterns.

```python
@pytest.mark.parametrize("test_input,expected", [
    ("3 square", 9),
    ("0 square", 0),
    ("-4 square", 16),
])
def test_square(ev, test_input, expected):
    ev.ev(test_input)
    assert ev.pop().value == expected
```

## Full-line commands vs. token commands

The guide above covers **token-level commands** — operators that are dispatched in a loop alongside other tokens on the same line.

**Full-line commands** (`DEFINE`, `CONST`, `LOAD`, `SAVE`, `HELP`, `VAR`, `SEE`, `DIGITS`) consume the rest of the input line as a string argument. To add one:

1. Implement `do_mycommand(self, line: str)` — `line` is everything after the keyword.
2. Register it in the `full_line_commands` dict at the top of `ev()`.

```python
full_line_commands = {
    ...
    'MYCOMMAND': self.do_mycommand,
    ...
}
```

## Checklist

- [ ] Handler method added to `Evaluator` in `ev.py`
- [ ] Entry added to `commands` (or `full_line_commands`) in `ev()`
- [ ] Help text added in `ev_help.py`
- [ ] Tests written and passing (`pytest`)
