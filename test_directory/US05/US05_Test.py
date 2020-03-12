"""
User Story 05 (US05) - Test File
US08: Birth before marriage of parents
@Author: Akshay Lavhagale
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_US05(unittest.TestCase):
    """ Tests that the user_story_5 function throws when expected. """

    def test_user_story_5(self):
        """ Tests that user_story_5 rejects illegitimate marriage by throwing a ValueError. """

        # need following cases:
        # marriage before death
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US05', 'US05_spr1.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_5()
        sys.stdout = sys.__stdout__
        output_str1 = 'US05 - Grey /Mann/ married after individual death date on line 161\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
