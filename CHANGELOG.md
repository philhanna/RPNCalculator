## Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

### Table of contents

- [Version 1.7.0 - 2022/09/12](#version-170---20220912)
- [Version 1.6.1 - 2022/08/28](#version-161---20220828)
- [Version 1.5.0 - 2022/08/20](#version-150---20220820)
- [Version 1.4.0 - 2020/06/27](#version-140---20200627)
- [Version 1.3.0 - 2019/19/21](#version-130---20191921)

### Version 1.7.0 - 2022/09/12

Added `/mod` (divmod) operator

### Version 1.6.1 - 2022/08/28

Now using [mpmath](https://mpmath.org/) for real and complex floating-point arithmetic
with arbitrary precision.  This is controlled by the `digits &lt;n&gt;` command.
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


### Version 1.5.0 - 2022/08/20

Declared classes in `__init__.py` and added unit tests.

### Version 1.4.0 - 2020/06/27

Added MIT license.

### Version 1.3.0 - 2019/19/21

First workable version, based on the Perl version.
