import sys
import tempfile
from contextlib import contextmanager

tmp = tempfile.gettempdir()

__all__ = [
    'tmp',
]
