"""
User Story 42 (US42) - Test File
US42: Reject illegitimate dates
@Author: Zephyr Zambrano

"""


import unittest
from ssw555a_ged import GED_Repo, Individual


class Test_US42(unittest.TestCase):
    """ Tests that the strip_date method rejects illegitimate dates by throwing ValueErrors. """

    def test_strip_date(self):
        """ Tests that strip_date rejects illegitimate dates by throwing a ValueError. """
        self.assertRaises(ValueError, GED_Repo.strip_date, self,"40 JAN 1990", line_number=0)
        self.assertRaises(ValueError, GED_Repo.strip_date, self,"1 DOG 1990", line_number=0)
        self.assertRaises(ValueError, GED_Repo.strip_date, self,"1 JAN -1", line_number=0)


if __name__ == "__main__":
    unittest.main(exit=False)
