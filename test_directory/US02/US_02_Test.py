"""
User Story 02 (US02) - Test File
US02: Individual birthday before marriage
@Author: Ejona Kocibelli
"""

import unittest, os
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US07(unittest.TestCase):
    """ Tests that the user_story_2 function prints when person is married before they are born. """

    def test_set_age(self):
        """ Tests that user_story_2 rejects illegitimate marriages before birthdays. """

        # need following cases:

        # born before married
        # should pass, unsure how to check this

        # born after married
        self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_directory', 'US02', 'US_02_03.ged'))

if __name__ == "__main__":
    unittest.main(exit=False)
