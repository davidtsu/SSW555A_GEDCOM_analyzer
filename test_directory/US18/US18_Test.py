"""
User Story 18 (US18) - Test File
US18: Siblings should not marry one another
@Author: Akshay Lavhagale
"""
import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US18(unittest.TestCase):
    """ Siblings should not marry one another """

    def test_user_story_15(self):
        """ Tests that Siblings should not marry one another """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US18', 'US18_siblings_should_not_marry.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_18()
        sys.stdout = sys.__stdout__
        output_str1 = 'US18 - Martin /Johnson/ and Kristen /Johnson/ are married on line 50\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
