"""
User Story 21 (US21) - Test File
US21: Correct gender test cases
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US21(unittest.TestCase):
    """ Tests that husbands have a male and wives have a female gender. """

    def test_user_story_21(self):
        """ Tests that husband gender is male and wife gender female and prints out the cases if not"""
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US21', 'US21_correct_gender_test.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_21()
        sys.stdout = sys.__stdout__
        output_str1 = 'US21 - Bella /Smith1/ gender is supposed to be female but is not on line 35\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)