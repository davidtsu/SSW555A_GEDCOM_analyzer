"""
User Story 15 (US15) - Test File
US15: Less than 15 siblings
@Author: Akshay Lavhagale
"""
import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US15(unittest.TestCase):
    """ There should be fewer than 15 siblings in a family """

    def test_user_story_15(self):
        """ Tests that There should be fewer than 15 siblings in a family """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US15', 'US15_less_than_15_siblings.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_15()
        sys.stdout = sys.__stdout__
        output_str1 = 'US15 - Bette /Mann5/ and Zepheniah /Mann5/ Family has 21 children on line 260\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
