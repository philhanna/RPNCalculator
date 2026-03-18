# Testing

Tests live in the top-level `tests/` directory. There is one file per logical group of commands.

## Running tests

```bash
# Full suite
pytest

# Single file
pytest tests/test_arithmetic_operations.py

# Single test
pytest tests/test_arithmetic_operations.py::test_addition

# Verbose output
pytest -v
```

## The `ev` fixture

`tests/conftest.py` provides a single fixture that every test uses:

```python
@pytest.fixture
def ev():
    return Evaluator()
```

This creates a **fresh `Evaluator` instance for each test**, so tests are fully isolated — stack, constants, functions, and variables all start empty. The constructor defaults to `debug=True`, which means `RuntimeError` is re-raised rather than printed, making it testable with `pytest.raises`.

## Common test patterns

### Evaluate a command string, check the top of the stack

The most common pattern. Suitable for anything that pushes a result.

```python
@pytest.mark.parametrize("test_input,expected", [
    ("2 3 +", 5),
    ("10 1.8 *", approx(18)),
])
def test_by_command(ev, test_input, expected):
    ev.ev(test_input)
    assert ev.pop().value == expected
```

Use `pytest.approx()` for floating-point results to avoid precision-related failures.

### Call a method directly

Useful when you want to test a specific `do_*` method in isolation.

```python
def test_operation(ev, test_input, fname, expected):
    ev.ev(test_input)          # push operands
    exec(f"ev.{fname}()")      # call the method
    assert ev.pop().value == expected
```

### Expect a RuntimeError

For invalid operations (divide by zero, bad argument, etc.). Note that `debug=True` is required for errors to propagate — the default fixture satisfies this.

```python
@pytest.mark.parametrize("test_input,errmsg", [
    ("10 0 /", "divide by zero"),
    ("-3 sqrt", "negative"),
])
def tests_with_errors(ev, test_input, errmsg):
    with pytest.raises(RuntimeError) as ae:
        ev.ev(test_input)
    assert errmsg in str(ae.value)
```

### Expect a printed error (stack underflow)

Stack underflow prints rather than raising (in production mode). To test it, use `capsys`:

```python
def test_empty_stack(ev, capsys):
    ev.ev("2")
    ev.do_add()
    captured = capsys.readouterr()
    assert "Stack empty" in captured.out
```

Note: the `ev` fixture sets `debug=True`, but `@stack_needs` prints and returns early regardless of the debug flag when the stack is too shallow.

### Check printed output

For commands like `.` (print), `.S` (dump stack), use `capsys`:

```python
def test_print(ev, capsys):
    ev.ev("42 .")
    captured = capsys.readouterr()
    assert "42" in captured.out
```

## File naming

| File | Commands covered |
|---|---|
| `test_arithmetic_operations.py` | `+ - * / % ** sqrt abs fact` and increment/decrement |
| `test_boolean.py` | `> < = != >= <= and or not xor true false` |
| `test_const.py` | `CONST`, `.C` |
| `test_define.py` | `DEFINE`, `.F`, user-defined functions |
| `test_digits.py` | `DIGITS` |
| `test_dump.py` | `.S`, `.F`, `.V`, `.C` |
| `test_help.py` | `HELP` / `H` / `?` |
| `test_load.py` | `LOAD` |
| `test_log_functions.py` | `LOG`, `LN`, `EXP` |
| `test_save.py` | `SAVE` |
| `test_see.py` | `SEE` |
| `test_stack_functions.py` | `DUP DROP SWAP OVER ROT CLEAR DEPTH` |
| `test_trigonometric_functions.py` | `SIN COS TAN ASIN ACOS ATAN ATAN2` |
| `test_var.py` | `VAR`, `@`, `!`, `.V` |

When adding tests for a new command, add them to the most relevant existing file. Create a new file only if the command group doesn't fit anywhere.
