"""
ssw555a_ged.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
file reader for GEDCOM files
"""
import os, math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable

class GED_Repo:
    """ stores data from a GEDCOM file """
    def __init__(self, in_file):
        """ constructor for GED_Repo, creates list of individuals and families """
        self.in_file = in_file
        self.individuals = dict()
        self.families = dict()

        try:
            if in_file.endswith('.ged'):
                # read data
                self.read_ged(self.in_file)

                # finish calculating data
                self.set_ages()

                # check data
                self.check_bday()

                # printing data
                # e.g. US35 - list recent births
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

        line_number = 1

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
                            raise ValueError(f'Line in {ip} has too few values. Please fix and try again. GEDCOM line: {line_number}')

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
                                        ind.set_name(arg, line_number)
                                    elif tag == 'SEX':
                                        ind.set_gender(arg, line_number)
                                    elif tag == 'FAMC':
                                        ind.set_child(arg, line_number)
                                    elif tag == 'FAMS':
                                        ind.set_spouse(arg, line_number)
                                    elif tag == 'BIRT':
                                        # must read & parse next line for DOB
                                        line = next(fp_in)
                                        line_number = line_number + 1

                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]

                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            ind.set_birthday(d, line_number)
                                            ind.set_alive(True, line_number)
                                            #ind.set_age(line_number)
                                    elif tag == 'DEAT':
                                        # must read & parse next line for DOD
                                        line = next(fp_in)
                                        line_number = line_number + 1

                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]

                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            ind.set_alive(False, line_number)
                                            ind.set_death(d, line_number)
                                            #ind.set_age(line_number)
                                    else: #tag == 'DATE'
                                        raise ValueError(f'Unmatched DATE tag, please review {ip}. GEDCOM line: {line_number}')

                                # check all family tags here
                                if f_flag:
                                    if tag == 'HUSB':
                                        fam.set_husb_id(arg, line_number)
                                        fam.set_husb_name(self.individuals[arg].name, line_number)
                                    elif tag == 'WIFE':
                                        fam.set_wife_id(arg, line_number)
                                        fam.set_wife_name(self.individuals[arg].name, line_number)
                                    elif tag == 'CHIL':
                                        fam.set_children(arg, line_number)
                                    elif tag == 'MARR':
                                        line = next(fp_in)
                                        line_number = line_number + 1

                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]

                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            fam.set_married(d, line_number)
                                    elif tag == 'DIV':
                                        line = next(fp_in)
                                        line_number = line_number + 1

                                        my_tuple = tuple(line.strip().split(sep, 2))
                                        level = my_tuple[0]
                                        tag = my_tuple[1]
                                        arg = '' if len(my_tuple) == 2 else my_tuple[2]

                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            fam.set_divorced(d, line_number)
                                    else: # tag == DATE and tag == TRLR. Not sure what to do with TRLR, since it just marks EOF.
                                        if tag == 'DATE':
                                            raise ValueError(f'Unmatched DATE tag, please review {ip}. GEDCOM line: {line_number}')

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
                                    ind.set_iid(tag, line_number)
                                    i_flag = True
                                if arg == 'FAM':
                                    fam.set_fid(tag, line_number)
                                    f_flag = True

                    line_number = line_number + 1

                # need to check once here for final individual/family item
                if ind.iid != '':
                    ind = self.add_individual(ind)
                    i_flag = f_flag = False
                if fam.fid != '':
                    fam = self.add_family(fam)
                    i_flag = f_flag = False

        # raise error if bad files.
        except ValueError as v:
            raise ValueError(f'Bad value. Please check {ip} for bad data: {v}. GEDCOM line: {line_number}')
        except FileNotFoundError:
            raise FileNotFoundError(f'Cannot open file. Please check {ip} exists and try again. GEDCOM line: {line_number}')

    def add_individual(self, i):
        """ must pass in individual """
        self.individuals[i.iid] = i
        return Individual()

    def add_family(self, f):
        """ must pass in family """
        self.families[f.fid] = f
        return Family()

    def check_bday(self):
        """ iterates through family dictionary, finding birthday issues
        1. US08 - checks birthday after marriage, before divorce
        2. US09 - checks birthday before parent's death
        """
        for fam in self.families.values():
            if fam.children != 'NA':
                # fam.children is either a set or 'NA' string
                for child in fam.children:
                    bday = self.individuals[child].birthday
                    marr = fam.married
                    div = fam.divorced

                    # if child is born before marriage date, and not yet divorced
                    if marr != 'NA' and bday < marr and div == 'NA':
                        raise ValueError(f'Individual birthday before marriage on line {self.individuals[child]._birthday_line}')
                    # if child is born more than 9 months after divorce
                    if div != 'NA' and bday > div + relativedelta(months=9):
                        raise ValueError(f'Individual birthday before marriage on line {self.individuals[child]._birthday_line}')

                    if fam.husb_id and fam.wife_id:
                        dad = self.individuals[fam.husb_id]
                        mom = self.individuals[fam.wife_id]
                        # if child is born any time after mother dies
                        if not mom.alive and mom.death < bday:
                            raise ValueError(f'Individual birthday after mom death date on line {self.individuals[child]._birthday_line}')
                        # if child dies later than nine months after father dies
                        if not dad.alive and dad.death + relativedelta(months=9) < bday:
                            raise ValueError(f'Individual birthday after dads death date on line {self.individuals[child]._birthday_line}')
                    else:
                        raise ValueError(f'Individual does not have both a mother and a father, on line {self.individuals[child]._birthday_line}')
    
    def set_ages(self):
        """ sets ages of individuals in individual_table """
        for i in self.individuals.values():
            i.set_age(i._age_line)
    
    def strip_date(self, arg, line_number=0):
        """ return datetime object
        throws error if illegitimate date is received 
        part of US42 """
        try:
            dt = datetime.strptime(arg, "%d %b %Y")
            return dt
        except ValueError:
            raise ValueError(f"illegitimate date received. GEDCOM line: {line_number}")
        else:
            return 'NA'

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
        self.iid = iid              # string
        self._iid_line = 0

        self.name = name            # string
        self._name_line = 0

        self.gender = gender        # string
        self._gender_line = 0

        self.birthday = birthday    # datetime object
        self._birthday_line = 0

        self.age = age              # int
        self._age_line = 0

        self.alive = alive          # bool
        self._alive_line = 0

        self.death = death          # datetime object
        self._death_line = 0

        self.child = child          # set
        self._child_lines = set()

        self.spouse = spouse        # set
        self._spouse_lines = set()

    def get_values(self):
        """ returns all values in individual as list for use in print """
        b = 'NA' if self.birthday == 'NA' or self.birthday == '' else self.birthday.strftime("%Y-%m-%d")
        d = 'NA' if self.death == 'NA' or self.death == '' else self.death.strftime("%Y-%m-%d")
        return [self.iid, self.name, self.gender, b, self.age, self.alive, d, self.child, self.spouse]

    def set_iid(self, i, line_number=0):
        """ sets new individual id (iid) """
        self.iid = i
        self._iid_line = line_number

    def set_name(self, n, line_number=0):
        """ sets new individual name """
        self.name = n
        self._name_line = line_number

    def set_gender(self, g, line_number=0):
        """ sets new individual gender """
        self.gender = g
        self._gender_line = line_number
    
    def set_birthday(self, b, line_number=0):
        """ sets new individual birthday """
        self.birthday = b
        self._birthday_line = line_number
        self._age_line = line_number

    def set_age(self, line_number=0):
        """ sets new individual age 
        throws error if illegitimate date is received
        part of US42 """
        self._age_line = line_number
        if self.alive and self.death == 'NA':
            bd = self.birthday
            cd = datetime.today()
            self.age = math.floor((cd - bd).days / 365.2425)
        else:
            if self.death == 'NA':
                raise f'{self.name} is either marked alive but has death or marked dead but has no death date. GEDCOM line: {line_number}'
            else:
                bd = self.birthday
                dd = self.death
                self.age = math.floor((dd - bd).days / 365.2425)
        if self.age >= 150:
            raise ValueError(f'{self.name} is age {self.age} over 150 years old, on line {line_number}')
                    
    def set_alive(self, a, line_number=0):
        """ sets new individual living status """
        self.alive = a
        self._alive_line = line_number

    def set_death(self, d, line_number=0):
        """ sets new individual death date """
        self.death = d
        self._death_line = line_number
        self._age_line = line_number

    def set_child(self, c, line_number=0):
        """ adds child to individual's children """
        if isinstance(self.child, set):
            self.child = self.child | {c}
            self._child_line = self._child_line | {line_number}
        else:
            self.child = {c} if (c and c != 'NA') else 'NA'
            self._child_line = {line_number}
    
    def set_spouse(self, s, line_number=0):
        """ sets new individual spouse """
        if isinstance(self.spouse, set):
            self.spouse = self.spouse | {s}
            self._spouse_lines = self._spouse_lines | {line_number}
        else:
            self.spouse = {s} if (s and s != 'NA') else 'NA'
            self._spouse_lines = {line_number}

