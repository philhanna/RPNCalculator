""" Expression evaluator """


def get_version():
    import re
    import subprocess
    version = None
    cp = subprocess.run(['pip', 'show', 'RPNCalculator'], stdout=subprocess.PIPE)
    if cp.returncode == 0:
        output = str(cp.stdout, encoding='utf-8')
        for token in output.split('\n'):
            m = re.match(r'^Version: (.*)', token)
            if m:
                version = m.group(1)
                break
    return version


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


from .ev import Evaluator, EXIT
from .ev_help import EVHelp

__all__ = [
    'get_version',
    'stack_needs',
    'EVHelp',
    'Evaluator',
    'EXIT',
]
