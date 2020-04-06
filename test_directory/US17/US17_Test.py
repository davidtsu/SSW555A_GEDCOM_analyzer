"""
User Story 17 (US17) - Test File
US17: Parents should not marry any of their children
@Author: Akshay Lavhagale
"""
import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US17(unittest.TestCase):
    """ Parents should not marry any of their children """

    def test_user_story_17(self):
        """ Tests that Parents should not marry any of their children """
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US17', 'US17_parents_should_not_marry_child.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_17()
        sys.stdout = sys.__stdout__
        output_str1 = 'US17 - Christine /Ponting/ and Brian /Ponting/ are married on line 52\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
