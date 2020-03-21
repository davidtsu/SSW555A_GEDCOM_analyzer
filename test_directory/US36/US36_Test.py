"""
User Story 36 (US36) - Test File
US36: List all people in a GEDCOM file who died in the last 30 days
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US36(unittest.TestCase):
    """ Tests thatList all people in a GEDCOM file who died in the last 30 days. """

    def test_check_user_story_36(self):
        """ Tests that user_story_36 list who died in last 30 days. """

        # need following cases:
        # deathday within 30days 
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US36', 'US36_recent_births.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_36()
        sys.stdout = sys.__stdout__
        output_str1 = 'us36-Jaf /Jo/ were died in the last 30 days on line 15\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
