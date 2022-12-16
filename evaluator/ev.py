import readline
import subprocess
import sys
from pathlib import Path

import pandas as pd
from mpmath import acos, asin, atan, atan2, cos, exp, ln, log10, pi, power, sin, sqrt, tan, mp, mpf

from evaluator import stack_needs, EXIT, NumberEntry, BooleanEntry, FALSE, TRUE, StackEntry
from evaluator.ev_help import EVHelp

assert readline is not None  # Do not delete this line - needed to
# prevent "import readline" from being optimized away


class Evaluator:
    """ Interactive RPN calulator """

    #   Constants
    PROMPT = "ev> "
    CONTINUATION_PROMPT = "(ev)> "

    #   Error messages
    MSG = {
        "BAD_CONST": "Invalid syntax - should be 'const <name> <value>'",
        "BAD_CONSTP": "Invalid syntax - should be 'const <name> <statements>'",
        "BAD_DIGITS": "'{}' is not a valid value for digits",
        "BAD_FORMAT": "Invalid format string  Should be printf-style.",
        "BAD_LOG": "Cannot take the log of a non-positive number",
        "BAD_OPEN": "Could not open file {}",
        "BAD_SEE": "SEE must be followed by a function name, a constant name, or a variable name",
        "BAD_SQRT": "Cannot take the square root of the negative number {}",
        "BAD_TOKEN": "Unrecognized token {}",
        "BAD_VARNUM": "Invalid memory reference, index={}",
        "CON_SAVED": "{} constant definitions saved to {}",
        "DIVIDE_BY_0": "Cannot divide by zero",
        "EMPTY": "Stack empty",
        "FUN_SAVED": "{} function definitions saved to {}",
        "INFINITY": "Number too large to represent",
        "NEGATIVE_BASE": "Cannot exponentiate the non-positive number {}",
        "NO_DEFINE": "No function definition specified",
        "NO_DIGITS": "Number of digits not specified",
        "NO_FILENAME": "No file name specified",
        "NO_SAVE": "Nothing to save",
        "NONNUMERIC": "Constants must be numeric",
        "VAR_SAVED": "{} variable definitions saved to {}",
    }

    def __init__(self, debug=True):
        """ Creates a new Evaluator class """
        self.debug = debug
        self.stack = []
        self.constant = {}
        self.function = {}
        self.variable = {}
        self.memory = [-1]
        self.helptext = {}
        ...

    def run(self, args):
        #   Load the profile, if any
        if not args.noprofile:
            self.load_profile()

        #   Run any command line tokens
        if args.c:
            rc = self.ev(args.c)
            if rc == EXIT:
                return

        #   Main loop
        while True:
            fullline = ""
            prompt = Evaluator.PROMPT
            while True:
                line = input(prompt)
                if line.endswith("\\"):
                    line = line.rstrip("\\").rstrip() + " "
                    fullline += line
                    prompt = Evaluator.CONTINUATION_PROMPT
                else:
                    fullline += line
                    break
            rc = self.ev(fullline)
            if rc == EXIT:
                return

    def ev(self, command) -> str | None:
        """Evaluates input line"""
        if not command or command.startswith('#'):
            return

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
            'SEE': self.do_see,
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
            'TRUE': self.do_true,
            'FALSE': self.do_false,
            '>': self.do_greater_than,
            '<': self.do_less_than,
            '=': self.do_equal_to,
            '==': self.do_equal_to,
            '>=': self.do_greater_than_or_equal_to,
            '<=': self.do_less_than_or_equal_to,
            '!=': self.do_not_equal_to,
            '<>': self.do_not_equal_to,
            'AND': self.do_and,
            'OR': self.do_or,
            'NOT': self.do_not,
            'XOR': self.do_xor,
        }

        #   Check for full line commands
        tokens = command.split()
        kwd = tokens[0].upper()
        rest = " ".join(tokens[1:])

        try:
            if kwd in full_line_commands:
                full_line_commands[kwd](rest)
                return

            #   Evaluate each token
            for token in tokens:
                token = token.upper()
                if token in ['Q', 'QUIT', 'EXIT']:
                    return EXIT
                if self.is_numeric(token):
                    result = NumberEntry(token)
                    self.push(result)
                elif token in self.variable:
                    result = self.variable[token]
                    self.push(result)
                elif token in self.constant:
                    result = self.constant[token]
                    self.push(result)
                elif token in self.function:
                    result = self.function[token]
                    self.ev(result)
                elif token == 'PI':
                    result = NumberEntry(pi)
                    self.push(result)
                elif token == 'E':
                    result = NumberEntry(mp.e)
                    self.push(result)
                elif token in commands:
                    commands[token]()
                else:
                    errmsg = Evaluator.MSG["BAD_TOKEN"].format(token)
                    raise RuntimeError(errmsg)
        except RuntimeError as e:
            errmsg = str(e)
            if self.debug:
                raise e
            else:
                print(errmsg)

    @stack_needs(1)
    def do_acos(self):
        x = self.pop().value
        y = acos(x)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_add(self):
        """ Adds two elements at top of stack """
        f2 = self.pop().value
        f1 = self.pop().value
        result = NumberEntry(f1 + f2)
        self.push(result)

    @stack_needs(2)
    def do_and(self):
        """Pushes f1 AND f2 onto the stack"""
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 and f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_asin(self):
        x = self.pop().value
        y = asin(x)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_atan(self):
        x = self.pop().value
        y = atan(x)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_atan2(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = atan2(f1, f2)
        result = NumberEntry(y)
        self.push(result)

    def do_clear(self):
        """ Clears the stack """
        self.stack.clear()

    def do_const(self, line):
        """ Defines a constant """
        line = line.upper()
        tokens = line.split()
        if len(tokens) < 2:
            errmsg = Evaluator.MSG["BAD_CONST"]
            raise RuntimeError(errmsg)

        #   The constant value needs to be calculated
        constname, *program = tokens
        constprogram = ' '.join(program)
        d1 = len(self.stack)
        self.ev(constprogram)
        d2 = len(self.stack)
        if d2 == (d1 + 1):
            self.constant[constname] = self.pop()
        else:
            errmsg = Evaluator.MSG["BAD_CONSTP"]
            raise RuntimeError(errmsg)

    @stack_needs(1)
    def do_cos(self):
        f1 = self.pop().value
        y = cos(f1)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_decrement(self):
        f1 = self.pop().value
        y = f1 - 1
        result = NumberEntry(y)
        self.push(result)

    def do_define(self, line):
        tokens = line.split()
        name = tokens[0].upper()
        tokens = tokens[1:]
        if not tokens:
            errmsg = Evaluator.MSG["NO_DEFINE"]
            raise RuntimeError(errmsg)
        definition = ' '.join(tokens)
        self.function[name] = definition

    def do_depth(self):
        """ (a1 a2 ... an -- a1 a2 ... an n) """
        y = len(self.stack)
        result = NumberEntry(y)
        self.push(result)

    @staticmethod
    def do_digits(line):
        tokens = line.split()
        if len(tokens) == 0:
            print(mp.dps)
            return
        try:
            digits = int(tokens[0])
            mp.dps = digits
        except ValueError:
            errmsg = Evaluator.MSG["BAD_DIGITS"].format(tokens[0])
            raise RuntimeError(errmsg)

    @stack_needs(2)
    def do_div(self):
        f2 = self.pop().value
        if f2 == 0:
            errmsg = Evaluator.MSG["DIVIDE_BY_0"]
            raise RuntimeError(errmsg)
        f1 = self.pop().value
        y = f1 / f2
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_drop(self):
        self.pop()

    @stack_needs(1)
    def do_dup(self):
        f1 = self.peek()
        self.push(f1)

    @stack_needs(1)
    def do_exp(self):
        x = self.pop().value
        y = exp(x)
        result = NumberEntry(y)
        self.push(result)

    def do_false(self):
        result = FALSE
        self.push(result)

    @stack_needs(1)
    def do_fetch(self):
        """Returns the current value of a variable

        The value on the stack is the address of the variable (index into memory array)
        and so must be an integer
        """
        test = self.pop()
        if isinstance(test, int):
            f1 = test
        else:
            f1 = test.value
        if f1 < 1 or f1 >= len(self.memory):
            errmsg = Evaluator.MSG["BAD_VARNUM"].format(f1)
            raise RuntimeError(errmsg)
        self.push(self.memory[f1])

    @stack_needs(2)
    def do_less_than_or_equal_to(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 < f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_less_than(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 < f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_greater_than_or_equal_to(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 >= f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_greater_than(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 > f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_equal_to(self):
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 == f2
        result = BooleanEntry(y)
        self.push(result)

    @staticmethod
    def do_help(topic):
        EVHelp(topic.upper())

    @stack_needs(1)
    def do_increment(self):
        f1 = self.pop().value
        y = f1 + 1
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_int(self):
        f1 = self.pop().value
        y = int(f1)
        result = NumberEntry(y)
        self.push(result)

    def do_load(self, filename):
        # Remove quotes if present
        filename = str(filename)
        filename = filename.replace("'", "")
        filename = filename.replace('"', "")
        try:
            with open(filename, "r") as f:
                while True:
                    fullline = ""
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("#"):
                            continue
                        if line.endswith("\\"):
                            line = line.rstrip("\\").rstrip() + " "
                            fullline += line
                        else:
                            fullline += line
                            break
                    if not fullline:
                        break
                    self.ev(fullline)
        except FileNotFoundError:
            errmsg = Evaluator.MSG["BAD_OPEN"].format(filename)
            raise RuntimeError(errmsg)

    @stack_needs(1)
    def do_ln(self):
        x = self.pop().value
        y = ln(x)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_log(self):
        x = self.pop().value
        y = log10(x)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_mod(self):
        f2 = self.pop().value
        if f2 == 0:
            errmsg = Evaluator.MSG["DIVIDE_BY_0"]
            raise RuntimeError(errmsg)
        f1 = self.pop().value
        y = f1 % f2
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_divmod(self):
        value = self.pop().value
        f2 = round(value)
        if f2 == 0:
            errmsg = Evaluator.MSG["DIVIDE_BY_0"]
            raise RuntimeError(errmsg)
        value = self.pop().value
        f1 = round(value)
        q, r = divmod(f1, f2)
        result = NumberEntry(r)
        self.push(result)
        result = NumberEntry(q)
        self.push(result)

    @stack_needs(2)
    def do_mult(self):
        """ Multiplies two elements at top of stack """
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 * f2
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_not(self):
        """Pushes NOT f1 onto the stack"""
        f1 = self.pop().value
        y = not bool(f1)
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_not_equal_to(self):
        """Returns True if f1 != f2"""
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 != f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_or(self):
        """Pushes f1 OR f2 onto the stack"""
        f2 = self.pop().value
        f1 = self.pop().value
        y = f1 or f2
        result = BooleanEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_over(self):
        """ (x y -- x y x) """
        # OVER is type-agnostic
        y = self.pop()
        x = self.pop()
        self.push(x)
        self.push(y)
        self.push(x)

    @stack_needs(2)
    def do_pow(self):
        f2 = self.pop().value
        f1 = self.pop().value
        if f1 <= 0:
            errmsg = Evaluator.MSG["NEGATIVE_BASE"].format(f1)
            raise RuntimeError(errmsg)
        if f2 == int(f2):
            y = f1 ** f2
        else:
            y = power(f1, f2)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_print(self):
        f1 = self.pop().value
        print(f1)

    @stack_needs(3)
    def do_rotate(self):
        """ (a b c) -- (b c a) """
        # ROT is type-agnostic
        c = self.pop()
        b = self.pop()
        a = self.pop()
        self.push(b)
        self.push(c)
        self.push(a)

    def do_save(self, filename):
        """ Saves all functions, constants, and variables
        """
        # Open the output file
        if not filename:
            errmsg = Evaluator.MSG["NO_FILENAME"]
            raise RuntimeError(errmsg)

        # Remove quotes from filename, if present
        filename = str(filename)
        filename = filename.replace("'", "")
        filename = filename.replace('"', "")
        filename = Path(filename).expanduser()

        with open(filename, "wt") as OFILE:

            # Save digits of precision
            OFILE.write(f"digits {mp.dps}\n")

            # Save constants
            if self.constant:
                for cname in sorted(self.constant):
                    OFILE.write(f"const {cname.lower()} {self.constant[cname].value}\n")
                print(Evaluator.MSG["CON_SAVED"].format(
                    len(self.constant),
                    filename
                ))

            # Save variables (both definitions and values)
            if self.variable:
                names = [name for name in sorted(self.variable)]
                OFILE.write("var {names}\n".format(
                    names=(' '.join(names)).lower()
                ))
                for vname in names:
                    index = self.variable[vname]
                    value = self.memory[index]
                    if isinstance(value, StackEntry):
                        value = value.value
                    OFILE.write("{value} {name} {token}\n".format(
                        value=value,
                        name=vname.lower(),
                        token='!'
                    ))
                print(Evaluator.MSG["VAR_SAVED"].format(
                    len(names),
                    filename
                ))

            # Save the function definitions
            if self.function:
                for fname in sorted(self.function):
                    OFILE.write("define {name} {body}\n".format(
                        name=fname.lower(),
                        body=self.function[fname],
                    ))
                print(Evaluator.MSG["FUN_SAVED"].format(
                    len(self.function),
                    filename
                ))

    def do_see(self, line):
        """Shows the details of a function, variable, or constant"""
        name = line.upper()
        if name in self.function:
            print(f"function {name}: {self.function[name]}")
        elif name in self.variable:
            print(f"variable {name}: addr={self.variable[name]}, value={self.memory[self.variable[name]].value}")
        elif name in self.constant:
            print(f"constant {name}: {self.constant[name].value}")
        else:
            errmsg = Evaluator.MSG["BAD_SEE"]
            raise RuntimeError(errmsg)

    @staticmethod
    def do_shell():
        """ Invokes a command line shell """
        if sys.platform.startswith("win"):
            subprocess.run("cmd /k", shell=True, check=True)
        else:
            subprocess.run("/usr/bin/gnome-terminal", shell=True, check=True)

    @stack_needs(1)
    def do_sin(self):
        f1 = self.pop().value
        y = sin(f1)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_sqrt(self):
        f1 = self.pop().value
        if f1 < 0:
            errmsg = Evaluator.MSG["BAD_SQRT"].format(f1)
            raise RuntimeError(errmsg)
        y = sqrt(f1)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(2)
    def do_store(self):
        # value is the variable's address (slot in the memory array)
        # and so needs to be an integer
        value = self.pop()
        f2 = value
        if isinstance(value, int):
            f2 = value
        elif isinstance(value, NumberEntry):
            f2 = value.value
            f2 = int(f2)
        if f2 < 1 or f2 >= len(self.memory):
            errmsg = Evaluator.MSG["BAD_VARNUM"].format(f2)
            raise RuntimeError(errmsg)
        f1 = self.pop()
        self.memory[f2] = f1

    @stack_needs(2)
    def do_sub(self):
        """ Subtracts two elements at top of stack """
        f2 = self.pop().value
        f1 = self.pop().value
        self.push(NumberEntry(f1 - f2))

    @stack_needs(2)
    def do_swap(self):
        # SWAP is type-agnostic
        f2 = self.pop()
        f1 = self.pop()
        self.push(f2)
        self.push(f1)

    @stack_needs(1)
    def do_tan(self):
        f1 = self.pop().value
        y = tan(f1)
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_to_degrees(self):
        f1 = self.pop().value
        y = f1 * 180. / pi
        result = NumberEntry(y)
        self.push(result)

    @stack_needs(1)
    def do_to_radians(self):
        f1 = self.pop().value
        y = f1 * pi / 180.0
        result = NumberEntry(y)
        self.push(result)

    def do_true(self):
        result = TRUE
        self.push(result)

    def do_variable(self, line):
        tokens = line.split()
        for varname in tokens:
            varname = varname.upper()
            # Ignore if variable is already defined
            if varname in self.variable:
                continue
            self.memory.append(None)
            self.variable[varname] = len(self.memory) - 1

    @stack_needs(2)
    def do_xor(self):
        f2 = self.pop().value
        f1 = self.pop().value
        f2b = bool(f2)
        f1b = bool(f1)
        y = f2b != f1b
        result = BooleanEntry(y)
        self.push(result)

    def dump_constants(self):
        # If there are no constants defined, skip this command
        if not self.constant or len(self.constant) == 0:
            return

        data = {
            "CONSTANT": [],
            "VALUE": [],
        }
        for constname in sorted(self.constant.keys()):
            value = self.constant[constname].value
            data["CONSTANT"].append(constname.lower())
            data["VALUE"].append(value)
        df = pd.DataFrame(data)
        print(df)

    def dump_functions(self):
        # Ignore this request if there are no functions to display
        if not self.function or len(self.function) == 0:
            return
        data = {
            'FUNCTION': [],
            'DEFINITION': [],
        }
        for fname in sorted(self.function):
            lcfname = fname.lower()
            lcdef = self.function[fname].lower()
            data['FUNCTION'].append(lcfname)
            data['DEFINITION'].append(lcdef)
        df = pd.DataFrame(data)
        print(df)

    def dump_stack(self):
        for stack_entry in self.stack:
            print(stack_entry.value)

    def dump_variables(self):
        # Skip if there are no variables defined
        if not self.variable or len(self.variable) == 0:
            return

        data = {
            'VAR': [],
            'ADDR': [],
            'VALUE': [],
        }
        for varname in sorted(self.variable.keys()):
            lcname = varname.lower()
            addr = self.variable[varname]
            value = self.memory[addr]
            if value is not None:
                value = value.value
            data['VAR'].append(lcname)
            data['ADDR'].append(addr)
            data['VALUE'].append(value)
        df = pd.DataFrame(data)
        print(df)

    @staticmethod
    def is_numeric(arg):
        try:
            mpf(arg)
            return True
        except ValueError:
            return False

    def load_profile(self):
        filename = Path.home().joinpath(".evrc")
        if filename.exists():
            self.do_load(filename)

    def peek(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)
