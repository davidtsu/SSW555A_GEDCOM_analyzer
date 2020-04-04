"""
User Story 24 (US24) - Test File
US24: checks that all families have unique spouse names and marriage date
@Author: David Tsu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_US24(unittest.TestCase):
    """ Tests that the check_user_story_24 function throws when expected. """

    def test_user_story_24(self):
        """ Tests that user_story_24 identifies all instances of families with non-unique spouse names and marriage date. """

        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US24', 'US24_Same_Spouses.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_24()
        sys.stdout = sys.__stdout__
        output_str1 = 'US24: @F2-US24-A@ family data appears at least twice with same spouses by name and the same marriage date on line 49\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US24', 'US24_Unique_Spouses.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_24()
        sys.stdout = sys.__stdout__
        output_str2 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str2)

if __name__ == "__main__":
    unittest.main(exit=False)
