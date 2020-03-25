"""
User Story 07 (US07) - Test File
US07: Less than 150 years old
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US07(unittest.TestCase):
    """ Tests that the set_ages function throws when person is over 150. """

    def test_set_age1(self):
        """ Tests that set_age rejects illegitimate ages by throwing a ValueError. """
        # person over 150 (failure)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US07', 'US07_Over_150.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_07()
        sys.stdout = sys.__stdout__
        output_str1 = 'US07 - Redmond /Mann3/ is age 159, which is over 150 years old, on line 24\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_set_age2(self):
        """ Tests that set_age rejects illegitimate ages by throwing a ValueError. """
        # person under 150 (success)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US07', 'US07_Under_150.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
