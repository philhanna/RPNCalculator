# Architecture

This document describes the internal design of RPNCalculator for developers who want to understand or modify the codebase.

## Package layout

```
evaluator/
├── __init__.py       # Exports, @stack_needs decorator, EXIT sentinel
├── __main__.py       # CLI entry point (argparse)
├── ev.py             # Evaluator class — the core engine
├── ev_help.py        # EVHelp class — built-in help text
└── stack_entry.py    # Stack value types: NumberEntry, BooleanEntry
tests/
└── test_*.py         # One file per command group
```

## The stack model

All values on the stack are instances of `StackEntry` (defined in `stack_entry.py`). There are two concrete subtypes:

| Type | Wraps | Used for |
|---|---|---|
| `NumberEntry` | `mpmath.mpf` | All numeric values |
| `BooleanEntry` | `bool` | Results of comparisons and logic ops |

`mpmath.mpf` provides arbitrary-precision arithmetic. The working precision is controlled by `mpmath.mp.dps` (decimal places), changed via the `DIGITS` command.

The stack itself is a plain Python `list` (`Evaluator.stack`). `push()` appends; `pop()` removes from the end; `peek()` reads without removing.

## Evaluator state

`Evaluator.__init__` sets up all mutable state:

| Attribute | Type | Purpose |
|---|---|---|
| `stack` | `list[StackEntry]` | The evaluation stack |
| `constant` | `dict[str, StackEntry]` | Named constants (e.g. `CONST TWO 2`) |
| `function` | `dict[str, str]` | User-defined functions stored as raw strings |
| `variable` | `dict[str, StackEntry]` | Named variables (e.g. `VAR X`) |
| `memory` | `list` | 1-indexed memory cells; index 0 unused; `-1` signals uninitialised |
| `debug` | `bool` | When `True`, `RuntimeError` is re-raised instead of printed |

## Token dispatch in `ev(command)`

`ev()` in [ev.py](../evaluator/ev.py) is the heart of the interpreter. Execution follows this order for each input line:

```
input line
  │
  ├─ starts with '#'? → skip (comment)
  │
  ├─ first token in full_line_commands?
  │     e.g. DEFINE, CONST, LOAD, SAVE, HELP, VAR, SEE, DIGITS
  │     → call handler(rest_of_line) and return
  │
  └─ iterate over tokens:
        ├─ Q / QUIT / EXIT → return EXIT sentinel
        ├─ numeric literal  → push NumberEntry
        ├─ name in variable → push its value
        ├─ name in constant → push its value
        ├─ name in function → re-evaluate the stored string via self.ev()
        ├─ 'PI'             → push NumberEntry(pi)
        ├─ 'E'              → push NumberEntry(e)
        ├─ name in commands → call the corresponding method
        └─ anything else    → raise RuntimeError("Unrecognized token")
```

`full_line_commands` handlers receive the remainder of the line as a string. Token-level `commands` handlers take no arguments — they read from and write to the stack directly.

## User-defined functions

Functions are stored in `Evaluator.function` as raw strings:

```
DEFINE DOUBLE DUP +
```

stores `{"DOUBLE": "DUP +"}`. Calling `DOUBLE` re-enters `self.ev("DUP +")`. This means functions support recursion naturally, because `ev()` can call itself.

## The `@stack_needs(n)` decorator

Defined in `__init__.py`. Wraps a method so that it checks `len(self.stack) >= n` before executing. If the check fails it prints `"Stack empty"` and returns early (or re-raises in debug mode). Every operator method that consumes stack values should use this decorator.

```python
@stack_needs(2)
def do_add(self):
    f2 = self.pop().value
    f1 = self.pop().value
    self.push(NumberEntry(f1 + f2))
```

## Error handling

- `RuntimeError` is the standard mechanism for domain errors (divide by zero, bad argument, etc.).
- In production (`debug=False`) these are caught in `ev()` and printed.
- In debug mode (`debug=True`, default in tests) they propagate, allowing `pytest.raises` to catch them.

## Profile and LOAD/SAVE

On startup `run()` calls `load_profile()`, which looks for `~/.evrc` and feeds it through `ev()`. `SAVE` serialises functions, constants, or variables to a file; `LOAD` reads them back the same way.

## Continuation lines and comments

- A line ending with `\` is joined to the next input line before parsing.
- Anything after `#` on a line is ignored.

Both are handled in the `run()` REPL loop before `ev()` is called.
