class EVHelp:
    helptext = {
        "overview": """
OVERVIEW: 

ev is an interactive programmable RPN calculator.  (Type 'help RPN' 
for details about Reverse Polish Notation).  It reads blank-delimited 
tokens from the input stream and interprets them one at a time using 
a syntax inspired by the FORTH programming language.  Anything following 
a '#' on an input line is considered a comment.

Besides simple calculations, ev supports variables, constants, and 
function definitions.  It also allows save and restore operations.

   For help on an individual topic, type 'help <topic name>'.

   To see a list of topics, type 'help topics'.

   To exit from ev, type 'q';
""",
        "topics": """
Arithmetic operations:   +, -, *, /, %, **, 1+, 1-, int, sqrt
Commands:                help, load, quit, save, shell
Configuration:           profile
Constants:               e, pi
Conversion functions:    toDegrees, toRadians
Declaratives:            const, define, digits, var
Log functions:           exp, ln, log
Memory operations:       @, !
Print functions:         ., .c, .f, .s, .v
Stack functions:         clear, depth, drop, dup, over, rot, swap
Trigonometric functions: acos, asin, atan, atan2, cos, sin, tan

""",

        "rpn": """

Reverse Polish Notation (RPN) is a syntax for writing
arithmetic expressions in which the operator follows the 
operands.  For example, 2 + 2 is written 2 2 +.  

RPN makes parentheses unnecessary: (1 + 5) * (3 - 4) is 
written 1 5 + 3 4 - *.  It also makes rules about operator
precedence unnecessary, since operators always take their
operands from the top of the stack and push their results
onto the stack.

While RPN may take a little getting used to, it is quite
compact and straightforward.  It is the standard notation
used by Hewlett Packard calculators.

""",
        "+": """
+:  Pops x and y from the stack and pushes x + y.
""",
        "-": """
-:  Pops x and y from the stack and pushes x - y.
""",
        "*": """
*:  Pops x and y from the stack and pushes x * y.
""",
        "/": """
/:  Pops x and y from the stack and pushes x / y.
     y must not be zero.
""",
        "%": """
%:  Pops x and y from the stack and pushes x mod y.
     y must not be zero.
""",
        "**": """
** :  Pops x and y from the stack and pushes x to the y power.
      '^' is a synonym for '**'.
""",
        "1+": """
1+ :  Pops x from the stack, increments it, and pushes it.
      '++' is a synonym for '1+'.
""",
        "1-": """
1- :  Pops x from the stack, decrements it, and pushes it.
      '--' is a synonym for '1-'.
""",
        "int": """
int:  Pops x from the stack and pushes the integer
      portion of x
""",
        "sqrt": """
sqrt:  Pops x from the stack and pushes its square root.
       x must be non-negative.
""",
        "help": """
help <topic>:  Displays the help text for <topic>.  
               If no topic is specified, displays
               the help text overview.

               'h' and '?' are aliases for 'help'.
""",
        "load": """
load <filename>:  Reads and interprets the contents of <filename>.
                  The file may contain any valid calculator commands.
                  Typically, <filename> is the result of a
                  'save' command, but it can be created by any
                  text editor.

                  See also 'profile'.
""",
        "quit": """
quit:  Exits from the calculator.
""",
        "save": """
save <filename>:  Saves the current state of the calculator,
                  including variable definitions and values,
                  constants, and function definitions. 

                  The saved state can be restored with the 'load'
                  command.
""",
        "shell": """
shell: Invokes a shell.
""",
        "profile": """
During initialization, ev looks for a file called '.evrc' in the home
directory.  If this profile file exists, it is loaded.  This feature
can be used to load frequently used constants and function definition.

See also 'load'.
""",
        "e": """
e:  Pushes the value of the constant e (2.718281828459045).
""",
        "pi": """
pi: Pushes the value of the constant pi (3.141592653589793).
""",
        "todegrees": """
toDegrees:  Pops x from the stack, converts it from radians to
            degrees, and pushes it back on the stack.
""",
        "toradians": """
toRadians:  Pops x from the stack, converts it from degrees to
            radians, and pushes it back on the stack.
""",
        "const": """
const:  Allows a constant to be defined.  The syntax used is

        const <constname> <definition>

        where <definition> can be a number or any list of
        valid calculator commands.  Constant names are not 
        case-sensitive.

        If 'const' is used, it must be the first token on the
        input line, and the rest of the line is ignored after
        the constant is evaluated.
""",
        "define": """
define:  Allows a function to be defined.  The syntax used is

         define <function name> <definition>

         where <definition> is a list of any valid calculator
         commands.  Function names are not case-sensitive.

         If 'define' is used, it must be the first token on the
         input line, and the rest of the line is ignored after
         the function definition is evaluated.
""",
        "digits": """
digits:  Defines the number of digits used for displaying numeric values.
         The syntax used is:

         digits <digits>

         where <digits> is an integer.

         If no digits argument is specified, shows current setting.
""",
        "var": """
var:  Allows a variable to be defined.  The syntax used is

      var <variable name> [, <variable name> ...]

      where <variable name> is any string of characters.
      Variable names are not case-sensitive.

      If 'var' is used, it must be the first token on the
      input line, and the rest of the tokens on the line
      are considered to be variable names.

      Once a variable is declared, it can have a value stored
      in it with the ! operator, and the value can be retrieved
      with the @ operator.

      WARNING:  No check is performed to see if a variable
      being defined is also a calculator keyword.  If you
      redefine a keyword, it will no longer perform its regular
      function.
""",
        "exp": """
exp:  Pops x from the stack and pushes e^x.
""",
        "ln": """
ln:  Pops x from the stack and pushes ln(x), the natural
     logarithm (base e) of x.

     x must be greater than zero.
""",
        "log": """
log:  Pops x from the stack and pushes log(x), the base 10
      logarithm of x.

      x must be greater than zero.
      
      log10 is an alias for log.
""",
        "@": """
@:  Used to fetch the value of a variable.  The syntax used is

    <varname> @

    where <varname> is the name of a previously declared variable.
    <varname> is popped from the stack, and the value of the
    variable is pushed.

    See also 'var', '!'.
""",
        "!": """
!:  Used to set the value of a variable.  The syntax used is

    <value> <varname> !

    where <varname> is the name of a previously declared variable.
    <value> and <varname> are popped from the stack and <value>
    is assigned to <varname>.

    See also 'var', '@'.
""",
        ".": """
.:  Pops x from the stack and prints it.  The display format
    is controlled by the current value of the format string.

    See also 'format', '.s'.
""",
        ".c": """
.c:  Prints a list of all user-defined constants and their values.

     See also 'const', 'format'.
""",
        ".f": """
.f:  Prints a list of all user-defined functions and their
     definitions.

     See also 'define'.
""",
        ".s": """
.s:  Prints the contents of the stack.  The stack level is not
     affected.  The display format is controlled by the current
     value of the format string.

     See also 'format'.
""",
        ".v": """
.v:  Prints a list of all user-defined variables and their values.

     See also 'var', 'format'.
""",
        "clear": """
clear:  Clears the contents of the stack.
""",
        "depth": """
depth:  Pushes the number of items on the stack
""",
        "drop": """
drop:  Pops the top element from the stack and discards it.
""",
        "dup": """
dup:  Pops the top element from the stack and pushes it twice.
""",
        "over": """
over:  Pops x and y from the stack, then pushes x, y, x.
""",
        "rot": """
rot:  Pops x, y, and z from the stack, then pushes y, z, and x.
""",
        "swap": """
swap:  Exchanges the order of the top two elements on the stack.
""",
        "acos": """
acos:  Pops x from the stack and then pushes the arccosine of
       x in radians

       See also 'toDegrees', 'toRadians'.
""",
        "asin": """
asin:  Pops x from the stack and then pushes the arcsine of
       x in radians

       See also 'toDegrees', 'toRadians'.
""",
        "atan": """
atan:  Pops x from the stack and then pushes the arctangent of
       x in radians in the range -pi to pi.

       See also 'toDegrees', 'toRadians'.
""",
        "atan2": """
atan2: Pops y and x from the stack and then pushes the arctangent
       of y/x in radians in the range -pi to pi.

       See also 'toDegrees', 'toRadians'.
""",
        "cos": """
cos:  Pops x from the stack and then pushes the cosine of x.
      x must be expressed in radians.

      See also 'toDegrees', 'toRadians'.
""",
        "sin": """
sin:  Pops x from the stack and then pushes the sine of x.
      x must be expressed in radians.

      See also 'toDegrees', 'toRadians'.
""",
        "tan": """
tan:  Pops x from the stack and then pushes the tangent of x.
      x must be expressed in radians.

      See also 'toDegrees', 'toRadians'.
""",
        "fmtstr": """
fmtstr: Prints the current format string
""",
    }

    def __init__(self, *args):
        if args and args[0]:
            topic = args[0]
        else:
            topic = "Overview"
        lctopic = topic.lower()
        if not lctopic in EVHelp.helptext:
            print("No help found for {}".format(topic))
            return
        text = EVHelp.helptext[lctopic]
        print(text)
