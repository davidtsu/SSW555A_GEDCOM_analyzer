"""
User Story 38 - Test File

US38: List upcoming birthdays
List all living people in a GEDCOM file whose birthdays occur in the next 30 days

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US38(unittest.TestCase):
    """ Tests US38. Ensures that upcoming birthdays are printed to the user. """
    
    def test_US38_upcoming_birthdays(self):
        """ Tests US38. Ensures that upcoming birthdays are printed to the user. """
        # upcoming birthday
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Upcoming_Birthdays.ged")])
        self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, [('Child /Lastname/', '04/18/2000')]), [('Child /Lastname/', '04/18/2000')])

        # no upcoming birthday
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_No_Upcoming_Birthdays.ged")])
        self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, []), "No upcoming birthdays.")

        # upcoming birthday, but person is dead so it does not count for this program
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Dead_Upcoming_Birthdays.ged")])
        self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, []), "No upcoming birthdays.")


if __name__ == "__main__":
    unittest.main(exit=False)