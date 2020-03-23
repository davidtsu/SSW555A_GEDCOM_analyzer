"""
User Story 01 (US01) - Test File
US01: Dates (birth, marriage, divorce, death) should not be after the current date
@Author: Xiaojun zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_user_story_01(unittest.TestCase):
    """ Tests that theuser_story_01 function throws when expected. """

    def test_check_user_story_01(self):
        """ Tests that user_story_01 rejects illegitimate birth day by throwing a ValueError. """

        # need following cases:
        # birthday after today
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US01', 'US01_birthday_after_today.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_01()
        sys.stdout = sys.__stdout__
        output_str1 = 'US01 - Jaf /Jo1/ birthday after today on line 21\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_user_story_01_2(self):
        """ Tests that user_story_01 rejects illegitimate death day by throwing a ValueError. """
        # deathday after today
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US01', 'US01_deathday_after_today.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_01()
        sys.stdout = sys.__stdout__
        output_str1 = 'US01 - Jaf /Jo2/ death after today on line 23\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_user_story_01_3(self):
        """ Tests that user_story_01 rejects illegitimate marriage day by throwing a ValueError. """
        # marriage day before today
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US01', 'US01_marriage_after_today.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_01()
        sys.stdout = sys.__stdout__
        output_str1 = 'US01 - Jaf /Jo4/ marriage after today on line 37\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_user_story_01_4(self):
        """ Tests that user_story_01 rejects illegitimate divorce day by throwing a ValueError. """
        # birthday after divorce (within 9mo)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US01', 'US01_divorce_after_today.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_01()
        sys.stdout = sys.__stdout__
        output_str1 = 'US01 - Jim /Jo3/ divorce after today on line 39\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)