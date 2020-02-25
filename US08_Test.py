"""
User Story 08 (US08) - Test File
US08: Birth before marriage of parents
@Author: David Tsu
"""

import unittest, os
from ssw555a_ged import GED_Repo, Individual, Family

class Test_GED_Repo(unittest.TestCase):
    """ Tests that the strip_date method rejects illegitimate dates by throwing ValueErrors. """

    def test_check_bday(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """

        # need following cases:
        # birthday before marriage
        self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_input_files', 'US08_Birth_Before_Marriage.ged'))

        # birthday after divorce (within 9mo)
        # should pass, not sure how to check this
        
        # birthday after divorce (after 9mo)
        #self.assertRaises(ValueError, GED_Repo, os.path.join(os.getcwd(), 'test_input_files', 'US08_Birth_After_Divorce'))

if __name__ == "__main__":
    unittest.main(exit=False)
