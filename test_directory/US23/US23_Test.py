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
        self.maxDiff = None

        # duplicate name and birthdate
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US23", "US23_Duplicate_Name_and_Birthdate.ged")])
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.US23_unique_name_and_birthdate()
        sys.stdout = sys.__stdout__
        output_str1 = "US23: Two people with the same name and birthdate: ('Firstname /Lastname/', '01/01/1950') on GEDCOM line: 9 and ('Firstname /Lastname/', '01/01/1950') on GEDCOM line 15.\n"        
        self.assertEqual(capturedOutput.getvalue(), output_str1)


if __name__ == "__main__":
    unittest.main(exit=False)