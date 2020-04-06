"""
User Story 31 - Test File

US30: List living singles
List all living people over 31 who have never been married in a GEDCOM file

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family


class Test_US31(unittest.TestCase):
<<<<<<< HEAD
    """ Tests US31. Ensures that List living singles are printed to the user. """  
    def test_US31_living_single(self):

        # single(age<30) is died#
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_died_less30_single.ged")])
        self.assertEqual(GED_Repo.US31_print_living_single(self, []),"No one is over 30 and has never been married.")

        # single(age<30) is live#
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_liv_less30_single.ged")])
        self.assertEqual(GED_Repo.US31_print_living_single(self, []), "No one is over 30 and has never been married.")
            
        # single(age>30) is live#
=======
    """ Tests US31. Ensures that List living singles are printed to the user. """
    
    def test_US31_living_single(self):
        """ Tests US31. Ensures that List living singles are printed to the user. """
        # single(age<30) is died
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_died_less30_single.ged")])
        self.assertEqual(GED_Repo.US31_print_living_single(self, [],"No one is over 30 and has never been married.")

        # single(age<30) is live
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_liv_less30_single.ged")])
        self.assertEqual(GED_Repo.US31_print_living_single(self, []), "No one is over 30 and has never been married.")
        
        # single(age>30) is live
>>>>>>> 6edecca6e66b9fdc2790314905c6e90c9fa95a38
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US31", "US31_liv_over30_single.ged")])
        self.assertEqual(GED_Repo.US31_print_living_single(self, [('ID@I1-US31-A@', 'Name: Libo /Tim_us31/', 'Age: 31')])


if __name__ == "__main__":
    unittest.main(exit=False)
