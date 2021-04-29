"""
Name: ABA.py
Date: 4/18/2021
Author: Quinn Bigane, Tom Padova, Bo Kulbacki
Description: This is a secure implementation of an Address Book database
"""

#بت
import datetime
import re
import os
from cryptography.fernet import Fernet


class Address_record:
    def __init__(self, recordID,
    SN='', GN='', PEM='', WEM='', PPH='', WPH='', SA='', CITY='', STP='', CTY='', PC=''):
        self.recordID = recordID
        self.SN = SN
        self.GN = GN
        self.PEM = PEM
        self.WEM = WEM
        self.PPH = PPH
        self.WPH = WPH
        self.SA = SA
        self.CITY = CITY
        self.STP = STP
        self.CTY = CTY
        self.PC = PC
        
class Address_Book:
    def __init__(self, login_state=0, current_user=None):
        try:
            login_info = open("logininfo.txt", "r")
            login_info.close()
        except OSError: #if file cannot be opened
            login_info = open("logininfo.txt", "wb")
            admin = self.encrypt_string("admin")
            login_info.write(admin)
            login_info.close()

        try:
            audit_log = open("audit_log.csv", "r")
            audit_log.close()
        except OSError: #if file cannot be opened
            audit_log = open("audit_log.csv", "wb")
            audit_log.close()
        #0 = not logged in
        #1 = logged in
        self.login_state = login_state
        self.current_user = current_user
        #Begin main loop
        self.driver()

    def driver(self):
        """
        Main looping module of the function, waits for user input
        """  
        #print this when the program first starts
        print("Address Book Application, version 1.0. Type “HLP” for a list of commands")

        #main loop waiting for user input
        while 1:
            #prompt user to enter a command
            command = input("ABA > ")
            #interpret user command
            self.command_line_interpreter(command)

    def command_line_interpreter(self, command):
        """
        Interprets user input and decides what to do based on that
        """
        #parse command entered on spaces
        self.tokens = None
        self.tokens = command.split(" ")

        #based on commanded entered, decide next step
        if self.tokens[0] == "HLP": #help
            self.display_help()
        elif self.tokens[0] == "LIN": #login
            self.login()
        elif self.tokens[0] == "LOU": #logout
            self.logout()
        elif self.tokens[0] == "CHP": #change password
            self.change_password()
        elif self.tokens[0] == "ADU": #add user
            self.add_user()
        elif self.tokens[0] == "DEU": #delete user
            self.delete_user()
        elif self.tokens[0] == "LSU": #list users
            self.list_users()
        elif self.tokens[0] == "DAL": #display audit log
            self.display_audit_log()
        elif self.tokens[0] == "ADR": #add record
            self.add_record()
        elif self.tokens[0] == "DER": #delete record
            self.delete_record()
        elif self.tokens[0] == "EDR": #edit record
            self.edit_record()
        elif self.tokens[0] == "GER": #get record
            self.get_record()
        elif self.tokens[0] == "IMD": #import database
            self.import_database()
        elif self.tokens[0] == "EXD": #export database
            self.export_database()
        elif self.tokens[0] == "EXT": #exit
            self.exit()
        else:
            print("Unrecognized command")

    def exit(self):
        """
        Exits ABA
        """
        exit()

    def login(self):
        """
        Verifies user login credentials based on a database of login info
        """
        #if there is currently an active login
        if self.login_state != 0:
            print("An account is currently active; logout before proceeding")
        #if the user entered no username or mulitple
        elif len(self.tokens) == 1 or len(self.tokens) > 2:
            print("Invalid Credentials")
        #check password
        else:
            login_info = open("logininfo.txt", "rb")
            #loop through all login data
            lines = login_info.readlines()
            for i in range(len(lines)):
                user_pass = lines[i].split(b",")
                user_pass[0] = self.decrypt_string(user_pass[0])
                #matching username found
                if user_pass[0].rstrip() == self.tokens[1]:
                    #no password associated with username
                    if len(user_pass) == 1:
                        #Request new password
                        new_password = input("This is the first time the account is being used. You must create a new password. Passwords may contain 1-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
                        #Request user to input password again
                        pw_confirmation = input("Reenter the same password: ")
                        #if the passwords do not match, return without adding password
                        if new_password != pw_confirmation:
                            print("Passwords do not match")
                            login_info.close()
                            self.add_to_audit_log("LF")
                            return
                        #maxsize of password => 24 characters, upercase or lowercase letters and numbers
                        #Check if password contains only uppercase, only lowercase, or only numbers
                        if not re.fullmatch(r"[A-Za-z0-9]{1,24}", new_password):
                            print("Password contains illegal characters")
                            login_info.close()
                            self.add_to_audit_log("LF")
                            return
                        #Check if the password is too basic or easy to guess
                        common_password_file = open("common_passwords.txt", "r")
                        common_passwords = common_password_file.readlines()
                        common_password_file.close()
                        if (len(new_password) < 8) or (new_password + '\n' in common_passwords) or (new_password == self.tokens[1]):
                            print("Password is too easy to guess")
                            login_info.close()
                            self.add_to_audit_log("LF")
                            return
                        #If the passwords do match, encrypt it and add it to the login info and login user
                        new_password = self.encrypt_string(new_password)
                        lines[i] = lines[i].rstrip() + b"," + new_password + b"\n"
                        login_info.close()
                        login_info = open("logininfo.txt", "wb")
                        login_info.writelines(lines)
                        login_info.close()
                        print("OK")
                        self.current_user = user_pass[0]
                        self.login_state = 1
                        self.add_to_audit_log("L1")
                        self.add_to_audit_log("LS")
                        return
                    #username has a password associated with it
                    else:
                        password_guess = input("Enter your password: ")
                        user_pass[1] = self.decrypt_string(user_pass[1])
                        if user_pass[1].rstrip() == password_guess: #correct password entered
                            #set current user variables
                            self.current_user = user_pass[0]
                            self.login_state = 1
                            print("OK")
                            login_info.close()
                            self.add_to_audit_log("LS")
                            return
                        else:
                            login_info.close()
                            print("Invalid credentials")
                            self.add_to_audit_log("LF")
                            return
            #username was not found in login info
            login_info.close()
            print("Invalid credentials")
            self.add_to_audit_log("LF")
        return

    def logout(self):
        """
        Logs out current user
        """
        #no active login session
        if self.login_state == 0:
            print("No active login session")

        #if there is an active login session
        else:
            self.login_state = 0
            self.add_to_audit_log("LO")
            self.current_user = None
            print("OK")
        return
    
    def change_password(self):
        """
        Logs out current user
        """
        if self.login_state == 0: #no active login session
            print("No active login session")
            self.add_to_audit_log("FPC") #if failed password change
        #User has entered command correctly
        else:
            #If the user eneterd no password or multiple
            if len(self.tokens) == 1 or len(self.tokens) > 2:
                print("Invalid Credentials")
                self.add_to_audit_log("FPC")
            #check password
            else:
                login_info = open("logininfo.txt", "rb")
                #loop through all login data
                lines = login_info.readlines()
                for i in range(len(lines)):
                        user_pass = lines[i].split(b",")
                        user_pass[0] = self.decrypt_string(user_pass[0])
                        #matching username found
                        if user_pass[0].rstrip() == self.current_user:
                            #if the given password matches the old password let user create new password
                            user_pass[1] = self.decrypt_string(user_pass[1])
                            if user_pass[1].rstrip() == self.tokens[1]:
                                #Request a new password
                                new_password = input("Create a new password. Passwords may contain up to 24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
                                #Request user to input password again
                                pw_confirmation = input("Reenter the same password: ")
                                #if the passwords do not match, return without adding password
                                if new_password != pw_confirmation:
                                    print("Passwords do not match")
                                    login_info.close()
                                    self.add_to_audit_log("FPC")
                                    return
                                #maxsize of password => 24 characters, upercase or lowercase letters and numbers
                                #Check if password contains only uppercase, only lowercase, or only numbers
                                if not re.fullmatch(r"([a-zA-Z0-9]){1,24}", new_password):
                                    print("Password contains illegal characters")
                                    login_info.close()
                                    self.add_to_audit_log("FPC")
                                    return
                                #Check if the password is too basic or easy to guess
                                common_password_file = open("common_passwords.txt", "r")
                                common_passwords = common_password_file.readlines()
                                common_password_file.close()
                                if (len(new_password) < 8) or (new_password + '\n' in common_passwords) or (new_password == self.current_user):
                                    print("Password is too easy to guess")
                                    login_info.close()
                                    self.add_to_audit_log("FPC")
                                    return

                                #If the passwords do match, add it to the login info
                                login_info.close()
                                new_password = self.encrypt_string(new_password)
                                user_pass[0] = self.encrypt_string(self.current_user)
                                lines[i] = user_pass[0] + b"," + new_password + b"\n"
                                login_info = open("logininfo.txt", "wb")
                                login_info.writelines(lines)
                                login_info.close()
                                print("OK")
                                self.login_state = 1
                                self.add_to_audit_log("SPC")
                                return
                            #if given password does not match old password, do not allow change password
                            else:
                                print("Invalid credentials")
                                login_info.close()
                                self.add_to_audit_log("FPC")
                                return
        return

    def list_users(self):
        """
        Display Users
        """
        #if there is currently an active login
        if self.login_state == 0:
            print("No active login session")
        #if the admin is not logged in
        elif self.current_user != "admin":
            print("Admin not active")
        #if the admin is logged in
        else:
            infile = open("logininfo.txt", "rb")
            lines = infile.readlines()
            for i in range(len(lines)):
                toks = lines[i].split(b",")
                toks[0] = self.decrypt_string(toks[0])
                print(toks[0].rstrip())
            infile.close()
            print("Ok")
        return

    def display_help(self):
        """
        Displays the help commands
        """
        if len(self.tokens) == 2:
            if self.tokens[1] == "HLP": #help
                print("HLP [<command name>]")
            elif self.tokens[1] == "LIN": #login
                print("LIN <userID>")
            elif self.tokens[1] == "LOU": #logout
                print("LOU")
            elif self.tokens[1] == "CHP": #change password
                print("CHP <old password>")
            elif self.tokens[1] == "ADU": #add user
                print("ADU <userID>")
            elif self.tokens[1] == "DEU": #delete user
                print("DEU <userID>")
            elif self.tokens[1] == "LSU": #list users
                print("LSU")
            elif self.tokens[1] == "DAL": #display audit log
                print("DAL [<userID>]")
            elif self.tokens[1] == "ADR": #add record
                print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
            elif self.tokens[1] == "DER": #delete record
                print("DER <recordID>")
            elif self.tokens[1] == "EDR": #edit record
                print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
            elif self.tokens[1] == "GER": #get record
                print("GER [<recordID>] [<fieldname> ...]")
            elif self.tokens[1] == "IMD": #import database
                print("IMD <Input_File>")
            elif self.tokens[1] == "EXD": #export database
                print("EXD <Output_file>")
            elif self.tokens[1] == "EXT": #exit
                print("EXT")
            else: #user entered an incorrect command
                print("LIN <userID>")
                print("LOU")
                print("CHP <old password>")
                print("ADU <userID>")
                print("DEU <userID>")
                print("LSU")
                print("DAL [<userID>]")
                print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
                print("DER <recordID>")
                print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
                print("GER [<recordID>] [<fieldname> ...]")
                print("IMD <Input_File>")
                print("EXD <Output_file>")
                print("HLP [<command name>]")
                print("EXT")
        else: #if user only entered HLP
            print("LIN <userID>")
            print("LOU")
            print("CHP <old password>")
            print("ADU <userID>")
            print("DEU <userID>")
            print("LSU")
            print("DAL [<userID>]")
            print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
            print("DER <recordID>")
            print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
            print("GER [<recordID>] [<fieldname> ...]")
            print("IMD <Input_File>")
            print("EXD <Output_file>")
            print("HLP [<command name>]")
            print("EXT")

        print("OK")
        return

    def import_database(self):
        """
        Imports a database
        """
        if self.login_state == 0: #no active login
            print("No active login session")
            return
        if self.current_user == "admin": #admin user currently logged in
            print("Admin not authorized")
            return
        if len(self.tokens) < 2: #no input file specified
            print("No Input_file specified")
            return
        try:
            infile = open(self.tokens[1], "r")
        except OSError: #if file cannot be opened
            print("Can’t open Input_file")
            return
        #check file format (Data fields may be no more than 64 printable ASCII characters in length)
        new_records = 0
        for line in infile:
            #Good record format: Bob;Smith;Robert;bobsmith@mail.edu;;8805551212;;;;;;;
            #recordID;SN;GN;PEM;WEM;PPH;WPH;SA;CITY;STP;CTY;PC
            tokens = line.split(";")
            if not(re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[0]) or re.fullmatch("",tokens[0])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[1]) or re.fullmatch("",tokens[1])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[2]) or re.fullmatch("",tokens[2])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[3]) or re.fullmatch("",tokens[3])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[4]) or re.fullmatch("",tokens[4])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[5]) or re.fullmatch("",tokens[5])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[6]) or re.fullmatch("",tokens[6])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[7]) or re.fullmatch("",tokens[7])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[8]) or re.fullmatch("",tokens[8])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[9]) or re.fullmatch("",tokens[9])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[10]) or re.fullmatch("",tokens[10])) or not(
            re.fullmatch(r"[\x00-\x7F]{1,64}",tokens[11]) or  re.fullmatch("",tokens[11])):
                print("Input_file invalid format")
                return

            if self.check_recordID(tokens[0]) == 1:
                print("Duplicate recordID")
                return
            new_records+=1

        #count the # of records in the user's database already and store in num_records_in_db
        #(maybe a self. variable?)
        num_records_in_db = self.count_records()
        if num_records_in_db + new_records > 256:
            print("Number of records exceeds maximum")
            return
        infile.close()
        infile = open(self.tokens[1], "r")
        #add each record to the user's database
        for line in infile:
            self.add_record_from_import(line.rstrip())

        infile.close()
        print("OK")
        return

    def count_records(self):
        """
        Returns the number of records stored in a user's database.
        """
        try:
            infile = open((self.current_user + ".txt"), "rb")

            num_records = 0
            for _ in infile:
                num_records += 1

            infile.close()
            return num_records
        except OSError: #if file cannot be opened
            return 0

    def check_recordID(self, recordID):
        """
        Checks a user's database for recordID and returns 0 if the recordID
        is not in the user’s database and 1 if it already exists
        """
        #loop through all lines of user text file and checks to see if recordID is
        # the same as any of the ones in the text file
        try:
            f = open((self.current_user + ".txt"), "rb")
            for line in f:
                tokens = line.split(b";")
                tokens[0] = self.decrypt_string(tokens[0])
                if recordID == tokens[0]:
                    f.close()
                    return 1
            return 0
        except OSError: #if file cannot be opened
            return 0

    def export_database(self):
        """
        Exports current user database
        """
        if self.login_state == 0: #no active login
            print("No active login session")
            return
        elif self.current_user == "admin": #admin user currently logged in
            print("Admin not authorized")
            return
        elif len(self.tokens) < 2: #no input file specified
            print("No Output_file specified")
            return
        try:
            outfile = open(self.tokens[1], "a")
        except OSError: #if file cannot be opened
            print("Can’t open Output_file")
            return
        infile = open((self.current_user + ".txt"), 'rb')
        try:
            for line in infile:
                tokens = line.split(b";")
                output_line = ""
                for tok in tokens:
                    output_line += self.decrypt_string(tok) + ";"
                outfile.write(output_line + "\n")
        except Exception: #error writing to file
            print("Error writing Output_file")
        outfile.close()
        print("OK")
        return

    def add_record(self):
        """
        Adds a new record for user
        """
        #if there is currently an active login
        if self.login_state == 0:
            print("No active login session")
            return
        #if current user is an admin
        if self.current_user == "admin":
            print("Admin not authorized")
            return
        #User did not enter a record ID
        if len(self.tokens) < 2:
            print("No recordID")
            return
        #User put field in record ID spot
        if "=" in self.tokens[1]:
            print("No recordID")
            return
        #check if recordID passed has correct format
        if not re.fullmatch(r"[\x00-\x7F]{1,64}", self.tokens[1]):
            print("Invalid recordID")
            return
        #if the record ID is not in the user database
        if self.check_recordID(self.tokens[1]) == 0:
            newRecord = Address_record(self.tokens[1])
            #clean the input commands
            self.tokens = " ".join(self.tokens[2:])
            self.tokens = re.split('" |\' ',self.tokens)
            self.tokens[-1] = self.tokens[-1][0:-1]
            for entry in self.tokens:#searches tokens 0 to end
                if(entry == ""):
                    continue
                command = entry[0:entry.index("=")] #the command which will be entered
                if (command == "SN"):
                    SN = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", SN) or re.fullmatch("", SN):
                        newRecord.SN = SN
                    else:
                        print("One or more invalid record data fields")
                        return
                elif(command == "GN"):
                    GN = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", GN) or re.fullmatch("", GN):
                        newRecord.GN = GN
                    else:
                        print("One or more invalid record data fields")
                        return
                elif(command =="PEM"):
                    PEM = entry[entry.index("=")+2:]
                    if (re.fullmatch(r"([\x00-\x7F]+@[\x00-\x7F]+\.[\x00-\x7F]+){1}", PEM) and len(PEM) < 65 ) or re.fullmatch("", PEM):
                        newRecord.PEM = PEM
                    else:
                        print("One or more invalid record data fields")
                        return
                elif (command =="WEM"):
                    WEM = entry[entry.index("=")+2:]
                    if (re.fullmatch(r"([\x00-\x7F]+@[\x00-\x7F]+\.[\x00-\x7F]+){1}", WEM) and len(PEM) < 65 ) or re.fullmatch("", WEM):
                        newRecord.WEM = WEM
                    else:
                        print("One or more invalid record data fields")
                        return
                elif(command=="PPH"):
                    PPH = entry[entry.index("=")+2:]
                    print(PPH)
                    if re.fullmatch(r"\d{1,10}", PPH) or re.fullmatch("", PPH):
                        newRecord.PPH = PPH
                        print("entered")
                    else:
                        print("One or more invalid record data fields")
                        return
                elif(command=="WPH"):
                    WPH = entry[entry.index("=")+2:]
                    if re.fullmatch(r"\d{1,10}", WPH) or re.fullmatch("", WPH):
                        newRecord.WPH = WPH
                elif (command=="SA"):
                    SA = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", SA) or re.fullmatch("", SA):
                        newRecord.SA = SA
                    else:
                        print("One or more invalid record data fields")
                        return
                elif (command=="CITY"):
                    CITY = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", CITY) or re.fullmatch("", CITY):
                        newRecord.CITY = CITY
                    else:
                        print("One or more invalid record data fields")
                        return
                elif (command=="STP"):
                    STP = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", STP) or re.fullmatch("", STP):
                        newRecord.STP = STP
                    else:
                        print("One or more invalid record data fields")
                        return
                elif (command =="CTY"):
                    CTY = entry[entry.index("=")+2:]
                    if re.fullmatch(r"[\x00-\x7F]{1,64}", CTY) or re.fullmatch("", CTY):
                        newRecord.CTY = CTY
                    else:
                        print("One or more invalid record data fields")
                        return
                elif (command =="PC"):
                    PC = entry[entry.index("=")+2:]
                    if re.fullmatch(r"\d{5}",PC) or re.fullmatch("", PC):
                        newRecord.PC = PC
                    else:
                        print("One or more invalid record data fields")
                        return
                else:
                    print("One or more invalid record data fields")
                    return
                #check if the user has exceeded the maximum number of records
                if (self.count_records() > 255):
                    print("Number of records exceeds maximum") 
                    return
                #newRecord is added to the user's personal database 
                f = open((self.current_user + ".txt"), "ab")#"a" for appending to textfile so not to erase data
                f.write(self.encrypt_string(newRecord.recordID)+b";"+
                self.encrypt_string(newRecord.SN)+b";"+
                self.encrypt_string(newRecord.GN)+b";"+
                self.encrypt_string(newRecord.PEM)+b";"+
                self.encrypt_string(newRecord.WEM)+b";"+
                self.encrypt_string(newRecord.PPH)+b";"+
                self.encrypt_string(newRecord.WPH)+b";"+
                self.encrypt_string(newRecord.SA)+b";"+
                self.encrypt_string(newRecord.CITY)+b";"+
                self.encrypt_string(newRecord.STP)+b";"+
                self.encrypt_string(newRecord.CTY)+b";"+
                self.encrypt_string(newRecord.PC)+
                b"\n")
                f.close()
                print("OK")
                return

        print("Duplicate recordID")
        return

    def add_record_from_import(self, string):
        """
        Adds a new record for user
        """       
        f = open((self.current_user + ".txt"), "ab")#"a" for appending to textfile so not to erase data   
        toks = string.split(';')   
        for i in range(len(toks)):
            toks[i] = self.encrypt_string(toks[i])
        f.write(toks[0]+b";"+
        toks[1]+b";"+
        toks[2]+b";"+
        toks[3]+b";"+
        toks[4]+b";"+
        toks[5]+b";"+
        toks[6]+b";"+
        toks[7]+b";"+
        toks[8]+b";"+
        toks[9]+b";"+
        toks[10]+b";"+
        toks[11]+b"\n")
        f.close()
    
    def delete_record(self):
        """
        Deletes a record from the database
        """ 
        #If no active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #If current user is admin
        elif self.current_user == "admin":
            print("Admin not authorized")
            return
        #if no record ID was given
        elif len(self.tokens) < 2:
            print("No recordID")
            return
        #check if recordID passed has correct format
        if not re.fullmatch(r"[\x00-\x7F]{1,64}", self.tokens[1]):
            print("Invalid recordID") 
            return
        #If the record ID does not exist
        elif (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return
        #If the record ID is found
        else:
            #delete it
            f = open((self.current_user + ".txt"), "rb")
            lines = f.readlines()
            for i in range(len(lines)):
                tokens = lines[i].split(b";")
                tokens[0] = self.decrypt_string(tokens[0])
                if (tokens[0] == self.tokens[1]):
                    lines[i] = b""
                    f.close()
                    outFile = open((self.current_user + ".txt"), "wb")
                    outFile.writelines(lines)
                    outFile.close()
            print("OK") 
            return   

    def edit_record(self):
        """
        Edits a record from the database
        """  
        #If no active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #If current user is admin
        elif self.current_user == "admin":
            print("Admin not authorized")
            return
        #User did not enter a record ID
        if len(self.tokens) < 2:
            print("No recordID")
            return
        #User put field in record ID spot
        if "=" in self.tokens[1]:
            print("No recordID")
            return
        #check if recordID passed has correct format
        if not re.fullmatch(r"[\x00-\x7F]{1,64}", self.tokens[1]):
            print("Invalid recordID") 
            return
        #If the record ID does not exist
        if (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return
        #If the record ID was found edit it
        f = open((self.current_user + ".txt"), "rb")
        #lines is arry of all lines in current_user.txt
        lines = f.readlines()
        #loops through all lines
        for i in range(len(lines)):
            tokens = lines[i].split(b";") 
            #if recordID from textfile is the same as the given recordID
            tokens[0] = self.decrypt_string(tokens[0])
            if (tokens[0] == self.tokens[1]):
                newRecord = Address_record(self.tokens[1])
                #clean the input commands
                # self.clean_inputs(self.tokens[2:])
                self.tokens = " ".join(self.tokens[2:])
                self.tokens = re.split('" |\' ',self.tokens)
                self.tokens[-1] = self.tokens[-1][0:-1]
                for entry in self.tokens:
                    if(entry == ""):
                        continue
                    command = entry[0:entry.index("=")] #the command which will be entered
                    if (command == "SN"):
                        SN = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", SN) or re.fullmatch("", SN):
                            newRecord.SN = SN
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif(command == "GN"):
                        GN = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", GN) or re.fullmatch("", GN):
                            newRecord.GN = GN
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif(command =="PEM"):
                        PEM = entry[entry.index("=")+2:]
                        if (re.fullmatch(r"([\x00-\x7F]+@[\x00-\x7F]+\.[\x00-\x7F]+){1}", PEM) and len(PEM) < 65 ) or re.fullmatch("", PEM):
                            newRecord.PEM = PEM
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command =="WEM"):
                        WEM = entry[entry.index("=")+2:]
                        if (re.fullmatch(r"([\x00-\x7F]+@[\x00-\x7F]+\.[\x00-\x7F]+){1}", WEM) and len(WEM) < 65 ) or re.fullmatch("", WEM):
                            newRecord.WEM = WEM
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif(command=="PPH"):
                        PPH = entry[entry.index("=")+2:]
                        if re.fullmatch(r"\d{1,10}", PPH) or re.fullmatch("", PPH):
                            newRecord.PPH = PPH
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif(command=="WPH"):
                        WPH = entry[entry.index("=")+2:]
                        if re.fullmatch(r"\d{1,10}", WPH) or re.fullmatch("", WPH):
                            newRecord.WPH = WPH
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command=="SA"):
                        SA = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", SA) or re.fullmatch("", SA):
                            newRecord.SA = SA
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command=="CITY"):
                        CITY = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", CITY) or re.fullmatch("", CITY):
                            newRecord.CITY = CITY
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command=="STP"):
                        STP = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", STP) or re.fullmatch("", STP):
                            newRecord.STP = STP
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command =="CTY"):
                        CTY = entry[entry.index("=")+2:]
                        if re.fullmatch(r"[\x00-\x7F]{1,64}", CTY) or re.fullmatch("", CTY):
                            newRecord.CTY = CTY
                        else:
                            print("One or more invalid record data fields")
                            return
                    elif (command =="PC"):
                        PC = entry[entry.index("=")+2:]
                        if re.fullmatch(r"\d{5}",PC) or re.fullmatch("", PC):
                            newRecord.PC = PC
                        else:
                            print("One or more invalid record data fields")
                            return                   
                    else:
                        print("One or more invalid record data fields")
                        return
                        
                
                lines[i] = (self.encrypt_string(newRecord.recordID)+b";"+
                self.encrypt_string(newRecord.SN)+b";"+
                self.encrypt_string(newRecord.GN)+b";"+
                self.encrypt_string(newRecord.PEM)+b";"+
                self.encrypt_string(newRecord.WEM)+b";"+
                self.encrypt_string(newRecord.PPH)+b";"+
                self.encrypt_string(newRecord.WPH)+b";"+
                self.encrypt_string(newRecord.SA)+b";"+
                self.encrypt_string(newRecord.CITY)+b";"+
                self.encrypt_string(newRecord.STP)+b";"+
                self.encrypt_string(newRecord.CTY)+b";"+
                self.encrypt_string(newRecord.PC)+b"\n")
                
                f.close()
                outFile = open((self.current_user + ".txt"), "wb")
                outFile.writelines(lines)
                outFile.close()
                        
                print("OK") 
                return
                
                
        f.close()
        print("RecordID not found")      
        return         

    def clean_inputs(self, string):
        #check if all things end in " when split 
        self.tokens = " ".join(self.tokens[2:])
        self.tokens = self.tokens.split('" ')
        self.tokens[-1] = self.tokens[-1][0:-1]
        
        return 1

    def get_record(self): 
        """
        Gets a record from the database 
        """
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if current user is an admin
        if self.current_user == "admin":
            print("Admin not authorized")
            return
        #check if recordID passed has correct format
        if not re.fullmatch(r"[\x00-\x7F]{1,64}", self.tokens[1]):
            print("Invalid recordID") 
            return
        #If the record ID does not exist
        if (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return
        
        #print all elements 
        if (len(self.tokens)<=2):
            #Open the users file
            f = open((self.current_user + ".txt"), "rb")
            lines = f.readlines()
            #loop through the data
            for i in range(len(lines)):
                tokens = lines[i].split(b";")
                tokens[0] = self.decrypt_string(tokens[0])
                #when matching record ID found, print it
                if (tokens[0] == self.tokens[1]):
                    print(tokens[0] +
                    " SN="+self.decrypt_string(tokens[1]) +
                    " GN="+self.decrypt_string(tokens[2]) +
                    " PEM="+self.decrypt_string(tokens[3]) +
                    " WEM="+self.decrypt_string(tokens[4]) +
                    " PPH="+self.decrypt_string(tokens[5]) +
                    " WPH="+self.decrypt_string(tokens[6]) +
                    " SA="+self.decrypt_string(tokens[7]) +
                    " CITY="+self.decrypt_string(tokens[8]) +
                    " STP="+self.decrypt_string(tokens[9]) +
                    " CTY="+self.decrypt_string(tokens[10]) +
                    " PC="+self.decrypt_string(tokens[11].rstrip()))
            f.close()
            print("OK")
            return
        #print specfic elements
        else:
            #open the users file
            f = open((self.current_user + ".txt"), "rb")
            lines = f.readlines()
            #loop through the data
            for i in range(len(lines)):
                tokens = lines[i].split(b";")
                tokens[0] = self.decrypt_string(tokens[0])
                #if matching record ID found
                if (tokens[0] == self.tokens[1]):
                    outputValue=self.tokens[1] + " "
                    #loop through parsed command, printing matching 
                    for i in range(2,len(self.tokens)):
                        #i and loop through all self.tokens
                        if (self.tokens[i] == "SN"): 
                            outputValue += "SN="+ self.decrypt_string(tokens[1])+" "
                        elif self.tokens[i] == "GN":
                            outputValue += "GN="+ self.decrypt_string(tokens[2])+" "
                        elif self.tokens[i] == "PEM":
                            outputValue += "PEM="+ self.decrypt_string(tokens[3])+" "
                        elif self.tokens[i] == "WEM":
                            outputValue += "WEM="+ self.decrypt_string(tokens[4])+" "
                        elif self.tokens[i] == "PPH":
                            outputValue += "PPH="+ self.decrypt_string(tokens[5])+" "
                        elif self.tokens[i] == "WPH":
                            outputValue += "WPH="+ self.decrypt_string(tokens[6])+" "
                        elif self.tokens[i] == "SA":
                            outputValue += "SA="+ self.decrypt_string(tokens[7])+" "
                        elif self.tokens[i] == "CITY":
                            outputValue += "CITY="+ self.decrypt_string(tokens[8])+" "
                        elif self.tokens[i] == "STP":
                            outputValue += "STP="+ self.decrypt_string(tokens[9]) +" "
                        elif self.tokens[i] == "CTY":
                            outputValue += "CTY="+ self.decrypt_string(tokens[10]) +" "
                        elif self.tokens[i] == "PC":
                            outputValue += "PC="+ self.decrypt_string(tokens[11].rstrip()) +" "

                        else:
                            #field invalid
                            print("Invalid fieldname (s)")
                            return

            print(outputValue)
            print("Ok")
            f.close()
            return

    def display_audit_log(self):
        """
        Displays the audit log 
        """   
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
        #if the admin is not logged in
        elif self.current_user != "admin":
            print("Admin not active")
        #if user ID is provided
        elif len(self.tokens) > 1:
            if self.tokens[1] == "admin" or not re.fullmatch(r"[A-Za-z0-9]{1,16}",self.tokens[1]):
                print("Invalid userID")
                return
            #if valid user ID
            login_info = open("logininfo.txt", "rb")
            lines = login_info.readlines()
            for i in range(len(lines)):
                user_pass = lines[i].split(b",")
                user_pass[0] = self.decrypt_string(user_pass[0])
                #if a matching username is found
                if user_pass[0].rstrip() == self.tokens[1]:
                    #display audit log for that user
                    login_info.close()
                    auditlog = open("audit_log.csv", "rb")
                    for line in auditlog:
                        line = self.decrypt_string(line.rstrip())
                        audit_record = line.split(",")
                        if audit_record[3].rstrip() == self.tokens[1]:
                            print(audit_record[0] + "," +audit_record[1] + "," + audit_record[2] + "," + audit_record[3])
                    print("Ok")
                    return
            print("Account does not exist")
        #if the admin is logged in
        else:    
            auditlog = open("audit_log.csv", "rb")
            for line in auditlog:
                line = self.decrypt_string(line.rstrip())
                audit_record = line.split(",")
                print(audit_record[0] + "," + audit_record[1] + "," + audit_record[2] + "," + audit_record[3].rstrip()) 
        return
    
    def delete_user(self):
        """
        Deletes a user from the Address Book
        """  
        username = self.tokens[1]
        
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        elif self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        else:
            #do not let admin delete himself
            if username == "admin" or not re.fullmatch(r"[A-Za-z0-9]{1,16}",username):
                print("Invalid userID")
                return
            infile = open("logininfo.txt", "rb")
            lines = infile.readlines()
            for i in range(len(lines)):
                toks = lines[i].split(b",")
                toks[0] = self.decrypt_string(toks[0])
                #if a matching username is found
                if toks[0].rstrip() == username:
                    #delete it from login info
                    lines[i] = b""
                    infile = open("logininfo.txt", "wb")
                    infile.writelines(lines)
                    infile.close()
                    #delte user data
                    if os.path.exists(username+".txt"):
                        os.remove(username+".txt")
                    print("Ok")
                    self.add_to_audit_log("DU")
                    return
            infile.close()
            print("Invalid userID")
            return

    def add_user(self):
        """
        Adds a new user to the Address Book
        """   
        username = self.tokens[1]
        
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        elif self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        else:
            if username == "admin" or not re.fullmatch(r"[A-Za-z0-9]{1,16}",username):
                print("Invalid userID")
                return
            infile = open("logininfo.txt", "rb")
            lines = infile.readlines()
            if len(lines) > 7:
                print("Invalid userID")
                return
            for i in range(len(lines)):
                toks = lines[i].split(b",")
                toks[0] = self.decrypt_string(toks[0])
                #if a matching username is found
                if toks[0].rstrip() == username:
                    #do not add it
                    infile.close()
                    print("Account already exists")
                    return
            #if account does not exist encrypt and add it
            username = self.encrypt_string(username)
            infile = open("logininfo.txt", "ab")
            infile.write(username + b"\n")
            infile.close()
            self.add_to_audit_log("AU")
            print("Ok")

    def add_to_audit_log(self, audit_type):
        auditlog_r = open("audit_log.csv", "rb")
        #If reached max length of audit log, delete first line
        lines = auditlog_r.readlines()
        if len(lines) > 511:
            auditlog_r.close()
            auditlog_w = open("audit_log.csv", "wb")
            auditlog_w.writelines(lines[1:])
            auditlog_w.close()
        e = datetime.datetime.now()
        #if there is currently no user
        auditlog_a = open("audit_log.csv", "ab")
        if self.current_user == None:
            audit = str(e.day) +"-"+ str(e.month) +"-"+ str(e.year) + "," + str(e.hour) +":"+ str(e.minute) +":"+ str(e.second) + "," + audit_type + "," 
            auditlog_a.write(self.encrypt_string(audit)+ b"\n")   
        #if there is a user
        else:
            audit = str(e.day) +"-"+ str(e.month) +"-"+ str(e.year) + "," + str(e.hour) +":"+ str(e.minute) +":"+ str(e.second) + "," + audit_type + "," + str(self.current_user.rstrip())
            auditlog_a.write(self.encrypt_string(audit) + b"\n")      
        auditlog_a.close()

    def encrypt_string(self, string):
        key = b"fyVx1pfKNXcIFd-h6Qvo2zbTI3lVGoxQTsOJQFLWMPs="
        f = Fernet(key)
        encrypted = f.encrypt(string.encode())  # Encrypt the bytes. The returning object is of type bytes
        return encrypted

    def decrypt_string(self, string):
        key = b"fyVx1pfKNXcIFd-h6Qvo2zbTI3lVGoxQTsOJQFLWMPs="
        f = Fernet(key)
        decrypted = f.decrypt(string).decode()
        return decrypted        

if __name__ == "__main__":
    Address_Book()
