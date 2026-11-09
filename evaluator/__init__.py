EXIT = "EXIT"


def get_version():
    from importlib.metadata import version, PackageNotFoundError
    try:
        return version('RPNCalculator')
    except PackageNotFoundError:
        return None


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

from .stack_entry import StackEntry, NumberEntry, BooleanEntry, HexEntry
TRUE = BooleanEntry(True)
FALSE = BooleanEntry(False)
from .ev import Evaluator
from .ev_help import EVHelp

__all__ = [
    'StackEntry',
    'NumberEntry',
    'BooleanEntry',
    'HexEntry',
    'TRUE',
    'FALSE',
    'get_version',
    'stack_needs',
    'EVHelp',
    'Evaluator',
    'EXIT',
]
