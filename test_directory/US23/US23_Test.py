"""
User Story 23 - Test File

US23: Unique name and birth date
No more than one individual with the same name and birth date should appear in a GEDCOM file

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US23(unittest.TestCase):
    """ Tests US23. """
    
    def test_US23_unique_name_and_birthdate(self):
        """ Tests US23. """
        # USE ASSERTRAISES, US 40 OR 42 FOR REFERENCE?
        
        # upcoming birthday
        # g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Upcoming_Birthdays.ged")])
        # self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, [('Child /Lastname/', '04/18/2000')]), [('Child /Lastname/', '04/18/2000')])

        # no upcoming birthday
        # g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_No_Upcoming_Birthdays.ged")])
        # self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, []), "No upcoming birthdays.")

        # upcoming birthday, but person is dead so it does not count for this program
        # g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US38", "US38_Dead_Upcoming_Birthdays.ged")])
        # self.assertEqual(GED_Repo.US38_print_upcoming_birthdays(self, []), "No upcoming birthdays.")


if __name__ == "__main__":
    unittest.main(exit=False)