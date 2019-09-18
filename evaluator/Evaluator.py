#  -----------------------------------------------------------------
#  MODULE NAME:      Evaluator
#  DESCRIPTION:      Interactive RPN calculator
#  AUTHOR:           Phil Hanna
#  USAGE:            ev [expression]
#  -----------------------------------------------------------------

import math
import os
import os.path
import re
import sys
from evaluator.EVHelp import EVHelp


def stack_needs(n):
    """ Decorator for stack checking """

    def decorator(fun):
        def wrapper(*args):
            stack = args[0].stack
            if len(stack) < n:
                print(Evaluator.MSG["EMPTY"])
            else:
                fun(*args)

        return wrapper

    return decorator


class Evaluator:
    #   Constants

    E = 2.718281828459045
    FMTSTR = "%f"
    PI = 3.141592653589793
    PROMPT = "ev> "

    #   Error messages

    MSG = {
        "BAD_CONST": "Invalid syntax - should be 'const <name> <value>'",
        "BAD_CONSTP": "Invalid syntax - should be 'const <name> <statements>'",
        "BAD_FORMAT": "Invalid format string  Should be printf-style.",
        "BAD_LOG": "Cannot take the log of a non-positive number",
        "BAD_OPEN": "Could not open file {}",
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
        "NO_FILENAME": "No file name specified",
        "NO_SAVE": "Nothing to save",
        "NONNUMERIC": "Constants must be numeric",
        "VAR_SAVED": "{} variable definitions saved to {}",
    }

    #   Constructor

    def __init__(self):
        self.stack = []
        self.constant = {}
        self.function = {}
        self.variable = {}
        self.memory = [-1]
        self.fmtstr = Evaluator.FMTSTR
        self.helptext = {}

        #   Load the profile, if any

        self.load_profile()

    def run(self, args):
        """
            Mainline
        """
        if args:
            line = ' '.join(args)
            self.ev(line)
        while True:
            line = input(Evaluator.PROMPT)
            self.ev(line)

    def ev(self, command):
        """
            Evaluates input line
        """

        if not command:
            return

        #   Check for full line commands

        tokens = command.split()
        kwd = tokens[0].upper()
        rest = " ".join(tokens[1:])

        if kwd in ['HELP', 'H', '?']:
            self.do_help(rest.upper())
            return
        elif kwd == 'CONST':
            self.do_const(rest.upper())
            return
        elif kwd == 'DEFINE':
            self.do_define(rest)
            return
        elif kwd == 'FORMAT':
            self.do_format(rest)
            return
        elif kwd == 'LOAD':
            self.do_load(rest)
            return
        elif kwd == 'SAVE':
            self.do_save(rest)
            return
        elif kwd == 'VAR':
            self.do_variable(rest)
            return

        #   Evaluate each token

        for token in tokens:
            token = token.upper()

            if token in ['Q', 'QUIT', 'EXIT']:
                sys.exit(0)
            elif token in self.variable:
                value = self.variable[token]
                value = float(value)
                self.push(value)
            elif token in self.constant:
                value = self.constant[token]
                value = float(value)
                self.push(value)
            elif token in self.function:
                self.ev(self.function[token])
            elif self.is_numeric(token):
                self.push(self.get_numeric_value(token))
            elif token == '@':
                self.do_fetch()
            elif token == '!':
                self.do_store()
            elif token == '.':
                self.do_print()
            elif token in ['1+', '++']:
                self.do_increment()
            elif token in ['1-', '--']:
                self.do_decrement()
            elif token == 'CLEAR':
                self.do_clear()
            elif token == '+':
                self.do_add()
            elif token == '-':
                self.do_sub()
            elif token == '*':
                self.do_mult()
            elif token == '/':
                self.do_div()
            elif token == '.S':
                self.dump_stack()
            elif token == '.F':
                self.dump_functions()
            elif token == '.V':
                self.dump_variables()
            elif token == '.C':
                self.dump_constants()
            elif token == 'DUP':
                self.do_dup()
            elif token == 'DROP':
                self.do_drop()
            elif token == 'SWAP':
                self.do_swap()
            elif token == 'OVER':
                self.do_over()
            elif token == 'ROT':
                self.do_rotate()
            elif token in ['SQR', 'SQRT']:
                self.do_sqrt()
            elif token == 'SIN':
                self.do_sin()
            elif token == 'COS':
                self.do_cos()
            elif token == 'ATAN':
                self.do_atan()
            elif token == 'ATAN2':
                self.do_atan2()
            elif token == 'TAN':
                self.do_tan()
            elif token == 'ACOS':
                self.do_acos()
            elif token == 'ASIN':
                self.do_asin()
            elif token == 'LOG':
                self.do_log()
            elif token == 'LN':
                self.do_ln()
            elif token == 'EXP':
                self.do_exp()
            elif token == 'TORADIANS':
                self.do_to_radians()
            elif token == 'TODEGREES':
                self.do_to_degrees()
            elif token in ['%', 'MOD']:
                self.do_mod()
            elif token in ['**', '^']:
                self.do_pow()
            elif token == 'INT':
                self.do_int()
            elif token == 'PI':
                self.push(Evaluator.PI)
            elif token == 'E':
                self.push(Evaluator.E)
            elif token == 'DEPTH':
                self.do_depth()
            elif token == 'FMTSTR':
                self.do_format_string()
            elif token == 'SHELL':
                self.do_shell()
            else:
                print(Evaluator.MSG["BAD_TOKEN"].format(token))

    @stack_needs(1)
    def do_acos(self):
        x = self.pop()
        try:
            y = math.acos(x)
            self.push(y)
        except ValueError as e:
            print(e)

    @stack_needs(2)
    def do_add(self):
        """ Adds two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 + f2)

    @stack_needs(1)
    def do_asin(self):
        x = self.pop()
        try:
            y = math.asin(x)
            self.push(y)
        except ValueError as e:
            print(e)

    @stack_needs(1)
    def do_atan(self):
        x = self.pop()
        y = math.atan(x)
        self.push(y)

    @stack_needs(2)
    def do_atan2(self):
        f2 = self.pop()
        f1 = self.pop()
        self.push(math.atan2(f1, f2))

    def do_clear(self):
        """ Clears the stack """
        self.stack = []

    def do_const(self, line):

        """ Defines a constant """

        tokens = line.split()
        if len(tokens) < 2:
            print(Evaluator.MSG["BAD_CONST"])
            return
        else:
            #   The constant value needs to be calculated
            constname, *program = tokens
            constprogram = ' '.join(program)
            d1 = len(self.stack)
            self.ev(constprogram)
            d2 = len(self.stack)
            if d2 == (d1 + 1):
                self.constant[constname] = self.pop()
            else:
                print(Evaluator.MSG["BAD_CONSTP"])

    @stack_needs(1)
    def do_cos(self):
        f1 = self.pop()
        self.push(math.cos(f1))

    @stack_needs(1)
    def do_decrement(self):
        f1 = self.pop()
        self.push(f1 - 1)

    def do_define(self, line):
        tokens = line.split()
        name = tokens[0].upper()
        tokens = tokens[1:]
        if not tokens:
            print(Evaluator.MSG["NO_DEFINE"])
            return
        definition = ' '.join(tokens)
        self.function[name] = definition

    def do_depth(self):
        """ (a1 a2 ... an -- a1 a2 ... an n) """
        self.push(len(self.stack))

    @stack_needs(2)
    def do_div(self):
        f2 = self.pop()
        if f2 == 0:
            print(Evaluator.MSG["DIVIDE_BY_0"])
            return
        f1 = self.pop()
        output = f1 / f2
        self.push(output)

    @stack_needs(1)
    def do_drop(self):
        self.pop()

    @stack_needs(1)
    def do_dup(self):
        f1 = self.peek()
        self.push(f1)

    @stack_needs(1)
    def do_exp(self):
        x = self.pop()
        result = math.exp(x)
        self.push(result)

    @stack_needs(1)
    def do_fetch(self):
        f1 = int(self.pop())
        if f1 < 1 or f1 >= len(self.memory):
            print(Evaluator.MSG["BAD_VARNUM"].format(f1))
            return
        self.push(self.memory[f1])

    def do_format_string(self):
        """Prints the current format string"""
        print('format "{}"'.format(self.fmtstr))

    def do_format(self, new_format):

        #   If no parameter, show current value

        if not new_format:
            print(self.fmtstr)
            return

        #   Shortcuts

        shortcuts = {
            'default': Evaluator.FMTSTR,
            'hex': '0x%x',
            'hex8': '0x%08x',
            'hex4': '0x%04x',
            'hex2': '0x%02x',
            'int': '%.0f',
        }
        if new_format in shortcuts:
            new_format = shortcuts[new_format]
        if new_format == 'shortcuts':
            for k, v in sorted(shortcuts.items()):
                print('format {k:<8} is "{v}"'.format(k=k, v=v))
            return

        #   Remove quotes if there are any

        new_format = re.sub(r"""['"]""", '', new_format)

        #   Validate according to
        #   docs.python.org/2/library/stdtypes.html#string-formatting

        m = re.search((
            r'%'
            r'[#0\- +]*'
            r'\d*'
            r'(\.\d+)*'
            r'[diouxXeEfFgGcb]'
        ), new_format)
        if not m:
            print(Evaluator.MSG["BAD_FORMAT"])
            return

        #   Assign the new format

        self.fmtstr = new_format

    def do_help(self, topic):
        EVHelp(topic)

    @stack_needs(1)
    def do_increment(self):
        f1 = self.pop()
        self.push(f1 + 1)

    @stack_needs(1)
    def do_int(self):
        f1 = self.pop()
        self.push(int(f1))

    def do_load(self, filename):
        # Remove quotes if present
        filename = re.sub('"', '', filename)
        try:
            with open(filename, "r") as f:
                for line in f:
                    if not line:
                        continue
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    self.ev(line)
        except FileNotFoundError:
            print(Evaluator.MSG["BAD_OPEN"].format(filename))

    @stack_needs(1)
    def do_ln(self):
        x = self.pop()
        y = math.log(x)
        self.push(y)

    @stack_needs(1)
    def do_log(self):
        x = self.pop()
        y = math.log10(x)
        self.push(y)

    @stack_needs(2)
    def do_mod(self):
        f2 = self.pop()
        if f2 == 0:
            print(Evaluator.MSG["DIVIDE_BY_0"])
            return
        f1 = self.pop()
        output = f1 % f2
        self.push(output)

    @stack_needs(2)
    def do_mult(self):
        """ Multiplies two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 * f2)

    @stack_needs(2)
    def do_over(self):
        """ (x y -- x y x) """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1)
        self.push(f2)
        self.push(f1)

    @stack_needs(2)
    def do_pow(self):
        f2 = self.pop()
        f1 = self.pop()
        if f1 <= 0:
            print(Evaluator.MSG["NEGATIVE_BASE"].format(f1))
            return
        if f2 == int(f2):
            result = f1 ** f2
        else:
            result = math.pow(f1, f2)
        self.push(result)

    @stack_needs(1)
    def do_print(self):
        f1 = self.pop()
        print(self.format_value(f1))

    @stack_needs(3)
    def do_rotate(self):
        """ (a b c) -- (b c a) """
        f3 = self.pop()
        f2 = self.pop()
        f1 = self.pop()
        self.push(f2)
        self.push(f3)
        self.push(f1)

    def do_save(self, filename):
        """ Saves all functions, constants, and variables
        """

        #   Remove quotes from filename, if present

        filename = re.sub('"', '', filename)

        #   Return if nothing to save

        if (not self.function and not self.constant and not self.variable):
            print(Evaluator.MSG["NO_SAVE"])
            return

        #   Open the output file

        if not filename:
            print(Evaluator.MSG["NO_FILENAME"])
            return

        with open(filename, "wt") as OFILE:

            #   Save constants

            if self.constant:
                for cname in sorted(self.constant):
                    OFILE.write("const {name} {value}\n".format(
                        name=cname.lower(),
                        value=self.constant[cname]
                    ))
                print(Evaluator.MSG["CON_SAVED"].format(
                    len(self.constant),
                    filename
                ))

            #   Save variables (both definitions and values)

            if self.variable:
                names = [name for name in sorted(self.variable)]
                OFILE.write("var {names}\n".format(
                    names=(' '.join(names)).lower()
                ))
                for vname in names:
                    index = self.variable[vname]
                    value = self.memory[index]
                    OFILE.write("{value} {name} {token}\n".format(
                        value=value,
                        name=vname.lower(),
                        token='!'
                    ))
                print(Evaluator.MSG["VAR_SAVED"].format(
                    len(names),
                    filename
                ))

            #   Save the function definitions

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

            #   Save the format string

            OFILE.write('format "{}"\n'.format(self.fmtstr))

    def do_shell(self):
        """ Invokes a command line shell """
        if sys.platform.startswith("win"):
            os.system("cmd /k")
        else:
            os.system("/usr/bin/gnome-terminal")

    @stack_needs(1)
    def do_sin(self):
        f1 = self.pop()
        self.push(math.sin(f1))

    @stack_needs(1)
    def do_sqrt(self):
        f1 = self.pop()
        if f1 < 0:
            print(Evaluator.MSG["BAD_SQRT"].format(f1))
            return
        result = math.sqrt(f1)
        self.push(result)

    @stack_needs(2)
    def do_store(self):
        f2 = int(self.pop())
        if f2 < 1 or f2 >= len(self.memory):
            print(Evaluator.MSG["BAD_VARNUM"].format(f2))
            return
        f1 = self.pop()
        self.memory[f2] = f1

    @stack_needs(2)
    def do_sub(self):
        """ Subtracts two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 - f2)

    @stack_needs(2)
    def do_swap(self):
        f2 = self.pop()
        f1 = self.pop()
        self.push(f2)
        self.push(f1)

    @stack_needs(1)
    def do_tan(self):
        f1 = self.pop()
        self.push(math.tan(f1))

    @stack_needs(1)
    def do_to_degrees(self):
        f1 = self.pop()
        result = f1 * 180. / Evaluator.PI
        self.push(result)

    @stack_needs(1)
    def do_to_radians(self):
        f1 = self.pop()
        result = f1 * Evaluator.PI / 180.0
        self.push(result)

    def do_variable(self, line):
        tokens = line.split()
        for varname in tokens:
            varname = varname.upper()
            if varname in self.variable:
                continue
            self.memory.append(0)
            self.variable[varname] = len(self.memory) - 1

    def dump_constants(self):
        if not len(self.constant):
            return
        print("CONSTANT        VALUE")
        for constname in sorted(self.constant.keys()):
            value = self.constant[constname]
            print("{name:<8s}        {value}".format(
                name=constname.lower(),
                value=self.format_value(value)
            ))

    def dump_functions(self):
        if not len(self.function):
            return
        print("FUNCTION  DEFINITION")
        for fname in sorted(self.function):
            lcfname = fname.lower()
            lcdef = self.function[fname].lower()
            print("{name:<8s}  {definition}".format(
                name=lcfname,
                definition=lcdef))

    def dump_stack(self):
        for value in self.stack:
            print(self.format_value(value))

    def dump_variables(self):
        if not len(self.variable):
            return
        print("VAR       ADDR  VALUE")
        for varname in sorted(self.variable.keys()):
            lcname = varname.lower()
            addr = self.variable[varname]
            value = self.format_value(self.memory[addr])
            print("{name:<8s}  {addr:04d}  {value}".format(
                name=lcname,
                addr=addr,
                value=value))

    def format_value(self, value):
        try:
            output = self.fmtstr % float(value)
        except TypeError:
            output = self.fmtstr % int(value)
        output = re.sub(r'(\.[0-9]*?)0+$', r'\1', output)
        output = re.sub(r'\.$', '', output)
        return output

    def get_numeric_value(self, arg):
        try:
            return float(arg)
        except ValueError:
            m = re.match(r'0[xX]([0-9a-fA-F]+)', arg)
            if m:
                hexstring = m.group(1)
                return float.fromhex(hexstring)
            print("{} is not numeric".format(arg))
            return None

    def is_numeric(self, arg):
        try:
            float(arg)
            return True
        except ValueError:
            m = re.match(r'0[xX][0-9a-fA-F]+', arg)
            if m:
                return True
            return False

    def load_profile(self):
        home = os.path.expanduser("~")
        filename = os.path.join(home, ".evrc")
        if os.path.exists(filename):
            self.do_load(filename)

    def peek(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)
