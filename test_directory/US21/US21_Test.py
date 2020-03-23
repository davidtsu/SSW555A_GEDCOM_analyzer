"""
User Story 21 (US21) - Test File
US21: Correct gender test cases
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US21(unittest.TestCase):
    """ Tests that husbands have a male and wives have a female gender. """

    def test_user_story_21(self):
        """ Tests that set_age rejects illegitimate ages by throwing a ValueError. """
        # husband gender female and wife gender male (failure)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US21', 'correct_gender_test.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_21()
        sys.stdout = sys.__stdout__
        output_str1 = 'US21 - Bella /Smith/ gender is supposed to be female but is not on line 35\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)