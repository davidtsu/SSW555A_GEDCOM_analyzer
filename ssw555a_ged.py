"""
ssw555a_ged.py
@Author: David Tsu, Ejona Kocibelli, Akshay Lavhagale, Zephyr Zambrano, Xiaojun Zhu
file reader for GEDCOM files
"""
import os, math, itertools, operator
from datetime import datetime
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable
from datetime import date
from collections import Counter

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
                    # print(f'Reading GED data from {in_file}')
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
        self.user_story_11()    # US11
        self.user_story_12()    # US12
        self.user_story_13()    # US13
        self.user_story_15()    # US15
        self.US16_male_last_names() # US16
        self.user_story_17()    # US17
        self.user_story_18()    # US18
        self.user_story_19()    # US19 
        self.user_story_20()    # US20
        self.user_story_21()    # US21
        self.user_story_24()    # US24
        self.US25_unique_first_names_in_families()  # US25

    def print_data(self):
        ''' all user stories related to PRINTING data should go here '''
        self.US28_Siblings_by_age()
        self.US29_list_deceased()
        self.US30_living_married()
        self.US31_living_single()
        self.US34_Twice_age_diff()
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

    def user_story_13(self):
        """ checks if siblings are born with enough separation (outside of 8mo or within 2days of each other) """
        for family in self.families.values():
            if family.children != 'NA':
                bday_dict = dict() # { iid1: bday1, iid2: bday1, iid3: bday2 }
                for child in family.children:
                    bday_dict[child] = self.individuals[child].birthday
                for i1, i2 in itertools.combinations(bday_dict, 2):
                    older = bday_dict[i1] if bday_dict[i1] < bday_dict[i2] else bday_dict[i2]
                    younger = bday_dict[i1] if bday_dict[i1] >= bday_dict[i2] else bday_dict[i2]
                    if older + relativedelta(days=1) < younger and younger < older + relativedelta(months=8):
                        print(f'US13 - {min(self.individuals[i1].name, self.individuals[i2].name)} and {max(self.individuals[i1].name, self.individuals[i2].name)} have birthdays that are too close together on lines {min(self.individuals[i1]._birthday_line, self.individuals[i2]._birthday_line)} and {max(self.individuals[i1]._birthday_line, self.individuals[i2]._birthday_line)}')

    def user_story_11(self):
        """US11: checks if there is bigamy happening in a family in where husband/wife is married twice in the same time."""
        processed = set()
        for fam in self.families.values():
            for fam2 in self.families.values():
                ids = tuple(sorted([fam.fid, fam2.fid]))
                if fam.fid != fam2.fid and ids not in processed:
                    processed.add(ids)
                    if fam.husb_id == fam2.husb_id:
                        if fam.divorced == 'NA' and fam2.divorced == 'NA' \
                        or fam.married < fam2.married < fam.divorced:
                            try:
                                print(
                                    f'US11 - {self.individuals[fam.husb_id].name} married twice on the same time on line {self.families[fam.fid]._married_line}')
                            except KeyError:
                                print(f'US11 - Husband or Wife is married twice at the same time.')
                    if fam.wife_id == fam2.wife_id:
                        if fam.divorced == 'NA' and fam2.divorced == 'NA' \
                        or fam.married < fam2.married < fam.divorced:
                            try:
                                print(
                                        f'US11 - {self.individuals[fam.wife_id].name} married twice on the same time on line {self.families[fam.fid]._married_line}')
                            except KeyError:
                                print(f'US11 - Husband or Wife is married twice at the same time.')

    def user_story_12(self):   
        """US12: checks if there is big gap age difference between father and child (>80) and mother and child (>60)"""
        for fam in self.families.values():
            if fam.children != 'NA':
                for child in fam.children:
                    if fam.husb_id and fam.wife_id:
                        if self.individuals[fam.husb_id].birthday != 'NA' and self.individuals[fam.wife_id].birthday != 'NA':
                            if self.individuals[fam.husb_id].age - self.individuals[child].age > 80:
                                print(
                                    f"US12 - {self.individuals[fam.husb_id].name} is 80 years older than his child on line {self.individuals[fam.husb_id]._birthday_line}")
                            if self.individuals[fam.wife_id].age - self.individuals[child].age > 60:
                                print(
                                    f'US12 - {self.individuals[fam.wife_id].name} is 60 years older than his child on line {self.individuals[fam.wife_id]._birthday_line}')
       
    def user_story_15(self):
        for family in self.families.values():
            if len(family.children) >= 15:
                print(f"US15 - {self.individuals[family.wife_id].name} and {self.individuals[family.husb_id].name} Family has {len(family.children)} children on line {self.individuals[sorted(family.children)[14]]._birthday_line}")
    
    def US16_male_last_names(self):
        """ US16: Male last names
        All male members of a family should have the same last name """

        for family in self.families.values():
            husband = family.husb_name
            x = husband.find("/")
            lastname = husband[x + 1:len(husband) - 1]
            children = family.children
            if "NA" in children: # no children
                pass
            else: # family has children
                for child in children:
                    for person in self.individuals.values():
                        if person.iid == child:
                            if person.gender == "M":
                                y = person.name.find("/")
                                child_lastname = person.name[y + 1:len(person.name) - 1]
                                if child_lastname != lastname:
                                    print(f"US16: Male child: {person.name} with ID: {person.iid} on GEDCOM line: {person._name_line} has a differet last name than the family last name: {lastname}.")
                        break

    def user_story_17(self):
        """ Parents should not marry any of their children """
        for f1 in self.families.values():
            for f2 in self.families.values():
                if f1.fid != f2.fid:
                    if f1.husb_id == f2.husb_id and f2.wife_id in f1.children:
                        try:
                            print(f"US17 - {self.individuals[f2.wife_id].name} and {self.individuals[f1.husb_id].name} are married on line {f1._married_line}")
                        except KeyError:
                            print(f"US17 - Parents are married to their children")
                    if f1.wife_id == f2.wife_id and f2.husb_id in f1.children:
                        print(f"US17 - {self.individuals[f2.husb_id].name} and {self.individuals[f1.wife_id].name} are married on line {f1._married_line}")

    def user_story_18(self):
        """ Siblings should not marry each other """
        for f1 in self.families.values():
            for f2 in self.families.values():
                if f2.husb_id in f1.children and f2.wife_id in f1.children:
                    try:
                        print(f"US18 - {self.individuals[f2.husb_id].name} and {self.individuals[f2.wife_id].name} are siblings and are married on line {f2._married_line}")
                    except KeyError:
                        print(f'US18 - Siblings married each other.')

    def siblings(self):
        sibs = list()
        for fam in self.families.values():
            sibs.append(fam.children)
        return sibs

    def parents(self, id):
        parents = []
        for fam in self.families.values():
            hub = fam.husb_id
            wif = fam.wife_id
            for child in fam.children:
                if (child == id):
                    parents = [hub, wif]
        return parents

    def user_story_19(self):
        """ first cousins should not get married """
        sibs = self.siblings()
        for fam in self.families.values():
            hub = fam.husb_id
            wif = fam.wife_id
            hub_parents = self.parents(hub)
            wif_parents = self.parents(wif)
            if len(hub_parents) > 0 and len(wif_parents) > 0:
                for kids in sibs:
                    if ((hub_parents[0] in kids and hub_parents[0] != wif_parents[0]) or (
                            hub_parents[1] in kids and hub_parents[1] != wif_parents[1])):
                        if wif_parents[0] in kids or wif_parents[1] in kids:
                            print(f"US19 - Family {fam.fid} is where first cousins are married")
    
    def user_story_20(self):
        """ people should not marry their aunt or uncle """
        sibs = self.siblings()
        dict = {}
        for fam in self.families.values():
            husband = fam.husb_id
            wife = fam.wife_id
            aunts_and_uncles = []
            for a in sibs:
                if (husband in a or wife in a):
                    aunts_and_uncles += a
            if husband in aunts_and_uncles:
                aunts_and_uncles.remove(husband)
            if (wife in aunts_and_uncles):
                aunts_and_uncles.remove(wife)
            if (len(aunts_and_uncles) > 0):
                for child in fam.children:
                    dict[child] = aunts_and_uncles
        for fam1 in self.families.values():
            hub = fam1.husb_id
            wif = fam1.wife_id
            if (hub in dict):
                lst = dict[hub]
                if (wif in lst):
                    print(f"US20 - Family {fam1.fid} has someone married to their aunt")
            if (wif in dict):
                lst = dict[wif]
                if (hub in lst):
                    print(f"US20 - Family {fam1.fid} has someone married to their uncle")

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
        Prints if there are two people with the same name and birthdate """
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
            else:
                unique_list.append(p)
                unique_list.append(line)

    def user_story_24(self):
        ''' check that each family has a unique combination of husband name, wife name, and marriage date '''
        existing_families = set()
        for family in self.families.values():
            if family.married and family.husb_name != '' and family.wife_name != '':
                if (family.married, family.husb_name, family.wife_name) in existing_families:
                    print(f'US24: {family.fid} family data appears at least twice with same spouses by name and the same marriage date on line {family._married_line}')
                else:
                    existing_families.add((family.married, family.husb_name, family.wife_name))
    
    def US25_unique_first_names_in_families(self):
        """ US25: Unique first names in families
        No more than one child with the same name and birth date should appear in a family """

        for family in self.families.values():
            husband_fullname = family.husb_name
            wife_fullname = family.wife_name

            x = husband_fullname.find("/")
            y = wife_fullname.find("/")

            husband = husband_fullname[0:x - 1]
            wife = wife_fullname[0:y - 1]

            firstnames = list()
            firstnames.append(husband)
            firstnames.append(wife)

            if husband == wife:
                h_line = 0
                w_line = 0
                for person in self.individuals.values():
                    if person.iid == family.husb_id:
                        h_line = person._name_line
                    if person.iid == family.wife_id:
                        w_line = person._name_line
                print(f"US25: Husband: {husband_fullname} on GEDCOM line: {h_line} and wife: {wife_fullname} on GEDCOM line {w_line} have the same first name.")
            else:
                children = family.children
                if "NA" in children: # no children
                    pass
                else: # family has children
                    for child in children:
                        for person in self.individuals.values():
                            if person.iid == child:
                                child_fullname = person.name
                                z = child_fullname.find("/")
                                child = person.name[0:z - 1]\

                                if child in firstnames:
                                    print(f"US25: Child: {person.name} on GEDCOM line: {person._name_line} has the same first name as another family member.")
                            break

    def US28_Siblings_by_age(self):
        """  US28: List siblings by age
        List siblings in families by decreasing age, i.e. oldest siblings first"""
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Silibings in family(sort)']

        for i in self.families.values():
            if i.children !="NA":
                siblings={}#{child_name_1:(age1,birthday1),child_name_2:(age2,birthday2)}
                for child_id in itertools.chain(i.children):
                    child_name=self.individuals[child_id].name
                    siblings[child_name] = (self.individuals[child_id].age,self.individuals[child_id].birthday)
                siblings_sort = {k:datetime.strftime(v[1], "%d %b %Y") for (k,v) in sorted(siblings.items(),key=lambda item:item[1][1],reverse=False)}
                pt.add_row([i.fid, siblings_sort])
    
        print("US28: List all siblings by age,i.e. oldest siblings first")
        if len(pt._rows) == 0:
            print('Family in ged.file doesn\'t have children yet.')
            return 'Family in ged.file doesn\'t have children yet.'
        else:
            pt.sortby = 'Family ID'
            print(pt)
            return pt

    def US29_list_deceased(self):
        """ US29: List deceased
        List all deceased individuals in a GEDCOM file """
        pt = PrettyTable()
        pt.field_names = ['Deceased Individual ID', 'Deceased Individual Name']
        for person in self.individuals.values():
            if person.alive == False:
                pt.add_row([person.iid, person.name])
        print("US29: List deceased") 
        if len(pt._rows) == 0:
            print('No deceased individuals.')
            return 'No deceased individuals.'
        else:
            pt.sortby = 'Deceased Individual ID'
            print(pt)
            return pt
    
    def US30_living_married(self):
        """  US30: List living married
        List all living married people in a GEDCOM file """
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Living Husband Name', ' Living Wife Name']
        for i in self.families.values():
            if i.married != 'NA' and i.divorced == 'NA' and i.wife_id != "NA" and i.wife_id != '' and i.husb_id != "NA" and i.husb_id != '':
               if self.individuals[i.wife_id].alive and self.individuals[i.husb_id].alive:
                    pt.add_row([i.fid, i.husb_name, i.wife_name])
        print("US30: List living married couples")
        if len(pt._rows) == 0:
            print('No living married couples.')
            return 'No living married couples.'
        else:
            pt.sortby = 'Family ID'
            print(pt)
            return pt

    def US31_living_single(self):
        """  US31: List living singles
        List all living people over 30 who have never been married in a GEDCOM file """
        pt = PrettyTable()
        pt.field_names = ['Unmarried Individual ID', 'Unmarried Individual Name']
        marriage_husb_ids = [ x.husb_id for x in self.families.values() ]
        marriage_wife_ids = [ x.wife_id for x in self.families.values() ]
        for i in self.individuals.values():
            if i.age >= 30 and not (i.iid in marriage_husb_ids or i.iid in marriage_wife_ids):
                pt.add_row([i.iid, i.name])
        print("US31: List all living people over 30 who have never been married")
        if len(pt._rows) == 0:
            print('No unmarried individuals over 30.')
            return 'No unmarried individuals over 30.'
        else:
            pt.sortby = 'Unmarried Individual ID'
            print(pt)
            return pt

    def US34_Twice_age_diff(self):
        """  US34: List large age differences
        List all couples who were married when the older spouse was more than twice as old as the younger spouse"""
        pt = PrettyTable()
        pt.field_names = ['Family ID', 'Twice age diff married spouse']

        for i in self.families.values():
            if i.married !="NA" and self.individuals[i.husb_id].birthday!="NA"\
                and self.individuals[i.wife_id].birthday!="NA":
                Hus_bd=self.individuals[i.husb_id].birthday
                Hus_marr_age=math.floor((i.married - Hus_bd).days / 365.2425) 
                Wf_bd=self.individuals[i.wife_id].birthday
                Wf_marr_age=math.floor((i.married -Wf_bd).days / 365.2425)
                if max(Hus_marr_age,Wf_marr_age)>min(Hus_marr_age,Wf_marr_age)*2\
                    and min(Hus_marr_age,Wf_marr_age)>0:
                    pt.add_row([i.fid,(i.husb_name,i.wife_name)])
    
        print("US34: List large age differences")
        if len(pt._rows) == 0:
            print('Couple in ged.file doesn\'t have 2 times age difference when married.')
            return 'Couple in ged.file doesn\'t have 2 times age difference when married.'
        else:
            pt.sortby = 'Family ID'
            print(pt)
            return pt

    def user_story_35(self):
        ''' US35 - prints list of individuals born in the last 30 days '''
        td=datetime.today()
        pt = PrettyTable()
        pt.field_names = ['Individual ID', 'Individual Name', 'Individual Birthday']
        for individual in self.individuals.values():
            if (individual.birthday + relativedelta(days=30) ) > td:
                pt.add_row([individual.iid, individual.name, individual.birthday.strftime("%m/%d/%Y")])
        if not len(pt._rows) == 0:
            print('US35: List individuals born in the last 30 days')
            print(pt)
            return pt 
        else:
            return(f'No individuals born in the last 30 days.') 

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
            if person.death == "" or person.death == "NA":
                bday = person.birthday
                bday_curr_year = bday.replace(year=today.year)

                if today < bday_curr_year and bday_curr_year < thirty_days:
                    upcoming_bdays.append([person.name, bday.strftime("%m/%d/%Y")])

        self.US38_print_upcoming_birthdays(upcoming_bdays)

    def US38_print_upcoming_birthdays(self, upcoming_bdays):
        """ US38: List upcoming birthdays
        Prints upcoming birthdays to the user """

        print("US38: List Upcoming Birthdays")
        pt = PrettyTable()
        pt.field_names = ["Name", "Birthday"]
        for i in upcoming_bdays:
            pt.add_row([i[0], i[1]])
        print(pt)
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
            husband_id = vals[3]
            wife_id = vals[5]
            dead = False

            for person in self.individuals.values(): # checks if one or both spouces are dead
                if person.iid == husband_id or person.iid == wife_id:
                    if person.alive == False:
                        dead = True

            if dead == False and married != "NA" and married != "":
                married = datetime.strptime(married, "%Y-%m-%d")
                married_curr_year = married.replace(year=today.year)

                if today < married_curr_year and married_curr_year < thirty_days:
                    upcoming_anniversaries.append([married.strftime("%m/%d/%Y"), vals[4], vals[6]])

        self.US39_print_upcoming_anniversaries(upcoming_anniversaries)

    def US39_print_upcoming_anniversaries(self, upcoming_anniversaries):
        """ US39: List upcoming anniversaries
        Prints upcoming anniversaries to the user """

        print("US39: List Upcoming Anniversaries")
        pt = PrettyTable()
        pt.field_names = ["Anniversary", "Husband", "Wife"]
        for i in upcoming_anniversaries:
            pt.add_row([i[0], i[1], i[2]])
        print(pt)
        return(upcoming_anniversaries)

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
    def __init__(self, iid = '', name = '', gender = '', birthday = '', age = 0, alive = True, death = 'NA', child = 'NA', spouse = 'NA', married = 'NA', divorced = 'NA'):
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
        self._child_lines = 0

        self.spouse = spouse        # set
        self._spouse_lines = set()

        self.married = married      # datetime object
        self._married_line = 0

        self.divorced = divorced    # datetime object
        self._divorced_line = 0

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
        self._children_lines = 0

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