class Family:
    """ stores info for a family """
    def __init__(self, fid = '', married = 'NA', divorced = 'NA', husb_id = '', husb_name = '', wife_id = '', wife_name = '', children = 'NA'):
        """ constructor for family """
        self.fid = fid                  # string
        self._fid_line = 0

        self.married = married          # datetime object
        self._married_line = 0

        self.divorced = divorced        # datetime object
        self._divorced_line = 0

        self.husb_id = husb_id          # string
        self._husb_id_line = 0

        self.husb_name = husb_name      # string
        self._husb_name_line = 0

        self.wife_id = wife_id          # string
        self._wife_id_line = 0

        self.wife_name = wife_name      # string
        self._wife_name_line = 0

        self.children = children        # set
        self._children_lines = set()

    def get_values(self):
        """ returns all values in family for use in print """
        m = 'NA' if self.married == 'NA' else self.married.strftime("%Y-%m-%d")
        d = 'NA' if self.divorced == 'NA' else self.divorced.strftime("%Y-%m-%d")
        return [self.fid, m, d, self.husb_id, self.husb_name, self.wife_id, self.wife_name, self.children]

    def set_fid(self, i, line_number=0):
        """ sets new family id """
        self.fid = i
        self._fid_line = line_number

    def set_married(self, m, line_number=0):
        """ sets new family marriage date """
        self.married = m if m else 'NA'
        self._married_line = line_number

    def set_divorced(self, d, line_number=0):
        """ sets new family divorce date """
        self.divorced = d if d else 'NA'
        self._divorced_line = line_number

    def set_husb_id(self, h, line_number=0):
        """ sets new family husb_id """
        self.husb_id = h
        self._husb_id_line = line_number

    def set_husb_name(self, h, line_number=0):
        """ sets new family husb_name """
        self.husb_name = h
        self._husb_name = line_number

    def set_wife_id(self, w, line_number=0):
        """ sets new family wife_id """
        self.wife_id = w
        self._wife_id_line = line_number

    def set_wife_name(self, w, line_number=0):
        """ sets new family wife_name """
        self.wife_name = w
        self._wife_name_life = line_number

    def set_children(self, c, line_number=0):
        """ adds child to family's children """
        if isinstance(self.children, set):
            self.children = self.children | {c}
            self._children_lines = self._children_lines | {line_number}
        else:
            self.children = {c} if (c and c != 'NA') else 'NA'
            self._children_lines = {line_number}

def main():
    """ for running GED reader. """

    # this will analyze all files in the input_files directory
    for folder in [x for x in os.listdir(os.path.join(os.getcwd(), 'test_directory')) if os.path.isdir(os.path.join(os.getcwd(), 'test_directory', x))]:
        for file in [f for f in os.listdir(os.path.join(os.getcwd(), 'test_directory', folder)) if f.endswith('.ged')]:
            try:
                print(f'Creating GED_Repo for data in {file}')
                g = GED_Repo(os.path.join(os.getcwd(), 'test_directory', folder, file))
                g.print_individuals()
                g.print_families()
            except ValueError as v:
                print(v)
            except FileNotFoundError as f:
                print(f)

if __name__ == '__main__':
    main()