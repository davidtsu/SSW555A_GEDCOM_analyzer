"""
User Story 19 (US19) - Test File
US19: first cousins should not get married
@Author: Akshay Lavhagale
""" 
import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US18(unittest.TestCase):
    """ first cousins should not get married """

    def test_user_story_19(self):
        """ Tests that first cousins should not get married """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US19', 'US19_first_cousins_should_not_marry_each_other.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_19()
        sys.stdout = sys.__stdout__
        output_str1 = 'US19 - Family @F5-US19-A@ is where first cousins are married\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
