"""
User Story 36 (US36) - Test File
US36: List all people in a GEDCOM file who died in the last 30 days
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from datetime import datetime
from prettytable import PrettyTable

class Test_US36(unittest.TestCase):
    """ List all people in a GEDCOM file who died in the last 30 days. """

    def test_check_user_story_36(self):
        """ Tests that user_story_36 list who died in last 30 days. """

        # need following cases:
        # deathday within 30days 
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US36', 'US36_recent_deaths.ged')])
        pt = PrettyTable()
        pt.field_names = ['Individual ID', 'Individual Name', 'Individual Death Date']
        pt.add_row(['@I1-US36-A@', 'Jaf /Jo7/', '03/31/2020'])
        self.assertEqual(g.user_story_36()._rows, pt._rows)

if __name__ == "__main__":
    unittest.main(exit=False)