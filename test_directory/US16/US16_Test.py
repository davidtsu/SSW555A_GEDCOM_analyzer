"""
User Story 16 - Test File

US16: Male last names
All male members of a family should have the same last name

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US16(unittest.TestCase):
    """ Tests US16. Ensures that all male family members have the same last name. """
    
    def test_US16_male_last_names(self):
        """ Tests US16. Ensures that all male family members have the same last name. """
        self.maxDiff == None

        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US16", "US16_Males_Same_Last_Names.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US16_male_last_names()
        sys.stdout = sys.__stdout__
        output_str1 = ""     
        self.assertEqual(capturedOutput.getvalue(), output_str1)


        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US16", "US16_Males_Different_Last_Names.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US16_male_last_names()
        sys.stdout = sys.__stdout__
        output_str1 = "US16: Male child: Child /DifferentLastnameUS16-1/ with ID: @I1@-US16-B@ on GEDCOM line: 3 has a differet last name than the family last name: LastnameUS16-1.\n"        
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)