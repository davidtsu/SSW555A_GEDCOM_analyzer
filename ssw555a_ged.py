"""
ssw555a_ged.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
file reader for GEDCOM files
"""
import os, math
from datetime import datetime
from prettytable import PrettyTable

class GED_Repo:
    """ stores data from a GEDCOM file """
    def __init__(self, in_file):
        """ constructor for GED_Repo, creates list of individuals and families """
        self.in_file = in_file
        self.individuals = dict()
        self.families = dict()

        try:
            # this will analyze all files in the input_files directory
            if in_file.endswith('.ged'):
                self.read_ged(self.in_file)
            else:
                print('Bad input file.')
        except FileNotFoundError as f:
            raise f
        except ValueError as v:
            raise v

    def read_ged(self, ip, sep=' '):
        """ For reading GEDCOM files """
        tags = {
            '0': {
                'VALID': {'NOTE', 'HEAD', 'TRLR'},
                'SWAP': {'INDI', 'FAM'}
            },
            '1': {
                'VALID': {'NAME', 'SEX', 'FAMC', 'FAMS', 'HUSB', 'WIFE', 'CHIL', 'BIRT', 'DEAT', 'MARR', 'DIV'},
                'SWAP': set()
            },
            '2': {
                'VALID': {'DATE'},
                'SWAP': set()
            }
        }

        try:
            # opens input file
            with open(ip, 'r') as fp_in:
                ind = Individual()
                i_flag = False
                fam = Family()
                f_flag = False

                for line in fp_in:
                    line = line.rstrip()
                    
                    if line:

                        # split each line at spaces
                        my_tuple = tuple(line.strip().split(sep, 2))

                        # non_blank_lines generator removes blank lines, might not need generator with this check in place.
                        if len(my_tuple) < 2:
                            raise ValueError(f'Line in {ip} has too few values. Please fix and try again.')

                        # renaming for sanity
                        level = my_tuple[0]
                        tag = my_tuple[1]
                        arg = '' if len(my_tuple) == 2 else my_tuple[2]

                        # level and tag checking
                        if level in tags.keys():
                            # if tag in dict
                            if tag in tags[level]['VALID']:
                                # check all individual tags here
                                if i_flag:
                                    if tag == 'NAME':
                                        ind.set_name(arg)
                                    elif tag == 'SEX':
                                        ind.set_gender(arg)
                                    elif tag == 'FAMC':
                                        ind.set_child(arg)
                                    elif tag == 'FAMS':
                                        ind.set_spouse(arg)
                                    elif tag == 'BIRT':
                                        # must read & parse next line for DOB
                                        line = next(fp_in)
                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag')
                                        else:
                                            d = self.strip_date(arg)
                                            ind.set_birthday(d)
                                            ind.set_alive(True)
                                            ind.set_age()
                                    elif tag == 'DEAT':
                                        # must read & parse next line for DOD
                                        line = next(fp_in)
                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag')
                                        else:
                                            d = self.strip_date(arg)
                                            ind.set_alive(False)
                                            ind.set_death(d)
                                            ind.set_age()
                                    else: #tag == 'DATE'
                                        raise ValueError(f'Unmatched DATE tag, please review {ip}.')

                                # check all family tags here
                                if f_flag:
                                    if tag == 'HUSB':
                                        fam.set_husb_id(arg)
                                        fam.set_husb_name(self.individuals[arg].name)
                                    elif tag == 'WIFE':
                                        fam.set_wife_id(arg)
                                        fam.set_wife_name(self.individuals[arg].name)
                                    elif tag == 'CHIL':
                                        fam.set_children(arg)
                                    elif tag == 'MARR':
                                        # 
                                        line = next(fp_in)
                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag')
                                        else:
                                            d = self.strip_date(arg)
                                            fam.set_married(d)
                                    elif tag == 'DIV':
                                        line = next(fp_in)
                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag')
                                        else:
                                            d = self.strip_date(arg)
                                            fam.set_divorced(d)
                                        pass
                                    else: # tag == DATE and tag == TRLR. Not sure what to do with TRLR, since it just marks EOF.
                                        if tag == 'DATE':
                                            raise ValueError(f'Unmatched DATE tag, please review {ip}.')

                            if arg in tags[level]['SWAP']:
                                # new individual/family starts here
                                # if old individual/family exists, save it to dictionary
                                if ind.iid != '':
                                    ind = self.add_individual(ind)
                                    i_flag = f_flag = False
                                if fam.fid != '':
                                    fam = self.add_family(fam)
                                    i_flag = f_flag = False

                                # starting new ind/fam
                                if arg == 'INDI':
                                    ind.set_iid(tag)
                                    i_flag = True
                                if arg == 'FAM':
                                    fam.set_fid(tag)
                                    f_flag = True

                # need to check once here for final individual/family item
                if ind.iid != '':
                    ind = self.add_individual(ind)
                    i_flag = f_flag = False
                if fam.fid != '':
                    fam = self.add_family(fam)
                    i_flag = f_flag = False

        # raise error if bad files.
        except ValueError as v:
            raise ValueError(f'Bad value. Please check {ip} for bad data: {v}')
        except FileNotFoundError:
            raise FileNotFoundError(f'Cannot open file. Please check {ip} exists and try again.')

    def add_individual(self, i):
        """ must pass in individual """
        self.individuals[i.iid] = i
        return Individual()

    def add_family(self, f):
        """ must pass in family """
        self.families[f.fid] = f
        return Family()

    def strip_date(self, arg):
        """ return datetime object
        throws error if illegitimate date is received """
        try:
            dt = datetime.strptime(arg, "%d %b %Y")
        except ValueError:
            raise ValueError("illegitimate date received")
        else:
            dt = datetime.strptime(arg, "%d %b %Y")
            return dt.strftime("%Y-%m-%d")

    def print_individuals(self):
        """ prints list of individuals using prettytable """
        pt = PrettyTable()
        pt.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
        for i in self.individuals.values():
            pt.add_row(i.get_values())
        print(pt)

    def print_families(self):
        """ prints list of families using prettytable """
        pt = PrettyTable()
        pt.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
        for f in self.families.values():
            pt.add_row(f.get_values())
        print(pt)

