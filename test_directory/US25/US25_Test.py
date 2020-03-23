"""
User Story 25 - Test File

US25: Unique first names in families
No more than one child with the same name and birth date should appear in a family

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US25(unittest.TestCase):
    """ Tests US25. """
    
    def test_US25_unique_first_names_in_families(self):
        """ Tests US25. """
        pass


if __name__ == "__main__":
    unittest.main(exit=False)