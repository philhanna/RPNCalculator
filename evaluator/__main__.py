import argparse

from evaluator import Evaluator, get_version

parser = argparse.ArgumentParser(description="""
`ev` is an interactive programmable RPN calculator.  (Enter "help RPN"
for details about Reverse Polish Notation.)  It reads blank-delimited 
tokens from the input stream and interprets them one at a time using 
a syntax inspired by the FORTH programming language.  Anything following 
a '#' on an input line is considered a comment.

Besides simple calculations, ev supports variables, constants, and 
function definitions.  It also allows save and restore operations.

For help on an individual topic, enter "help <topic name>".

To see a list of topics, enter "help topics".

To exit from ev, enter "q"
""")
parser.add_argument('-v', '--version', action='version', version=f"{get_version()}", help='display version number')
parser.add_argument('-c', help='Execute commands before entering main loop')
parser.add_argument('--noprofile', action='store_true',
                    help='Do not load profile from .evrc')
args = parser.parse_args()
ev = Evaluator(debug=False)
ev.run(args)
