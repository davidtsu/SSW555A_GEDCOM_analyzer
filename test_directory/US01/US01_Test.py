"""
User Story 01 (US01) - Test File
US01: Dates (birth, marriage, divorce, death) should not be after the current date
@Author: Xiaojun zhu
"""

class Test_user_story_01(unittest.TestCase):
    """ Tests that theuser_story_01 function throws when expected. """

    def test_check_user_story_01(self):
        """ Tests that user_story_01 rejects illegitimate Dates (birth, marriage, divorce, death) by throwing a ValueError. """

        # need following cases:
        # birthday after today
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US01', 'US01_birthday after today.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'Jim /Smith/ birthday before marriage on line 39\n'
        self.assertEqual(capturedOutput.getvalue(), output_str1)

    def test_check_bday2(self):
        """ Tests that check_bday rejects illegitimate birthdays by throwing a ValueError. """
        # birthday after divorce (after 9mo)
        g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', 'US08', 'US08_Birth_After_Divorce_Bad.ged'))
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        g.check_bday()
        sys.stdout = sys.__stdout__
        output_str1 = 'John /Smith/ birthday before marriage on line 21\n'
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