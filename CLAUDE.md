# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install .

# Run all tests
pytest

# Run a single test file
pytest evaluator/tests/test_arithmetic_operations.py

# Run a specific test by name
pytest evaluator/tests/test_arithmetic_operations.py::test_addition

# Run the calculator interactively
python -m evaluator
# or via the shell wrapper:
./ev

# Execute commands non-interactively
python -m evaluator -c "2 3 + ."
```

## Architecture

The package lives entirely in `evaluator/` with five source files:

- **`ev.py`** — The `Evaluator` class (~860 lines). This is the core engine. `run()` starts the REPL and loads `~/.evrc`. `ev(command)` tokenizes and dispatches each line. Command routing uses two dictionaries: `full_line_commands` (for commands that consume the rest of the line, e.g. `DEFINE`, `CONST`, `LOAD`) and `commands` (token-level operations for arithmetic, stack manipulation, math functions, etc.).

- **`stack_entry.py`** — Two stack value types: `NumberEntry` (wraps `mpmath.mpf` for arbitrary precision) and `BooleanEntry` (wraps `bool`). All values on the stack are one of these.

- **`__init__.py`** — Exports `EXIT` sentinel, `get_version()`, and the `@stack_needs(n)` decorator that validates minimum stack depth before a method executes.

- **`ev_help.py`** — `EVHelp` class with a static `helptext` dict (~50 topics) used by `do_help()`.

- **`__main__.py`** — Argparse CLI. Flags: `-v` (version), `-c <cmds>` (run commands before REPL), `--noprofile` (skip `~/.evrc`).

### Key design details

- **User-defined functions** are stored as strings in `Evaluator.function` and re-evaluated via `self.ev()`, which supports recursion.
- **Precision** is controlled via `do_digits()` and stored in `mpmath.mp.dps`.
- **Memory** is a 1-indexed list; index `-1` signals uninitialized.
- **Error handling**: `@stack_needs(n)` prints an error and returns early in production; in debug mode it raises. `RuntimeError` is raised for invalid operations.
- **Continuation lines** end with `\`; comments begin with `#`.

### Tests

Tests live in `evaluator/tests/`. `conftest.py` provides a single `ev` fixture that creates a fresh `Evaluator()` per test. Tests use `@pytest.mark.parametrize` heavily. Use `pytest.approx()` for floating-point comparisons.
