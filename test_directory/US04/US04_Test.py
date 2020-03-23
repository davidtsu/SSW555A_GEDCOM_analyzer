"""
User Story 04 (US04) - Test File
US04: Marriage before divorce
@Author: Akshay Lavhagale
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US04(unittest.TestCase):
    """ Tests that the user_story_4 function throws when expected. """

    def test_user_story_4(self):
        """ Tests that user_story_4 rejects illegitimate marriage by throwing a ValueError. """

        # need following cases:
        # Marriage before divorce
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US04', 'ssw555a_input.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_4()
        sys.stdout = sys.__stdout__
        output_str1 = 'US04 - Jodie /John/ and Jimmy /John/ married after divorce on line 22\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
