# Contributing to RPNCalculator

This document is the starting point for new contributors. It covers environment setup, workflow, and where to look for more detail.

## Prerequisites

- Python 3.x
- `pip`

## Setting up a development environment

```bash
# Clone the repo
git clone https://github.com/philhanna/RPNCalculator
cd RPNCalculator

# (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies and the package in editable mode
pip install -r requirements.txt
pip install -e .
```

## Running the calculator

```bash
# Interactive REPL
python -m evaluator

# Run a one-liner non-interactively
python -m evaluator -c "2 3 + ."

# Skip loading ~/.evrc (useful during development)
python -m evaluator --noprofile
```

There is also a shell wrapper `./ev` in the project root.

## Running the tests

```bash
# Run the full test suite
pytest

# Run a single test file
pytest tests/test_arithmetic_operations.py

# Run a single test by name
pytest tests/test_arithmetic_operations.py::test_addition
```

See [testing.md](testing.md) for conventions and patterns.

## Typical contribution workflows

| Task | Where to look |
|---|---|
| Add a new operator or command | [adding-commands.md](adding-commands.md) |
| Add a help topic | [adding-help.md](adding-help.md) |
| Understand the internals | [architecture.md](architecture.md) |

## Coding conventions

- <!-- TODO: document style guide, e.g. PEP 8, formatter, linter settings -->
- Use `mpmath.mpf` for all numeric values; never use raw `float` on the stack.
- Decorate stack-consuming methods with `@stack_needs(n)` rather than checking depth manually.
- Error messages should be defined in `Evaluator.MSG` and raised as `RuntimeError`.

## Submitting a pull request

<!-- TODO: describe branch naming, PR checklist, review process -->
