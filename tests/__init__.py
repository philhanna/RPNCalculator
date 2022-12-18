import sys
import tempfile
from contextlib import contextmanager

tmp = tempfile.gettempdir()


# redirect stdout technique from https://www.python.org/dev/peps/pep-0343/

@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


@contextmanager
def stdin_redirected(new_stdin):
    save_stdin = sys.stdin
    sys.stdin = new_stdin
    try:
        yield None
    finally:
        sys.stdin = save_stdin


__all__ = [
    'tmp', 'stdout_redirected', 'stdin_redirected',
]
