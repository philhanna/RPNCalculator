Source: [https://github.com/philhanna/RPNCalculator](https://github.com/philhanna/RPNCalculator)

# OVERVIEW

***ev*** is an interactive programmable RPN calculator.  (Type `help RPN`
for details about Reverse Polish Notation).  It reads blank-delimited 
tokens from the input stream and interprets them one at a time using 
a syntax inspired by the FORTH programming language.  Anything following 
a '#' on an input line is considered a comment.

Besides simple calculations, ev supports variables, constants, and 
function definitions.  It also allows save and restore operations.

For help on an individual topic, type `help` *&lt;topic name&gt;*.

To see a list of topics, type `help topics`.

To exit from ev, type `q`;

## Installation and setup

After cloning the project from GitHub, run the command:
```bash
cd <install_dir>
pip install .
```
Then copy the mainline `ev` to a directory in your path.

## Commands by category
* Arithmetic operations:   `+`, `-`, `*`, `/`, `%`, `**`, `1+`, `1-`, `int`, `sqrt`
* Commands:                `help`, `load`, `quit`, `save`, `shell`
* Configuration:           `profile`
* Constants:               `e`, `pi`
* Conversion functions:    `toDegrees`, `toRadians`
* Declaratives:            `const`, `define`, `format`, `var`
* Log functions:           `exp`, `ln`, `log`
* Memory operations:       `@`, `!`
* Print functions:         `.`, `.c`, `.f`, `.s`, `.v`, `fmtstr`
* Stack functions:         `clear`, `depth`, `drop`, `dup`, `over`, `rot`, `swap`
* Trigonometric functions: `acos`, `asin`, `atan`, `atan2`, `cos`, `sin`, `tan`

## Reverse Polish Notation
Reverse Polish Notation (RPN) is a syntax for writing arithmetic expressions in which operands are pushed on a stack and the operator follows the operands.  For example,

```
2 + 3
```
is written
```
2 3 +
```
When this expression is evaluated, the two operands are popped from the stack, the sum is calculated, and the result 5 is pushed on the stack

RPN makes parentheses unnecessary:

```
(1 + 5) * (3 - 4)
```
is written
```
1 5 + 3 4 - *
```

It also makes rules about operator precedence unnecessary, since operators always take their operands from the top of the stack and push their results onto the stack.

While RPN may take a little getting used to, it is quite compact and straightforward.  It is the standard notation used by Hewlett Packard calculators.
