"""
User Story 31 - Test File

US30: List living singles
List all living people over 31 who have never been married in a GEDCOM file

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US31(unittest.TestCase):
    """ Tests US31. Ensures that List living singles are printed to the user. """
    
    def test_US31_living_single(self):
        """ Tests US31. Ensures that List living singles are printed to the user. """
        # single(age<30) is died
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_died_less30_single.ged")])
        self.assertEqual(g.US31_living_single(), 'No unmarried individuals over 30.')

        # single(age<30) is live
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_liv_less30_single.ged")])
        self.assertEqual(g.US31_living_single(), 'No unmarried individuals over 30.')
        
        # single(age>30) is live
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_liv_over30_single.ged")])
        pt = PrettyTable()
        pt.field_names = ['Unmarried Individual ID', 'Unmarried Individual Name']
        pt.add_row(['@I1-US31-A@', 'Libo /Tim_us31/'])
        pt.sortby = 'Unmarried Individual ID'
        self.assertEqual(pt._rows, g.US31_living_single()._rows)

        pass


if __name__ == "__main__":
    unittest.main(exit=False)
