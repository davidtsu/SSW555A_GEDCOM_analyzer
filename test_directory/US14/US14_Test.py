"""
User Story 14 (US14) - Test File
US14: No more than 5 multiple births Test Cases
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US14(unittest.TestCase):
    """ Tests that there are no more than 5 multiple births at the same time. """

    def test_user_story_14(self):
        """ Tests that there are no more than 5 multiple births at the same time and prints out the cases if so"""
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US14', 'US14_multiple_births.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_14()
        sys.stdout = sys.__stdout__
        output_str1 = '''US14 - @F1-US14-EK@ has more than 5 multiple childrens born in the same time.\n'''
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)