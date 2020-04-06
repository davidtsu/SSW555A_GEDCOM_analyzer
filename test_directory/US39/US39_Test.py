"""
User Story 38 - Test File

US39: List upcoming anniversaries
List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US39(unittest.TestCase):
    """ Tests US39. Ensures that upcoming anniversaries are printed to the user. """
    
    def test_US39_upcoming_anniversaries(self):
        """ Tests US39. Ensures that upcoming anniversaries are printed to the user. """
        self.maxDiff = None

        # upcoming anniversary
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_Upcoming_Anniversaries.ged")])
        populated_pt = PrettyTable()
        populated_pt.field_names = ["Anniversary", "Husband", "Wife"]
        populated_pt.add_row(['04/18/1990', 'Father /LastnameUS39-1/', 'Mother /LastnameUS39-1/'])
        self.assertEqual(GED_Repo.US39_print_upcoming_anniversaries(self, [['04/18/1990', 'Father /LastnameUS39-1/', 'Mother /LastnameUS39-1/']]), [['04/18/1990', 'Father /LastnameUS39-1/', 'Mother /LastnameUS39-1/']])

        # empty pretty table for the last two tests
        empty_pt = PrettyTable()
        empty_pt.field_names = ["Anniversary", "Husband", "Wife"]

        # no upcoming anniversary
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_No_Upcoming_Anniversaries.ged")])
        self.assertEqual(GED_Repo.US39_print_upcoming_anniversaries(self, []), [])

        # upcoming anniversary, but person is dead so it does not count for this program
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_Dead_Upcoming_Anniversaries.ged")])
        self.assertEqual(GED_Repo.US39_print_upcoming_anniversaries(self, []), [])


if __name__ == "__main__":
    unittest.main(exit=False)
