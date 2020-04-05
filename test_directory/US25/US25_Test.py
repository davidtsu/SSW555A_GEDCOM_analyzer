"""
User Story 25 - Test File

US25: Unique first names in families
No more than one child with the same first name should appear in a family

@Author: Zephyr Zambrano

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US25(unittest.TestCase):
    """ Tests US25. Ensures that no more than one child with the same first name should appear in a family. """
    
    def test_US25_unique_first_names_in_families(self):
        """ Tests US25. Ensures that no more than one child with the same first name should appear in a family. """
        
        self.maxDiff == None

        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US25", "US25_Parents_Same_First_Name.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US25_unique_first_names_in_families()
        sys.stdout = sys.__stdout__
        output_str1 = "US25: Husband: Parent /LastnameUS25-1/ on GEDCOM line: 9 and wife: Parent /LastnameUS25-1/ on GEDCOM line 15 have the same first name.\n"
        self.assertEqual(capturedOutput.getvalue(), output_str1)

        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US25", "US25_Child_Same_First_Name.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US25_unique_first_names_in_families()
        sys.stdout = sys.__stdout__
        output_str1 = "US25: Child: Father /LastnameUS25-2/ on GEDCOM line: 3 has the same first name as another family member.\n"        
        self.assertEqual(capturedOutput.getvalue(), output_str1)

        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US25", "US25_No_Duplicate_First_Names.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US25_unique_first_names_in_families()
        sys.stdout = sys.__stdout__
        output_str1 = ""        
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)