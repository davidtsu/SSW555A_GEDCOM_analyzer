"""
User Story 38 - Test File

US38: List upcoming birthdays
List all living people in a GEDCOM file whose birthdays occur in the next 30 days

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US38(unittest.TestCase):
    """ Tests that the methods that throw errors display the line number as part of the error message. """
    
    def test_US38_upcoming_birthdays(self):
        """ Tests the methods in US38_upcoming_birthdays """
        # upcoming birthday
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Upcoming_Birthdays.ged")])
        self.assertEqual(g.US38_print_upcoming_birthdays, [('Child /Lastname/', '04/18/2020')])

        # no upcoming birthday
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_No_Upcoming_Birthdays.ged")])
        self.assertEqual(g.US38_print_upcoming_birthdays, "No upcoming birthdays.")

        # upcoming birthday, but person is dead so it does not count for this program
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Dead_Upcoming_Birthdays.ged")])
        self.assertEqual(g.US38_print_upcoming_birthdays, "No upcoming birthdays.")


if __name__ == "__main__":
    unittest.main(exit=False)