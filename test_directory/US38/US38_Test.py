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
    
    def test_upcoming_birthdays(self):
        """ """
        pass

    def test_no_upcoming_birthdays(self):
        """ """
        # "No upcoming birthdays."
        pass


if __name__ == "__main__":
    unittest.main(exit=False)