"""
User Story 30 - Test File

US30: List List living married
List all living married people in a GEDCOM file

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US30(unittest.TestCase):
    """ Tests US30. Ensures that List living married are printed to the user. """
    
    def test_US30_living_married(self):
        """ Tests US30. Ensures that List living married are printed to the user. """
        # Married couple are alive
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US30", "US30_Living_couples.ged")])
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Living Husband Name', ' Living Wife Name']
        pt.add_row(['@F1-US30-B@', 'Jim /Joy_US30/', 'Smith /Jo_A/'])
        pt.sortby = 'Family ID'
        self.assertEqual(pt._rows, g.US30_living_married()._rows)

        # Married couple are not alive
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US30", "US30_No_Living_couples.ged")])
        self.assertEqual(g.US30_living_married(), 'No living married couples.')


if __name__ == "__main__":
    unittest.main(exit=False)
