"""
User Story 06 (US06) - Test File
US08: Birth before marriage of parents
@Author: Akshay Lavhagale
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo


class Test_US06(unittest.TestCase):
    """ Tests that the user_story_6 function throws when expected. """

    def test_user_story_6(self):
        """ Tests that user_story_6 rejects illegitimate marriage by throwing a ValueError. """

        # need following cases:
        # divorce before death
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US06', 'US06_spr1.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_6()
        sys.stdout = sys.__stdout__
        output_str1 = 'US06 - Olivia /Mann/ divorce after individual death date on line 183\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)
