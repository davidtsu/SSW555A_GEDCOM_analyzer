"""
User Story 33 - Test File
US33: List all orphans
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US33(unittest.TestCase):
    """ Tests US33. Ensures that list all orphans. """
    
    def test_US33_orphans_list(self):
        """ Tests US33. Ensures that list all orphans. """
        # I tested my US11 Test File as I know there are no orphans.
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US11", "US11_no_bigamy.ged")])
        self.assertEqual(g.user_story_33(), 'No orphans.')
 
        # orphans
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US33", "US33_orphans.ged")])
        pt = PrettyTable()
        pt.field_names = ['ID', 'Name', 'Age']
        pt.add_row(['@I1-US33-EK@', 'Blerta /Methasani/', 17])
        pt.sortby = 'ID'
        self.assertEqual(pt._rows, g.user_story_33()._rows)

        pass


if __name__ == "__main__":
    unittest.main(exit=False)
