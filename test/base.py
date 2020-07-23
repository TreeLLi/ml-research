import unittest
import os, sys

import torch as tc
import numpy as np

curr_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(curr_path, "..")

if root_path not in sys.path:
    sys.path.insert(0, root_path)

class TestBase(unittest.TestCase):
    def assertEqual(self, first, second, msg=None):
        first = sanitized(first)
        second = sanitized(second)
        super(TestBase, self).assertEqual(first, second, msg)

def sanitized(x):
    x = x.tolist() if isinstance(x, tc.Tensor) or isinstance(x, np.ndarray) else x
    return x
        
def run_test():
    unittest.main()
