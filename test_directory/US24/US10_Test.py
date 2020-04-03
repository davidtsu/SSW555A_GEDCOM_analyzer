"""
User Story 10 (US10) - Test File
US10: check Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
@Author: Xiaojun zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_user_story_10(unittest.TestCase):
    """ Tests that the check_user_story_10 function throws when expected. """

    def test_user_story_10(self):
        """ Tests that check_bday rejects illegitimate Marriage days by throwing a ValueError. """

        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US10', 'US10_Marriage_Before_14.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_2()
        sys.stdout = sys.__stdout__
        output_str1 = 'US10 - Jodie /Hooke/ was less than 14 years old at time of marriage on line 30\nUS10 - Captain /Hooke/ was less than 14 years old at time of marriage on line 21\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
