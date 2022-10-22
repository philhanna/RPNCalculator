""" Expression evaluator """
import re

from .ev_help import EVHelp
from .ev import Evaluator, EXIT


def get_version():
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


__all__ = [
    'get_version',
    'EVHelp',
    'Evaluator',
    'EXIT',
]
