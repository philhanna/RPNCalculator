# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

- Moved stack_needs decorator to `__init__.py`
- Code reformatted by PyCharm
- Prevented `import readline` from being optimized away

## [1.8.0] - 2022-10-22

### Added

- This `CHANGELOG.md`.
- `__main__.py` in package so that it can be called with `python -m evaluator`

### Changed

Refactored main body of `Evaluator` class to reduce code complexity.
Instead of a long series of `if` statements, now uses dictionaries
that map command names to handler functions:

```
full_line_commands = {
    'HELP': self.do_help,
    'H': self.do_help,
    '?': self.do_help,
    'CONST': self.do_const,
    'DEFINE': self.do_define,
    'DIGITS': self.do_digits,
    'LOAD': self.do_load,
    'SAVE': self.do_save,
    'VAR': self.do_variable,
}

commands = {
    '@': self.do_fetch,
    '!': self.do_store,
    '.': self.do_print,
    '1-': self.do_decrement,
    '--': self.do_decrement,
    '1+': self.do_increment,
    '++': self.do_increment,
    'CLEAR': self.do_clear,
    '+': self.do_add,
    '-': self.do_sub,
    '*': self.do_mult,
    '/': self.do_div,
    '.S': self.dump_stack,
    '.F': self.dump_functions,
    '.V': self.dump_variables,
    '.C': self.dump_constants,
    'DUP': self.do_dup,
    'DROP': self.do_drop,
    'SWAP': self.do_swap,
    'OVER': self.do_over,
    'ROT': self.do_rotate,
    'SQR': self.do_sqrt,
    'SQRT': self.do_sqrt,
    'SIN': self.do_sin,
    'COS': self.do_cos,
    'ATAN': self.do_atan,
    'ATAN2': self.do_atan2,
    'TAN': self.do_tan,
    'ACOS': self.do_acos,
    'ASIN': self.do_asin,
    'LOG': self.do_log,
    'LOG10': self.do_log,
    'LN': self.do_ln,
    'EXP': self.do_exp,
    'TORADIANS': self.do_to_radians,
    'TODEGREES': self.do_to_degrees,
    '%': self.do_mod,
    'MOD': self.do_mod,
    '/MOD': self.do_divmod,
    '**': self.do_pow,
    '^': self.do_pow,
    'INT': self.do_int,
    'DEPTH': self.do_depth,
    'SHELL': self.do_shell,
}
```

These are used by lookups:

```
if kwd in full_line_commands:
            full_line_commands[kwd](rest)
            return
...
commands[token]()
```

## [1.7.1] - 2022-09-19

Bug fix:

- Issue #9 - Command line -c C does not include a way to quit

## [1.7.0] - 2022-09-12

Added `/mod` (divmod) operator

## [1.6.1] - 2022-08-28

Now using [mpmath](https://mpmath.org/) for real and complex floating-point arithmetic
with arbitrary precision. This is controlled by the `digits &lt;n&gt;` command.
For example:

```
ev> 2 sqrt .
1.4142135623731
ev> digits 60
ev> 2 sqrt .
1.41421356237309504880168872420969807856967187537694807317668
```

This can be set in `.evrc` if desired.

Increased unit test coverage by adding unit tests:

- `mod` with divide by zero
- Invalid square root
- Power with non-integer
- Power with negative base
- Power with zero base
- Dump functions when none are defined
- Dump variables when none are defined
- Duplicate variable definition
- Dump constants when none are defined
- `do_shell` on Windows
- Invalid store (no variable defined)
- Invalid fetch (no variable defined)
- `digits` with an invalid argument
- Invalid token
- Dump stack

Also updated help text to include the changes

## [1.5.0] - 2022-08-20

Declared classes in `__init__.py` and added unit tests.

## [1.4.0] - 2020-06-27

Added MIT license.

## [1.3.0] - 2019-19-21

First workable version, based on the Perl version.

[Unreleased]: https://github.com/philhanna/RPNCalculator/compare/1.8.0..HEAD
[1.8.0]: https://github.com/philhanna/RPNCalculator/compare/1.7.1..1.8.0
[1.7.1]: https://github.com/philhanna/RPNCalculator/compare/1.7.0..1.7.1
[1.7.0]: https://github.com/philhanna/RPNCalculator/compare/1.6.1..1.7.0
[1.6.1]: https://github.com/philhanna/RPNCalculator/compare/1.5.0..1.6.1
[1.5.0]: https://github.com/philhanna/RPNCalculator/compare/1.4.0..1.5.0
[1.4.0]: https://github.com/philhanna/RPNCalculator/compare/1.3.0..1.4.0
[1.3.0]: https://github.com/philhanna/RPNCalculator/compare/81bb24..1.4.0
