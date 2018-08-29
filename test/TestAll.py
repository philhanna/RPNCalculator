#! /usr/bin/python3

import unittest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Evaluator import Evaluator
from TestArithmeticOperations import *
from TestLogFunctions import *
from TestPrintFunctions import *
from TestStackFunctions import *
from TestTrigonometricFunctions import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestArithmeticOperations)
    suite.addTest(TestLogFunctions)
    suite.addTest(TestPrintFunctions)
    suite.addTest(TestStackFunctions)
    suite.addTest(TestTrigonometricFunctions)
    return suite

if __name__ == '__main__':
    unittest.main()
