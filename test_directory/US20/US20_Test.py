"""
User Story 20 (US20) - Test File
US20: people should not marry their aunt or uncle
@Author: Akshay Lavhagale
"""
import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US20(unittest.TestCase):
    """ people should not marry their aunt or uncle """

    def test_user_story_20(self):
        """ Tests that people should not marry their aunt or uncle """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US20', 'US20_aunts_uncles_should_not_marry_nephew_niece.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_20()
        sys.stdout = sys.__stdout__
        output_str1 = 'US20 - Family @F4-US20-A@ has someone married to their uncle\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
