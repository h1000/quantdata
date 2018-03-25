import unittest
import numpy as np
from quantdata.util.func import num_peak_valley_pivots


class UtilFuncTestCase(unittest.TestCase):

    def test_NumPeakValleyPivots1(self):
        """测试数字波峰波谷"""
        l = [1,2,3,4,5,2,4,3,9,8,7,1,1,2]
        a = num_peak_valley_pivots(l,3,-3)
        r = np.array([-1,0,0,0,1,-1,0,0,1,0,0,0,0,1],dtype='i1')
        self.assertEqual(a.all(),r.all())

if __name__ == "__main__":
    unittest.main(verbosity=2)