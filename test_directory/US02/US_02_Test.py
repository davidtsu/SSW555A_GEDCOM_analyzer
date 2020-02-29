"""
User Story 02 (US02) - Test File
US02: Individual birthday before marriage
@Author: Ejona Kocibelli
"""

import unittest, os, io, sys
from collections import Counter
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US02(unittest.TestCase):
    """ Tests that the user_story_2 function prints when person is married before they are born. """

    def test_user_story_2(self):
        """ Tests that user_story_2 rejects illegitimate marriages before birthdays. """

        # need following cases:

        # born before married
        # should pass, unsure how to check this

        # born after married
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US02', 'US_02_03.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_2()
        sys.stdout = sys.__stdout__
        output_str1 = '''Natalie /Jones/ birthday after marriage date on line 41
Bob /Johnson/ birthday after marriage date on line 31
Mary /Miller/ birthday after marriage date on line 110'''
        c1 = Counter(capturedOutput.getvalue())
        c2 = Counter(output_str1)
        us02_true = all(k in c1 and c1[k] >= c2[k] for k in c2)

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_3()
        sys.stdout = sys.__stdout__
        output_str2 = '''Ella /Moore/ birthday after death date on line 87
Diana /Brown/ birthday after death date on line 121'''
        c3 = Counter(capturedOutput.getvalue())
        c4 = Counter(output_str2)
        us03_true = all(k in c3 and c3[k] >= c4[k] for k in c4)

        self.assertTrue(us02_true and us03_true)        

        #self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_directory', 'US02', 'US_02_03.ged'))

if __name__ == "__main__":
    unittest.main(exit=False)
