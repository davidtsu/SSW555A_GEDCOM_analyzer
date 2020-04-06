"""
User Story 12 (US12) - Test File
US21: No huge gap difference between father and child (<80) and mother and child (<60)
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US12(unittest.TestCase):
    """ Tests that there is no huge gap difference between father and child (<80) and mother and child (<60) """

    def test_user_story_12(self):
        """ Tests that there is no huge gap difference between father and child (<80) and mother and child (<60)  and prints out the cases if so"""
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US12', 'US12_parents_not_too_old.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_12()
        sys.stdout = sys.__stdout__
        output_str1 = '''US12 - Rahim /Kaleci/ is 80 years older than his child on line 18
US12 - Sevdia /Meta/ is 60 years older than his child on line 27\n'''
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)