"""
User Story 11 (US11) - Test File
US21: No Bigamy Test Cases
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US11(unittest.TestCase):
    """ Tests that husbands and wifes are not married twice at the same time. """

    def test_user_story_11(self):
        """ Tests that husbands and wifes are not married twice at the same time and prints out the cases if so"""
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US11', 'US11_no_bigamy.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_11()
        sys.stdout = sys.__stdout__
        output_str1 = '''US11 - Bledar /Hasa/ married twice on the same time on line 53
US11 - Ela /Zili/ married twice on the same time on line 62\n'''
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)