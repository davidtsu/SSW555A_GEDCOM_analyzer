"""
User Story 07 (US07) - Test File
US09: Less than 150 years old
@Author: David Tsu, Zephyr Zambrano, Xiaojun Zhu
"""

import unittest, os
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US07(unittest.TestCase):
    """ Tests that the set_ages function throws when person is over 150. """

    def test_check_bday(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """

        # need following cases:

        # person under 150 (success)
        # should pass, unsure how to check this

        # person over 150 (failure)
        self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_directory', 'US07', 'US07_Over_150.ged'))

if __name__ == "__main__":
    unittest.main(exit=False)
