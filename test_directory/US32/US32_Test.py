"""
User Story 32 - Test File

US32: List multiple births
List all multiple births in a GEDCOM file

@Author: David Tsu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from datetime import datetime
from prettytable import PrettyTable


class Test_US32(unittest.TestCase):
    """ Tests US32. Ensures that a list of multiple births is printed. """
    
    def test_US32_living_single(self):
        """ Tests US32. Ensures that a list of multiple births is printed. """
        # no multiple births
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US32", "US32_none.ged")])
        self.assertEqual(g.user_story_32(), 'No instances of multiple births.')
        
        # triplets
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US32", "US32_triplets.ged")])
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Individual ID', 'Individual Name', 'Individual Birthday']
        pt.add_row(['@F1-US32-B@', '@I3-US32-B@', 'Sibling1 /US32-B/', datetime(2020, 2, 1, 0, 0).strftime("%m/%d/%Y")])
        pt.add_row(['@F1-US32-B@', '@I4-US32-B@', 'Sibling2 /US32-B/', datetime(2020, 2, 1, 0, 0).strftime("%m/%d/%Y")])
        pt.add_row(['@F1-US32-B@', '@I5-US32-B@', 'Sibling3 /US32-B/', datetime(2020, 2, 1, 0, 0).strftime("%m/%d/%Y")])
        pt.sortby = 'Family ID'
        self.assertEqual(sorted(pt._rows), sorted(g.user_story_32()._rows))

        pass


if __name__ == "__main__":
    unittest.main(exit=False)
