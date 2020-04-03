"""
User Story 13 (US13) - Test File
US13: Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
@Author: David Tsu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_US13(unittest.TestCase):
    """ Tests that the US13 function throws when expected. """

    def test_user_story_13(self):
        """ Tests that US13 function rejects bad sibling birthdays. """
        self.maxDiff=None
        # need following cases:
        # siblings born >8mo apart (good)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US13', 'US13_Sibling_Spacing_3.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_13()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

        # siblings born <2 days apart (good)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US13', 'US13_Sibling_Spacing_1.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_13()
        sys.stdout = sys.__stdout__
        output_str2 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str2)

        # siblings born between 2days and 8mo apart (bad)
        g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', 'US13', 'US13_Sibling_Spacing_2.ged')])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.user_story_13()
        sys.stdout = sys.__stdout__
        output_arr3 = {'US13 - Sibling1 /US13-B/ and Sibling2 /US13-B/ have birthdays that are too close together on lines 18 and 24',
'US13 - Sibling2 /US13-B/ and Sibling3 /US13-B/ have birthdays that are too close together on lines 24 and 30',
'US13 - Sibling1 /US13-B/ and Sibling3 /US13-B/ have birthdays that are too close together on lines 18 and 30'}
        self.assertEqual(set([x for x in capturedOutput.getvalue().split('\n') if x != '']), output_arr3)

if __name__ == "__main__":
    unittest.main(exit=False)
