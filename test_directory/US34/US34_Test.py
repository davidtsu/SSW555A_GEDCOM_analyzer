"""
User Story 34 - Test File

US34: List large age differences
List all couples who were married when the older spouse was more than twice as old as the younger spouse

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US34(unittest.TestCase):
    """ Tests US34. Ensures that List all couples who were married when the older spouse are printed to the user. """
    
    def test_US34_Twice_age_diff(self):
        """ Tests US34. Ensures that List all couples who were married when the older spouse are printed to the user.  """
        # US34_test_married_diff
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US34", "US34_test_married_diff.ged")])
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Twice age diff married spouse']
        pt.add_row(['@F1_US34_A@',('Limod /Desimy/', 'Simoy /Camd/')])
        pt.sortby = 'Family ID'
        self.assertEqual(pt._rows, g.US34_Twice_age_diff()._rows)




if __name__ == "__main__":
    unittest.main(exit=False)
