"""
User Story 40 (US40) - Test File
US40: Include input line numbers (when throwing errors)
@Author: Zephyr Zambrano

"""


import unittest
from ssw555a_ged import GED_Repo, Individual


class Test_Line_Numbers(unittest.TestCase):
    """ Tests that the methods that throw errors display the line number as part of the error message. """

    def test_strip_date(self):
        """ Tests that strip_date displays the correct error message with the expected line number. """
        with self.assertRaises(ValueError) as e:
            GED_Repo.strip_date(self,"40 JAN 1990", line_number=0).fail()
        self.assertEqual("illegitimate date received. GEDCOME line: 0", str(e.exception))


if __name__ == "__main__":
    unittest.main(exit=False)
