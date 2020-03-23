"""
User Story 15 (US15) - Test File
US15: Fewer than 15 siblings
@Author: Akshay Lavhagale
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo


class Test_US15(unittest.TestCase):
    """ Tests that the user_story_15 function throws when expected. """

    def test_user_story_15(self):
        """ Tests that user_story_15 rejects illegitimate siblings by throwing a ValueError. """

        # need following cases:
        # Fewer than 15 siblings
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US15', 'ssw555a_input.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_15()
        sys.stdout = sys.__stdout__
        output_str1 = 'Bette /Mann/ and Zepheniah /Mann/ Family has 21 children on line 260\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
