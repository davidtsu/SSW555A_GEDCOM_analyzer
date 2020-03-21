"""
User Story 27 (US27) - Test File
US27: Include Individual Ages
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US27(unittest.TestCase):
    """ Tests that the set_ages function calculates age correctly. """

    def test_set_age1(self):
        """ Tests that set_age rejects illegitimate ages by throwing a ValueError. """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US27', 'US27_Set_Ages.ged')])
        self.assertEqual(g.individuals['@I1-US27-A@'].age, 35)
        self.assertEqual(g.individuals['@I2-US27-A@'].age, 40)

if __name__ == "__main__":
    unittest.main(exit=False)
