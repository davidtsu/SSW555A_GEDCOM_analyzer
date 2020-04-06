"""
User Story 30 - Test File

US30: List List living married
List all living married people in a GEDCOM file

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US30(unittest.TestCase):
    """ Tests US30. Ensures that List living married are printed to the user. """
    
    def test_US30_living_married(self):
        """ Tests US30. Ensures that List living married are printed to the user. """
        # Married couple are alive
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US30", "US30_Living_couples.ged")])
        self.assertEqual(GED_Repo.US30_print_living_married(self, [('living couple #1', 'Husband: Jim /Joy_US30/', 'Wife: Smith /Jo_A/')]))

        # Married couple are not alive
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US30", "US30_No_Living_couples.ged")])
        self.assertEqual(GED_Repo.US30_print_living_married(self, []), "Either wife or husband in married couples is died.")


if __name__ == "__main__":
    unittest.main(exit=False)
