"""
User Story 38 - Test File

US39: List upcoming anniversaries
List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US39(unittest.TestCase):
    """ Tests that the methods that throw errors display the line number as part of the error message. """
    
    def test_US39_upcoming_anniversaries(self):
        """ Tests the methods in US39_upcoming_anniversaries """
        # upcoming anniversary
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_Upcoming_Anniversaries.ged")])
        self.assertEqual(g.US38_print_upcoming_anniversaries, [('04/18/1990', 'Husband: Father /Lastname/', 'Wife: Mother /Oldlastname/')])

        # no upcoming anniversary
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_No_Upcoming_Anniversaries.ged")])
        self.assertEqual(g.US38_print_upcoming_anniversaries, "No upcoming anniversaries.")

        # upcoming anniversary, but person is dead so it does not count for this program
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US39", "US39_Dead_Upcoming_Anniversaries.ged")])
        self.assertEqual(g.US38_print_upcoming_anniversaries, "No upcoming anniversaries.")


if __name__ == "__main__":
    unittest.main(exit=False)
