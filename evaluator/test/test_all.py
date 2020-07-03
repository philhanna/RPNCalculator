import unittest

from evaluator.test.test_arithmetic_operations import TestArithmeticOperations
from evaluator.test.test_log_functions import TestLogFunctions
from evaluator.test.test_print_functions import TestPrintFunctions
from evaluator.test.test_stack_functions import TestStackFunctions
from evaluator.test.test_trigonometric_functions import TestTrigonometricFunctions


def suite():
    """ Runs all the test cases in this package """
    suite = unittest.TestSuite()
    suite.addTest(TestArithmeticOperations)
    suite.addTest(TestLogFunctions)
    suite.addTest(TestPrintFunctions)
    suite.addTest(TestStackFunctions)
    suite.addTest(TestTrigonometricFunctions)
    return suite


if __name__ == '__main__':
    unittest.main()