class Individual:
    """ stores info for a single individual """
    def __init__(self, iid = '', name = '', gender = '', birthday = '', age = 0, alive = True, death = 'NA', child = 'NA', spouse = 'NA'):
        """ constructor for Individual """
        self.iid = iid
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.alive = alive
        self.death = death
        self.child = child
        self.spouse = spouse

    def get_values(self):
        """ returns all values in individual as list for use in print """
        return [self.iid, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]

    def set_iid(self, i):
        """ sets new individual id (iid) """
        self.iid = i

    def set_name(self, n):
        """ sets new individual name """
        self.name = n

    def set_gender(self, g):
        """ sets new individual gender """
        self.gender = g
    
    def set_birthday(self, b):
        """ sets new individual birthday """
        self.birthday = b

    def set_age(self):
        """ sets new individual birthday 
        throws error if illegitimate date is received """
        if self.alive and self.death == 'NA':
            try:
                bd = datetime.strptime(self.birthday, "%Y-%m-%d")
            except ValueError:
                raise ValueError("illegitimate date received")
            else:
                bd = datetime.strptime(self.birthday, "%Y-%m-%d")
                cd = datetime.today()
                self.age = math.floor((cd - bd).days / 365.2425)
        else:
            if self.death == 'NA':
                raise f'{self.name} is either marked alive but has death or marked dead but has no death date.'
            else:
                try:
                    bd = datetime.strptime(self.birthday, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("illegitimate date received")
                try:
                    dd = datetime.strptime(self.death, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("illegitimate date received")
                else:
                    bd = datetime.strptime(self.birthday, "%Y-%m-%d")
                    dd = datetime.strptime(self.death, "%Y-%m-%d")
                    self.age = math.floor((dd - bd).days / 365.2425)
                    

    def set_alive(self, a):
        """ sets new individual living status """
        self.alive = a

    def set_death(self, d):
        """ sets new individual death date """
        self.death = d if d else 'NA'

    def set_child(self, c):
        """ adds child to individual's children """
        if isinstance(self.child, set):
            self.child = self.child | {c}
        else:
            self.child = {c} if (c and c != 'NA') else 'NA'
    
    def set_spouse(self, s):
        """ sets new individual spouse """
        if isinstance(self.spouse, set):
            self.spouse = self.spouse | {s}
        else:
            self.spouse = {s} if (s and s != 'NA') else 'NA'

class Family:
    """ stores info for a family """
    def __init__(self, fid = '', married = 'NA', divorced = 'NA', husb_id = '', husb_name = '', wife_id = '', wife_name = '', children = 'NA'):
        """ constructor for family """
        self.fid = fid
        self.married = married
        self.divorced = divorced
        self.husb_id = husb_id
        self.husb_name = husb_name
        self.wife_id = wife_id
        self.wife_name = wife_name
        self.children = children

    def get_values(self):
        """ returns all values in family for use in print """
        return [self.fid, self.married, self.divorced, self.husb_id, self.husb_name, self.wife_id, self.wife_name, self.children]

    def set_fid(self, i):
        """ sets new family id """
        self.fid = i

    def set_married(self, m):
        """ sets new family marriage date """
        self.married = m if m else 'NA'

    def set_divorced(self, d):
        """ sets new family divorce date """
        self.divorced = d if d else 'NA'

    def set_husb_id(self, h):
        """ sets new family husb_id """
        self.husb_id = h

    def set_husb_name(self, h):
        """ sets new family husb_name """
        self.husb_name = h

    def set_wife_id(self, w):
        """ sets new family wife_id """
        self.wife_id = w

    def set_wife_name(self, w):
        """ sets new family wife_name """
        self.wife_name = w

    def set_children(self, c):
        """ adds child to family's children """
        if isinstance(self.children, set):
            self.children = self.children | {c}
        else:
            self.children = {c} if (c and c != 'NA') else 'NA'

def main():
    """ for running GED reader. """

    # this will analyze all files in the input_files directory
    for file in [f for f in os.listdir(os.path.join(os.getcwd(), 'test_input_files')) if f.endswith('.ged')]:
        try:
            print(f'Creating GED_Repo for data in {file}')
            g = GED_Repo(os.path.join(os.getcwd(), 'test_input_files', file))
            g.print_individuals()
            g.print_families()
        except ValueError as v:
            print(v)
        except FileNotFoundError as f:
            print(f)
    else:
        print('No files found in test_input_files, or test_input_files not found.')

if __name__ == '__main__':
    main()