"""
ssw555a_ged_Demo.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
to run all GEDCOM files in one reader object, for demo purposes.
"""

import os
from ssw555a_ged import GED_Repo, Individual, Family

def main():
    """ for running GED reader. """

    file_list = []
    # this will analyze all files in the input_files directory
    for folder in [x for x in os.listdir(os.path.join(os.getcwd(), 'test_directory')) if os.path.isdir(os.path.join(os.getcwd(), 'test_directory', x))]:
        try:
            print(f'Reading files in {folder}')
            file_list = file_list + [os.path.join(os.getcwd(), 'test_directory', folder, f) for f in os.listdir(os.path.join(os.getcwd(), 'test_directory', folder)) if f.endswith('.ged')]
        except ValueError as v:
            print(v)
        except FileNotFoundError as f:
            print(f)

    try:
        print(f'Analyzing final cumulative file data.')
        print(file_list)
        g = GED_Repo(file_list)
        g.check_data()
        g.print_data()
        g.print_individuals()
        g.print_families()
    except ValueError as v:
        print(v)
    except FileNotFoundError as f:
        print(f)


if __name__ == '__main__':
    main()
