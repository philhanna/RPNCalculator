import os
import sys

from . import __path__ as path
sys.path[0:0] = map(os.path.abspath, path)
del path[:], path
