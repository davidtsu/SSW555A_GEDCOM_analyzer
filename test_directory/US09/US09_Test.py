"""
User Story 09 (US09) - Test File
US09: Birth before death of parents
@Author: David Tsu
"""

import unittest, os
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US09(unittest.TestCase):
    """ Tests that the check_bday function throws when expected. """

    def test_check_bday(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """

        # need following cases:

        # birth with both parents alive (success) (default)
        # should pass, unsure how to check this

        # birth after father's death, within 9 months (success)
        # should pass, unsure how to check this

        # birth after mother's death (failure)
        self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Mom.ged'))

        # birth after father's death, outside 9 months (failure)
        self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Dad.ged'))

if __name__ == "__main__":
    unittest.main(exit=False)
