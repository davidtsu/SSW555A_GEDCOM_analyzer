"""
ssw555a_ged.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
file reader for GEDCOM files
"""
import os, math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable
from datetime import date

class GED_Repo:
    """ stores data from a GEDCOM file """
    def __init__(self, in_folder):
        """ constructor for GED_Repo, creates list of individuals and families """
        self.individuals = dict()
        self.families = dict()

        try:
            # read all files from folder, saves to individuals and families dictionaries
            for in_file in in_folder:
                if in_file.endswith('.ged'):
                    # read data
                    print(f'Reading GED data from {in_file}')
                    self.read_ged(in_file)

                    # finish calculating data
                    self.set_data()

                else:
                    print('Bad input file.')

        except FileNotFoundError as f:
            raise f
        except ValueError as v:
            raise v

    def set_data(self):
        ''' all user stories related to CHANGING data should probably go here '''
        self.set_ages()
        self.US23_unique_name_and_birthdate() # this must be done for EVERY GEDCOM file
    
    def check_data(self):
        ''' all user stories related to CHECKING data should probably go here '''
        self.user_story_01()    # US01
        self.user_story_2()     # US02 and US10
        self.user_story_3()     # US03
        self.user_story_4()     # US04
        self.user_story_5()     # US05
        self.user_story_6()     # US06
        self.user_story_07()    # US07
        self.check_bday()       # US08 and US09
        self.user_story_15()    # US15
        self.user_story_21()    # US21
        self.user_story_17()    # US17
        self.user_story_18()    # US18

    def print_data(self):
        ''' all user stories related to PRINTING data should go here '''
        self.US29_list_deceased()
        self.user_story_35()
        self.user_story_36()
        self.US38_upcoming_birthdays()
        self.US39_upcoming_anniversaries()

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
                        (level, tag, arg) = self.line_to_tuple(line, sep, line_number)

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
                                        (level, tag, arg) = self.line_to_tuple(line, sep, line_number)
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            ind.set_birthday(d, line_number)
                                            ind.set_alive(True, line_number)
                                    elif tag == 'DEAT':
                                        # must read & parse next line for DOD
                                        line = next(fp_in)
                                        line_number = line_number + 1
                                        (level, tag, arg) = self.line_to_tuple(line, sep, line_number)
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            ind.set_alive(False, line_number)
                                            ind.set_death(d, line_number)
                                    elif tag == 'DATE':
                                        print(f'Unmatched DATE tag of {tag}. GEDCOM line: {line_number}')
                                    else: # Not sure what to do with TRLR, since it just marks EOF.
                                        break #print(f'Reached end of {ip}')

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
                                        (level, tag, arg) = self.line_to_tuple(line, sep, line_number)
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            fam.set_married(d, line_number)
                                    elif tag == 'DIV':
                                        line = next(fp_in)
                                        line_number = line_number + 1
                                        (level, tag, arg) = self.line_to_tuple(line, sep, line_number)
                                        if tag != 'DATE':
                                            raise ValueError(f'Bad value, {tag} is not DATE tag. GEDCOM line: {line_number}')
                                        else:
                                            d = self.strip_date(arg, line_number)
                                            fam.set_divorced(d, line_number)
                                    elif tag == 'DATE':
                                        print(f'Unmatched DATE tag of {tag}. GEDCOM line: {line_number}')
                                    else: # Not sure what to do with TRLR, since it just marks EOF.
                                        break #print(f'Reached end of {ip}')

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
            print(v)
        except FileNotFoundError:
            raise FileNotFoundError(f'Cannot open file. Please check {ip} exists and try again. GEDCOM line: {line_number}')
    
    def line_to_tuple(self, line, sep, line_number):
        """ reads line, returns values in input """
        s = line.strip().split(sep, 2)
        if len(s) < 2:
            raise ValueError(f'Line {line_number} has too few values.')
        return tuple((s[i] if i < len(s) else "" for i in range(3)))

    def add_individual(self, i):
        """ must pass in individual 
        US22: checks if the individual ids are unique
        """
        if i.iid in self.individuals.keys():
            print(f'US22 - {i.iid} id has a duplicate in line number {i._iid_line}')
        self.individuals[i.iid] = i
        return Individual()

    def add_family(self, f):
        """ must pass in family 
        US22: checks if the family ids are unique
        """
        if f.fid in self.families.keys():
            print(f'US22 - {f.fid} id has a duplicate in line number {f._fid_line}')
        self.families[f.fid] = f
        return Family()

    def user_story_01(self):
        """"check if Dates (birth, marriage, divorce, death) should not be after the current date"""
        td=datetime.today()
        for person in self.individuals.values():
            pb=person.birthday
            pd=person.death
            if pb !="NA" and pb>td:
                print(f'US01 - {person.name} birthday after today on line {person._birthday_line}')
            if pd !="NA" and pd>td:
                print(f'US01 - {person.name} death after today on line {person._death_line}')
        for family in self.families.values():
            fm=family.married 
            fd=family.divorced
            if fm !="NA" and fm>td:
                print(f'US01 - {self.individuals[family.wife_id].name} marriage after today on line {family._married_line}')
            if fd !="NA" and fd>td:
                 print(f'US01 - {self.individuals[family.husb_id].name} divorce after today on line {family._divorced_line}')

    def user_story_2(self):
        """
        US02: checks if a person's birthday occurs before their marriage
        US10: checks if person was at least 14 by their marriage date
        """
        for family in self.families.values():
            if family.married != 'NA':
                if family.wife_id != 'NA':
                    if self.individuals[family.wife_id].birthday != 'NA':
                        if self.individuals[family.wife_id].birthday > family.married:
                            print(
                                f'US02 - {self.individuals[family.wife_id].name} birthday after marriage date on line {self.individuals[family.wife_id]._birthday_line}')
                        elif self.individuals[family.wife_id].birthday + relativedelta(years=14) > family.married:
                            print(
                                f'US10 - {self.individuals[family.wife_id].name} was less than 14 years old at time of marriage on line {self.individuals[family.wife_id]._birthday_line}')

                if family.husb_id != 'NA':
                    if self.individuals[family.husb_id].birthday != 'NA':
                        if self.individuals[family.husb_id].birthday > family.married:
                            print(
                                f'US02 - {self.individuals[family.husb_id].name} birthday after marriage date on line {self.individuals[family.husb_id]._birthday_line}')
                        elif self.individuals[family.wife_id].birthday + relativedelta(years=14) > family.married:
                            print(
                                f'US10 - {self.individuals[family.husb_id].name} was less than 14 years old at time of marriage on line {self.individuals[family.husb_id]._birthday_line}')
      
    def user_story_3(self):
        """ checks if a person's birthday occurs before their death day """
        for person in self.individuals.values():
            if person.birthday != 'NA' and person.death != 'NA':
                if person.birthday > person.death:
                    print(f'US03 - {person.name} birthday after death date on line {person._birthday_line}')

    def user_story_4(self):
        """ Marriage should occur before divorce of spouses, and divorce can only occur after marriage """
        for family in self.families.values():
            if family.married != 'NA':
                if family.wife_id != 'NA' and family.husb_id != 'NA' and family.divorced != 'NA':
                    if family.divorced < family.married:
                        print(
                            f'US04 - {self.individuals[family.wife_id].name} and {self.individuals[family.husb_id].name} married after divorce on line {family._married_line}')

    def user_story_5(self):
        """ checks that marriage should occur before death of either spouse """
        for family in self.families.values():
            if family.married != 'NA':
                if family.wife_id != 'NA':
                    if self.individuals[family.wife_id].death != 'NA':
                        if self.individuals[family.wife_id].death < family.married:
                            print(
                                f'US05 - {self.individuals[family.wife_id].name} married after individual death date on line {family._married_line}')

                if family.husb_id != 'NA':
                    if self.individuals[family.husb_id].death != 'NA':
                        if self.individuals[family.husb_id].death < family.married:
                            print(
                                f'US05 - {self.individuals[family.husb_id].name} married after individual death date on line {family._married_line}')

    def user_story_6(self):
        """ checks that divorce can only occur before death of both spouses """
        for family in self.families.values():
            if family.divorced != 'NA':
                if family.wife_id != 'NA':
                    if self.individuals[family.wife_id].death != 'NA':
                        if self.individuals[family.wife_id].death < family.divorced:
                                print(f'US06 - {self.individuals[family.wife_id].name} divorce after individual death date on line {family._divorced_line}')

                if family.husb_id != 'NA':
                    if self.individuals[family.husb_id].death != 'NA':
                        if self.individuals[family.husb_id].death < family.divorced:
                                print(f'US06 - {self.individuals[family.husb_id].name} divorce after individual death date on line {family._divorced_line}')

    def user_story_07(self):
        """ checks that age of individuals is <150 """
        for ind in self.individuals.values():
            if ind.age >= 150:
                print(f'US07 - {ind.name} is age {ind.age}, which is over 150 years old, on line {ind._age_line}')

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
                        print(f'US08 - {self.individuals[child].name} birthday before marriage on line {self.individuals[child]._birthday_line}')
                    # if child is born more than 9 months after divorce
                    if div != 'NA' and bday > div + relativedelta(months=9):
                        print(f'US08 - {self.individuals[child].name} birthday before marriage on line {self.individuals[child]._birthday_line}')

                    if fam.husb_id and fam.wife_id:
                        dad = self.individuals[fam.husb_id]
                        mom = self.individuals[fam.wife_id]
                        # if child is born any time after mother dies
                        if not mom.alive and mom.death < bday:
                            print(f'US09 - {self.individuals[child].name} birthday after mom death date on line {self.individuals[child]._birthday_line}')
                        # if child dies later than nine months after father dies
                        if not dad.alive and dad.death + relativedelta(months=9) < bday:
                            print(f'US09 - {self.individuals[child].name} birthday after dads death date on line {self.individuals[child]._birthday_line}')
                    #else:
                    #    print(f'{self.individuals[child].name} does not have both a mother and a father, on line {self.individuals[child]._birthday_line}')

    def user_story_15(self):
        for family in self.families.values():
                if len(family.children) >= 15:
                    print(f"US15 - {self.individuals[family.wife_id].name} and {self.individuals[family.husb_id].name} Family has {len(family.children)} children on line {self.individuals[sorted(family.children)[14]]._birthday_line}")
    
    def user_story_21(self):   
        """US21: checks the correct gender of husband and wife"""   
        for family in self.families.values():    
            if family.married != 'NA':
                if family.husb_id != 'NA':
                    if self.individuals[family.husb_id].gender != 'NA':
                        if self.individuals[family.husb_id].gender != 'M':
                            print(
                            f'US21 - {self.individuals[family.husb_id].name} gender is supposed to be male but is not on line {self.individuals[family.husb_id]._gender_line}')

                if family.wife_id != 'NA':
                    if self.individuals[family.wife_id].gender != 'NA':
                        if self.individuals[family.wife_id].gender != 'F': 
                            print(
                                f'US21 - {self.individuals[family.wife_id].name} gender is supposed to be female but is not on line {self.individuals[family.husb_id]._gender_line}')
    
    def US23_unique_name_and_birthdate(self):
        """ US23: Unique name and birth date
        No more than one individual with the same name and birth date should appear in a GEDCOM file
        Throws an error if there are two people with the same name and birthdate """

        print("US23: Unique Name and Birthdate")
        unique = True
        unique_list = list() # list structure - [ (person, birthday), line, (person, birthday), line ]

        for person in self.individuals.values():
            name = person.name
            bday = person.birthday.strftime("%m/%d/%Y")
            line = person._name_line
            p = (name, bday)
            if p in unique_list:
                duplicate_index = unique_list.index(p)
                duplicate_line = unique_list[duplicate_index + 1]
                print(f"US23: Two people with the same name and birthdate: {p} on GEDCOM line: {duplicate_line} and {p} on GEDCOM line {line}.")
                unique = False
            else:
                unique_list.append(p)
                unique_list.append(line)
        if unique == True:
            print("US23: All individuals have unique names and birthdates.")

    def US29_list_deceased(self):
        """ US29: List deceased
        List all deceased individuals in a GEDCOM file """
        deceased = list()
        for person in self.individuals.values():
            if person.alive == False:
                deceased.append(person.name)

    def US29_print_deceased(self, deceased):
        """ US29: List deceased
        Prints a list of deceased individuals to the user. """
        print("US29: List deceased")
        if len(deceased) == 0:
            print("No deceased.")
            return("No deceased.")
        else:
            print(deceased)
            return deceased
    
    def user_story_35(self):
        ''' US35 - prints list of individuals born in the last 30 days '''
        td=datetime.today()
        for individual in self.individuals.values():
            if (individual.birthday + relativedelta(days=30) ) > td:
               print(f'US35 - {individual.name} were born in the last 30 days on line {individual._name_line}') 

    def user_story_36(self):
        ''' US36 - prints list of individuals who died in the last 30 days '''
        td=datetime.today()
        for individual in self.individuals.values():
            if individual.death != 'NA':
                if (individual.death + relativedelta(days=30) ) > td:
                    print(f'US36 - {individual.name} were died in the last 30 days on line {individual._name_line}')
    
    def US38_upcoming_birthdays(self):
        """ US38: List upcoming birthdays
        List all living people in a GEDCOM file whose birthdays occur in the next 30 days """
        today = datetime.now() # current date and time
        thirty_days = today + relativedelta(days=30) # thirty days from today

        upcoming_bdays = list()
        for person in self.individuals.values():
            if person.death == "NA" or person.death == "NA":
                bday = person.birthday
                bday_curr_year = bday.replace(year=today.year)

                if today < bday_curr_year and bday_curr_year < thirty_days:
                    upcoming_bdays.append((person.name, bday.strftime("%m/%d/%Y")))
        
        self.US38_print_upcoming_birthdays(upcoming_bdays)
    
    def US38_print_upcoming_birthdays(self, upcoming_bdays):
        """ US38: List upcoming birthdays 
        Prints upcoming birthdays to the user """

        print("US38: List Upcoming Birthdays")

        if len(upcoming_bdays) == 0:
            print("No upcoming birthdays.")
            return ("No upcoming birthdays.")
        else:
            print(upcoming_bdays)
            return(upcoming_bdays)

    def US39_upcoming_anniversaries(self):
        """  US39: List upcoming anniversaries
        List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days """
        today = datetime.now() # current date and time
        thirty_days = today + relativedelta(days=30) # thirty days from today

        upcoming_anniversaries = list()

        for family in self.families.values():
            vals = family.get_values()
            married = vals[1]
            
            if married != "NA" and married != "" and vals[6] != "NA" and vals[6] != "":
                married = datetime.strptime(married, "%Y-%m-%d")
                married_curr_year = married.replace(year=today.year)
            
                if today < married_curr_year and married_curr_year < thirty_days:
                    upcoming_anniversaries.append((married.strftime("%m/%d/%Y"), "Husband: " + vals[4], "Wife: " + vals[6]))

        self.US39_print_upcoming_anniversaries(upcoming_anniversaries)
    
    def US39_print_upcoming_anniversaries(self, upcoming_anniversaries):
        """ US39: List upcoming anniversaries
        Prints upcoming anniversaries to the user """

        print("US39: List Upcoming Anniversaries") 

        if len(upcoming_anniversaries) == 0:
            print("No upcoming anniversaries.")
            return("No upcoming anniversaries.")
        else:
            print(upcoming_anniversaries)
            return(upcoming_anniversaries)

    # def user_story_17(self):
    #     """ Parents should not marry any of their children """
    #     for family in self.families.values():
    #         if family.married != 'NA' and family.wife_id != 'NA' and family.husb_id != 'NA' and family.children != 'NA':
    #             if len(family.children) > 0:
    #                 if self.individuals[family.husb_id] == self.individuals[family.husb_id] and self.individuals[family.children] == self.individuals[family.wife_id]:
    #                     print(f"US17 - {self.individuals[family.children].name} and {self.individuals[family.husb_id].name} are married on line {family._married_line}")
    #                 if self.individuals[family.wife_id] == self.individuals[family.wife_id] and self.individuals[family.children] == self.individuals[family.husb_id]:
    #                     print(f"US17 - {self.individuals[family.children].name} and {self.individuals[family.wife_id].name} are married on line {family._married_line}")
    
    def user_story_18(self):
        """ Siblings should not marry one another """
        for family in self.families.values():
            if family.husb_id != 'NA':
                if len(family.husb_id.children) > 0:
                    for child in family.husb_id.children:
                        c = self.individuals(family.children)
                        c.father = family.husb_id
            if family.wife_id != 'NA':
                if len(family.wife_id.children) > 0:
                    for child in family.wife_id.children:
                        c = self.individuals(family.children)
                        c.mother = family.wife_id
        for family in self.families.values():
            if family.husb_id != 'NA' and family.wife_id != 'NA':
                if family.husb_id.mother == family.wife_id.mother or family.husb_id.father == family.wife_id.father:
                    print(f"US18 - {self.individuals[family.husb_id].name} and {self.individuals[family.wife_id].name} are married on line {family._married_line}")
            
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
            raise ValueError(f"US42 - Illegitimate date of {arg}. GEDCOM line: {line_number}")
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
    def __init__(self, iid = '', name = '', gender = '', birthday = '', age = 0, alive = True, death = 'NA', child = 'NA', spouse = 'NA', married = 'NA', divorced = 'NA', mother = '', father = ''):
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

        self.married = married      # datetime object
        self._married_line = 0

        self.divorced = divorced    # datetime object
        self._divorced_line = 0

        self.mother = ""

        self.father = ""

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
                print(f'{self.name} is either marked alive but has death or marked dead but has no death date. GEDCOM line: {line_number}')
            else:
                bd = self.birthday
                dd = self.death
                self.age = math.floor((dd - bd).days / 365.2425)

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

    def add_mother(self, person):
        iid.mother = person.mother
    
    def add_father(self, person):
        iid.father = person.father


class Family:
    """ stores info for a family """
    def __init__(self, fid = '', married = 'NA', divorced = 'NA', husb_id = '', husb_name = '',fam_id = '', wife_id = '', wife_name = '', children = 'NA', death = 'NA'):
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

        self.fam_id = fam_id            # string
        self._fam_id_line = 0

        self.wife_id = wife_id          # string
        self._wife_id_line = 0

        self.wife_name = wife_name      # string
        self._wife_name_line = 0

        self.children = children        # set
        self._children_lines = set()

        self.death = death  # datetime object
        self._death_line = 0

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

    def set_death(self, d, line_number=0):
        """ sets new family divorce date """
        self.death = d if d else 'NA'
        self._death_line = line_number

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
        try:
            print(f'Creating GED_Repo for files in {folder}')
            g = GED_Repo([os.path.join(os.getcwd(), 'test_directory', folder, f) for f in os.listdir(os.path.join(os.getcwd(), 'test_directory', folder)) if f.endswith('.ged')])
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
