"""
User Story 35 (US35) - Test File
US35: List all people in a GEDCOM file who were born in the last 30 days
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from datetime import datetime

class Test_US35(unittest.TestCase):
    """ Tests that List all people in a GEDCOM file who were born in the last 30 days. """

    def test_check_user_story_35(self):
        """ Tests that user_story_35 list birth day in last 30 days. """

        # need following cases:
        # birthday within 30days 
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US35', 'US35_recent_births.ged')])
        self.assertEqual(g.user_story_35()._rows, [['@I1-US35-A@', 'Emith /Ohou/', datetime(2020, 3, 30, 0, 0).strftime("%m/%d/%Y")]])

if __name__ == "__main__":
    unittest.main(exit=False)