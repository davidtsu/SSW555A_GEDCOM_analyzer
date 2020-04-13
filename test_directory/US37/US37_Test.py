"""
User Story 37 - Test File

US37: List recent survivors
List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days.
@Author: David Tsu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from datetime import datetime
from prettytable import PrettyTable


class Test_US37(unittest.TestCase):
    """ Tests US37. Ensures that a list of multiple births is printed. """
    
    def test_US37_survivors(self):
        """ Tests US37. Ensures that a list of multiple births is printed. """

        # no deaths
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US37", "US37_none.ged")])
        self.assertEqual(g.user_story_37(), 'No individuals have died in the past 30 days.')
        
        # triplets
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US37", "US37_dead.ged")])
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Individual ID', 'Individual Name']
        pt.add_row(['@F1-US37-B@', '@I2-US37-B@', 'Mother /US37-B/'])
        pt.add_row(['@F2-US37-B@', '@I3-US37-B@', 'Sibling1 /US37-B/'])
        pt.add_row(['@F1-US37-B@', '@I4-US37-B@', 'Sibling2 /US37-B/'])
        pt.add_row(['@F1-US37-B@', '@I5-US37-B@', 'Sibling3 /US37-B/'])
        pt.add_row(['@F2-US37-B@', '@I7-US37-B@', 'Baby /US37-B/'])
        pt.sortby = 'Family ID'
        self.assertEqual(sorted(pt._rows), sorted(g.user_story_37()._rows))

        pass


if __name__ == "__main__":
    unittest.main(exit=False)
