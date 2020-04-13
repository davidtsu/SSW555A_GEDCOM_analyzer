"""
User Story 30 - Test File

US28: List siblings by age
List siblings in families by decreasing age, i.e. oldest siblings first

@Author: xiaojun zhu

"""


import unittest, os, io, sys
from ssw555a_ged import GED_Repo, Individual, Family
from prettytable import PrettyTable


class Test_US28(unittest.TestCase):
    """ Tests US28. Ensures that List siblingss are printed to the user. """
    
    def test_US28_Siblings_by_age(self):
        """ Tests US28. Ensures that List siblingss are printed to the user. """
        # US28_3childrens_1died
        g = GED_Repo([os.path.join(os.getcwd(), "test_directory", "US28", "US28_3children_1died.ged")])
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Siblings in family(sort)']
        pt.add_row(['@F2_US28_B@',{'Cherry /Ponting/': '05 Dec 1985', 'Honor /Ponting/': '05 Oct 1986', 'Apple /Ponting/': '11 Jun 1990'}])
        pt.sortby = 'Family ID'
        self.assertEqual(pt._rows, g.US28_Siblings_by_age()._rows)




if __name__ == "__main__":
    unittest.main(exit=False)
