"""
User Story 09 (US09) - Test File
US09: Birth before death of parents
@Author: David Tsu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family

class Test_US09(unittest.TestCase):
    """ Tests that the check_bday function throws when expected. """

    def test_check_bday1(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birth after mother's death (failure)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Mom_Bad.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'Jimmy /John/ birthday after mom death date on line 21\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday2(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birth after father's death, outside 9 months (failure)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Dad_Bad.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'Jimmy /John/ birthday after dads death date on line 21\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)
    
    def test_check_bday3(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birth with both parents alive (success) (default)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Dad_Good.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday4(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birth after father's death, within 9 months (success)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US09', 'US09_Birth_After_Death_Mom_Good.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
