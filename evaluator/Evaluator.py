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


def stackNeeds(n):
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

    E  = 2.718281828459045
    FMTSTR = "%f"
    PI = 3.141592653589793
    PROMPT = "ev> "

    #   Error messages

    MSG = {
        "BAD_CONST"     : "Invalid syntax - should be 'const <name> <value>'",
        "BAD_CONSTP"    : "Invalid syntax - should be 'const <name> <statements>'",
        "BAD_FORMAT"    : "Invalid format string  Should be printf-style.",
        "BAD_LOG"       : "Cannot take the log of a non-positive number",
        "BAD_OPEN"      : "Could not open file {}",
        "BAD_SQRT"      : "Cannot take the square root of the negative number {}",
        "BAD_TOKEN"     : "Unrecognized token {}",
        "BAD_VARNUM"    : "Invalid memory reference, index={}",
        "CON_SAVED"     : "{} constant definitions saved to {}",
        "DIVIDE_BY_0"   : "Cannot divide by zero",
        "EMPTY"         : "Stack empty",
        "FUN_SAVED"     : "{} function definitions saved to {}",
        "INFINITY"      : "Number too large to represent",
        "NEGATIVE_BASE" : "Cannot exponentiate the non-positive number {}",
        "NO_DEFINE"     : "No function definition specified",
        "NO_FILENAME"   : "No file name specified",
        "NO_SAVE"       : "Nothing to save",
        "NONNUMERIC"    : "Constants must be numeric",
        "VAR_SAVED"     : "{} variable definitions saved to {}",
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

        self.loadProfile()

    def run(self, args):
        """
            Mainline
        """
        if args:
            line = ' '.join(args)
            self.ev(line)
            args = []
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
            self.doHelp(rest.upper())
            return
        elif kwd == 'CONST':
            self.doConst(rest.upper())
            return
        elif kwd == 'DEFINE':
            self.doDefine(rest)
            return
        elif kwd == 'FORMAT':
            self.doFormat(rest)
            return
        elif kwd == 'LOAD':
            self.doLoad(rest)
            return
        elif kwd == 'SAVE':
            self.doSave(rest)
            return
        elif kwd == 'VAR':
            self.doVar(rest)
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
            elif self.numeric(token):
                self.push(self.numval(token))
            elif token == '@':
                self.doFetch()
            elif token == '!':
                self.doStore()
            elif token == '.':
                self.doPrint()
            elif token in ['1+', '++']:
                self.doIncrement()
            elif token in ['1-', '--']:
                self.doDecrement()
            elif token == 'CLEAR':
                self.doClear()
            elif token == '+':
                self.doAdd()
            elif token == '-':
                self.doSub()
            elif token == '*':
                self.doMult()
            elif token == '/':
                self.doDiv()
            elif token == '.S':
                self.dump_stack()
            elif token == '.F':
                self.dump_functions()
            elif token == '.V':
                self.dump_variables()
            elif token == '.C':
                self.dump_constants()
            elif token == 'DUP':
                self.doDup()
            elif token == 'DROP':
                self.doDrop()
            elif token == 'SWAP':
                self.doSwap()
            elif token == 'OVER':
                self.doOver()
            elif token == 'ROT':
                self.doRot()
            elif token in ['SQR', 'SQRT']:
                self.doSqrt()
            elif token == 'SIN':
                self.doSin()
            elif token == 'COS':
                self.doCos()
            elif token == 'ATAN':
                self.doAtan()
            elif token == 'ATAN2':
                self.doAtan2()
            elif token == 'TAN':
                self.doTan()
            elif token == 'ACOS':
                self.doAcos()
            elif token == 'ASIN':
                self.doAsin()
            elif token == 'LOG':
                self.doLog()
            elif token == 'LN':
                self.doLn()
            elif token == 'EXP':
                self.doExp()
            elif token == 'TORADIANS':
                self.doToRadians()
            elif token == 'TODEGREES':
                self.doToDegrees()
            elif token in ['%', 'MOD']:
                self.doMod()
            elif token in ['**', '^']:
                self.doPow()
            elif token == 'INT':
                self.doInt()
            elif token == 'PI':
                self.push(Evaluator.PI)
            elif token == 'E':
                self.push(Evaluator.E)
            elif token == 'DEPTH':
                self.doDepth()
            elif token == 'FMTSTR':
                self.doFmtstr()
            elif token == 'SHELL':
                self.doShell()
            else:
                print(Evaluator.MSG["BAD_TOKEN"].format(token))

    @stackNeeds(1)
    def doAcos(self):
        x = self.pop()
        try:
            y = math.acos(x)
            self.push(y)
        except ValueError as e:
            print(e)

    @stackNeeds(2)
    def doAdd(self):
        """ Adds two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 + f2)

    @stackNeeds(1)
    def doAsin(self):
        x = self.pop()
        try:
            y = math.asin(x)
            self.push(y)
        except ValueError as e:
            print(e)

    @stackNeeds(1)
    def doAtan(self):
        x = self.pop()
        y = math.atan(x)
        self.push(y)

    @stackNeeds(2)
    def doAtan2(self):
        f2 = self.pop()
        f1 = self.pop()
        self.push(math.atan2(f1, f2))

    def doClear(self):
        """ Clears the stack """
        self.stack = []

    def doConst(self, line):

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

    @stackNeeds(1)
    def doCos(self):
        f1 = self.pop()
        self.push(math.cos(f1))

    @stackNeeds(1)
    def doDecrement(self):
        f1 = self.pop()
        self.push(f1 - 1)

    def doDefine(self, line):
        tokens = line.split()
        name = tokens[0].upper()
        tokens = tokens[1:]
        if not tokens:
            print(Evaluator.MSG["NO_DEFINE"])
            return
        definition = ' '.join(tokens)
        self.function[name] = definition

    def doDepth(self):
        """ (a1 a2 ... an -- a1 a2 ... an n) """
        self.push(len(self.stack))

    @stackNeeds(2)
    def doDiv(self):
        f2 = self.pop()
        if f2 == 0:
            print(Evaluator.MSG["DIVIDE_BY_0"])
            return
        f1 = self.pop()
        output = f1 / f2
        self.push(output)

    @stackNeeds(1)
    def doDrop(self):
        self.pop()

    @stackNeeds(1)
    def doDup(self):
        f1 = self.peek()
        self.push(f1)

    @stackNeeds(1)
    def doExp(self):
        x = self.pop()
        result = math.exp(x)
        self.push(result)

    @stackNeeds(1)
    def doFetch(self):
        f1 = int(self.pop())
        if f1 < 1 or f1 >= len(self.memory):
            print(Evaluator.MSG["BAD_VARNUM"].format(f1))
            return
        self.push(self.memory[f1])

    def doFmtstr(self):
        """Prints the current format string"""
        print('format "{}"'.format(self.fmtstr))

    def doFormat(self, new_format):

        #   If no parameter, restore default value

        if not new_format:
            self.fmtstr = Evaluator.FMTSTR
            return

        #   Shortcuts

        shortcuts = {
            'hex'   : '0x%x',
            'hex8'  : '0x%08x',
            'hex4'  : '0x%04x',
            'hex2'  : '0x%02x',
            'int'   : '%.0f',
        }
        if new_format in shortcuts:
            new_format = shortcuts[new_format]
        if new_format == 'shortcuts':
            for k,v in sorted(shortcuts.items()):
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

    def doHelp(self, topic):
        EVHelp(topic)

    @stackNeeds(1)
    def doIncrement(self):
        f1 = self.pop()
        self.push(f1 + 1)

    @stackNeeds(1)
    def doInt(self):
        f1 = self.pop()
        self.push(int(f1))

    def doLoad(self, filename):
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

    @stackNeeds(1)
    def doLn(self):
        x = self.pop()
        y = math.log(x)
        self.push(y)

    @stackNeeds(1)
    def doLog(self):
        x = self.pop()
        y = math.log10(x)
        self.push(y)

    @stackNeeds(2)
    def doMod(self):
        f2 = self.pop()
        if f2 == 0:
            print(Evaluator.MSG["DIVIDE_BY_0"])
            return
        f1 = self.pop()
        output = f1 % f2
        self.push(output)

    @stackNeeds(2)
    def doMult(self):
        """ Multiplies two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 * f2)

    @stackNeeds(2)
    def doOver(self):
        """ (x y -- x y x) """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1)
        self.push(f2)
        self.push(f1)

    @stackNeeds(2)
    def doPow(self):
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
        
    @stackNeeds(1)
    def doPrint(self):
        f1 = self.pop()
        print(self.fmtval(f1))

    @stackNeeds(3)
    def doRot(self):
        """ (a b c) -- (b c a) """
        f3 = self.pop()
        f2 = self.pop()
        f1 = self.pop()
        self.push(f2)
        self.push(f3)
        self.push(f1)

    def doSave(self, filename):
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
                        name = cname.lower(),
                        value = self.constant[cname]
                        ))
                print(Evaluator.MSG["CON_SAVED"].format(
                    len(self.constant),
                    filename
                    ))

            #   Save variables (both definitions and values)

            if self.variable:
                names = [name for name in sorted(self.variable)]
                OFILE.write("var {names}\n".format(
                    names = (' '.join(names)).lower()
                    ))
                for vname in names:
                    index = self.variable[vname]
                    value = self.memory[index]
                    OFILE.write("{value} {name} {token}\n".format(
                        value = value,
                        name = vname.lower(),
                        token = '!'
                        ))
                print(Evaluator.MSG["VAR_SAVED"].format(
                    len(names),
                    filename
                    ))

            #   Save the function definitions

            if self.function:
                for fname in sorted(self.function):
                    OFILE.write("define {name} {body}\n".format(
                        name = fname.lower(),
                        body = self.function[fname],
                        ))
                print(Evaluator.MSG["FUN_SAVED"].format(
                    len(self.function),
                    filename
                    ))

            #   Save the format string

            OFILE.write('format "{}"\n'.format(self.fmtstr))

    def doShell(self):
        """ Invokes a command line shell """
        if sys.platform.startswith("win"):
            os.system("cmd /k")
        else:
            os.system("/usr/bin/gnome-terminal")

    @stackNeeds(1)
    def doSin(self):
        f1 = self.pop()
        self.push(math.sin(f1))

    @stackNeeds(1)
    def doSqrt(self):
        f1 = self.pop()
        if f1 < 0:
            print(Evaluator.MSG["BAD_SQRT"].format(f1))
            return
        result = math.sqrt(f1)
        self.push(result)
        
    @stackNeeds(2)
    def doStore(self):
        f2 = int(self.pop())
        if f2 < 1 or f2 >= len(self.memory):
            print(Evaluator.MSG["BAD_VARNUM"].format(f2))
            return
        f1 = self.pop()
        self.memory[f2] = f1

    @stackNeeds(2)
    def doSub(self):
        """ Subtracts two elements at top of stack """
        f2 = self.pop()
        f1 = self.pop()
        self.push(f1 - f2)

    @stackNeeds(2)
    def doSwap(self):
       f2 = self.pop()
       f1 = self.pop()
       self.push(f2)
       self.push(f1)

    @stackNeeds(1)
    def doTan(self):
        f1 = self.pop()
        self.push(math.tan(f1))

    @stackNeeds(1)
    def doToDegrees(self):
        f1 = self.pop()
        result = f1 * 180. / Evaluator.PI
        self.push(result)

    @stackNeeds(1)
    def doToRadians(self):
        f1 = self.pop()
        result = f1 * Evaluator.PI / 180.0
        self.push(result)

    def doVar(self, line):
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
                name = constname.lower(),
                value = self.fmtval(value)
                ))

    def dump_functions(self):
        if not len(self.function):
            return
        print("FUNCTION  DEFINITION")
        for fname in sorted(self.function):
            lcfname = fname.lower()
            lcdef   = self.function[fname].lower()
            print("{name:<8s}  {definition}".format(
                name = lcfname,
                definition = lcdef))

    def dump_stack(self):
        for value in self.stack:
            print(self.fmtval(value))

    def dump_variables(self):
        if not len(self.variable):
            return 
        print("VAR       ADDR  VALUE")
        for varname in sorted(self.variable.keys()):
            lcname  = varname.lower()
            addr    = self.variable[varname]
            value   = self.fmtval(self.memory[addr])
            print("{name:<8s}  {addr:04d}  {value}".format(
                name = lcname,
                addr = addr,
                value = value))
        
    def fmtval(self, value):
        try:
            output = self.fmtstr % float(value)
        except TypeError:
            output = self.fmtstr % int(value)
        output = re.sub(r'(\.[0-9]*?)0+$', r'\1', output)
        output = re.sub(r'\.$', '', output)
        return output
        
    def loadProfile(self):
        home = os.path.expanduser("~")
        filename = os.path.join(home, ".evrc")
        if os.path.exists(filename):
            self.doLoad(filename)

    def numeric(self, arg):
        try:
            float(arg)
            return True
        except ValueError:
            m = re.match(r'0[xX][0-9a-fA-F]+', arg)
            if m:
                return True
            return False

    def numval(self, arg):
        try:
            return float(arg)
        except ValueError:
            m = re.match(r'0[xX]([0-9a-fA-F]+)', arg)
            if m:
                hexstring = m.group(1)
                return float.fromhex(hexstring)
            print("{} is not numeric".format(arg))
            return None

    def peek(self):
        return self.stack[-1]
        
    def pop(self):
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)
