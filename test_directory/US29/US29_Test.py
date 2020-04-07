"""
User Story 38 - Test File

US29: List deceased
List all deceased individuals in a GEDCOM file

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US29(unittest.TestCase):
    """ Tests US29. """
    
    def test_US29_list_deceased(self):
        """ Tests US29. """
        # deceased
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US29", "US29_Deceased.ged")])
        self.assertEqual(g.US29_list_deceased()._rows, [['@I1@-US29-A@', 'Child /Lastname/']])

        # no deceased
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US29", "US29_No_Deceased.ged")])
        self.assertEqual(g.US29_list_deceased(), 'No deceased individuals.')


if __name__ == "__main__":
    unittest.main(exit=False)