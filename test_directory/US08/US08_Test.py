"""
User Story 08 (US08) - Test File
US08: Birth before marriage of parents
@Author: David Tsu
"""

import unittest, os, io, sys
from ssw555a_ged import GED_Repo

class Test_US08(unittest.TestCase):
    """ Tests that the check_bday function throws when expected. """

    def test_check_bday1(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """

        # need following cases:
        # birthday before marriage
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US08', 'US08_Birth_Before_Marriage.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'US08 - Jim /Smith/ birthday before marriage on line 39\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday2(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birthday after divorce (after 9mo)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US08', 'US08_Birth_After_Divorce_Bad.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'US08 - John /Smith/ birthday before marriage on line 21\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday3(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birthday during marriage (normal case)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US08', 'US08_Birth_After_Marriage.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday4(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birthday after divorce (within 9mo)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US08', 'US08_Birth_After_Divorce_Good.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = ''
        self.assertEqual(capturedOutput.getvalue(), output_str1)

if __name__ == "__main__":
    unittest.main(exit=False)
