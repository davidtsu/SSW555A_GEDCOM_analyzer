"""
ssw555a_ged.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
file reader for GEDCOM files
"""
import os
from prettytable import PrettyTable

class GED_Repo:
    """ stores data from a GEDCOM file """
    def __init__(self):
        """ constructor for GED_Repo, creates list of individuals and families """
        self.individuals = dict()
        self.families = dict()

    def print_individuals(self):
        """ prints list of individuals using prettytable """
        pt = PrettyTable()
        pt.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
        #for i in self.individuals.values():
        #    pt.add_row()
        pass

    def print_families(self):
        """ prints list of families using prettytable """
        pt = PrettyTable()
        pt.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
        pass

def read_ged(ip, op, sep=','):
    """ For reading GEDCOM files """
    tags = {
        '0': {
            'VALID': {'NOTE', 'HEAD', 'TRLR'},
            'SWAP': {'INDI', 'FAM'}
        },
        '1': {
            'VALID': {'NAME', 'SEX', 'FAMC', 'FAMS', 'HUSB', 'WIFE', 'CHIL', 'BIRT', 'DEAT', 'MARR', 'DIV'},
            'SWAP': set()   # not sure I need to make this, but in case of future extension I'll leave it.
        },
        '2': {
            'VALID': {'DATE'},
            'SWAP': set()
        }
    }

    try:
        # deletes old output file, if it exists
        if os.path.exists(op):
            os.remove(op)

        # opens input and output files
        with open(ip, 'r') as fp_in, open(op, 'x') as fp_out:
            for line in non_blank_lines(fp_in):
                # split each line at spaces
                my_tuple = tuple(line.strip().split(sep, 2))

                # non_blank_lines generator removes blank lines, might not need generator with this check in place.
                if len(my_tuple) < 2:
                    raise ValueError(f'Line in {ip} has too few values. Please fix and try again.')

                # renaming for sanity
                level = my_tuple[0]
                tag = my_tuple[1]
                arg = '' if len(my_tuple) == 2 else my_tuple[2]
                out_line = tuple()

                # level and tag checking
                if level in tags.keys():
                    # if tag in dict
                    if tag in tags[level]['VALID'] or arg in tags[level]['SWAP']:
                        # TODO: ADD MORE ANALYSIS HERE. ALL VALID LINES SHOULD FALL IN HERE.
                        out_line = (level, tag, 'Y', arg)
                    # tag or arg not in dict
                    else:
                        out_line = (level, tag, 'N', arg)
                # invalid level
                else:
                    out_line = (level, tag, 'N', arg)

                # write input and output lines to output file
                fp_out.write('--> ' + line + '\n')
                fp_out.write('<-- ' + '|'.join(out_line) + '\n')

    # raise error if bad files.
    except ValueError as v:
        raise ValueError(f'Bad value. Please check {ip} for bad data: {v}')
    except FileNotFoundError:
        raise FileNotFoundError(f'Cannot open files. Please check {ip} exists and try deleting {op} if it exists.')

def non_blank_lines(f):
    """ generator to remove empty lines, found somewhere on Google """
    # I have to use this because blank lines break my code
    for line in f:
        line = line.rstrip()
        if line:
            yield line

def main():
    """ for running GED reader. """
    # fetch user input
    in_file = input("Enter input GED file name (no extension): ")

    # file name manipulation
    out_file = in_file + '_out'
    in_file += '.ged'
    out_file += '.ged'
    ip = os.path.join(os.getcwd(), in_file)
    op = os.path.join(os.getcwd(), out_file)

    # read from ip, write to op
    try:
        read_ged(ip, op, ' ')
    except ValueError as v:
        print(v)
    except FileNotFoundError as f:
        print(f)

if __name__ == '__main__':
    main()