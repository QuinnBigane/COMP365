"""
Name: ABA.py
Date: 4/18/2021
Author: Quinn Bigane, Tom Padova, Bo Kulbacki
Description: This is a secure implementation of an Address Book database 
"""
 
import re

class Address_record:
    def __init__(self, recordID, SN='', GN='', PEM='', WEM='', PPH='', WPH='', SA='', CITY='', STP='', CTY='', PC=''):
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
    def __init__(self, login_state = 0,current_user = None):
        self.login_state = login_state
        
        self.driver()
        
    
    
    """
    Main looping module of the function, waits for user input
    """   
    def driver(self):
        #possible vars: active_login (1=yes, 2=no)
        #loop to wait for user input

        print("Address Book Application, version 1.0. Type “HLP” for a list of commands") #print this when the program first starts
         
        while(1):
            #prompt user to enter a command
            command = input("ABA >")
            self.command_line_interpreter(command)

    
    
    """
    Interprets user input and decides what to do based on that
    """   
    def command_line_interpreter(self, command):
        #parse command entered on spaces
        self.tokens = None
        self.tokens = command.split(" ")
        #TODO: Add command entered to audit log
        
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
    
    """
    Exits ABA
    """
    def exit(self):
        exit()
    """
    Verifies user login credentials based on a database of login info
    """  
    def login(self):
        #TODO: Add error handling if user does not enter a username with LIN



        username = self.tokens[1]
        infile = open("logininfo.txt", "r")

        #if there is currently an active login
        if self.login_state != 0: 
            print("An account is currently active; logout before proceeding")
        

        #if there is no currently active login
        else:
            #loop through all login data
            lines = infile.readlines()
            for i in range(len(lines)):
                toks = lines[i].split(",")
                #matching username found
                if toks[0].rstrip() == username:
                    #no password associated with username
                    if len(toks) == 1: 
                        new_password = input("This is the first time the account is being used. You must create a new password. Passwords may contain 1-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
                        pw_confirmation = input("Reenter the same password: ")
                        #TODO: add error handling if user does not meet password specifications
                        if new_password != pw_confirmation:
                            print("Passwords do not match")
                            infile.close()
                            return
                        else:
                            lines[i] = lines[i].rstrip() + "," + new_password + "\n"
                            infile = open("logininfo.txt", "w")
                            infile.writelines(lines)
                            infile.close()
                            print("OK")
                            self.current_user = toks[0]
                            self.login_state = 1
                            infile.close()
                            return
                    #username has a password
                    else:
                        password = toks[1].rstrip() #users's password
                        password_guess = input("Enter your password: ")
                        if password == password_guess: #correct password entered
                            #set current user variables
                            self.current_user = toks[0]
                            self.login_state = 1
                            print("OK")
                            infile.close()
                            return
            infile.close()
            print("Invalid credentials")    




    """
    Logs out current user
    """  
    def logout(self):
        if self.login_state == 0: #no active login session
            print("No active login session")

        else:
            self.login_state = 0
            self.current_user = None
            print("OK")

    """
    Logs out current user
    """  
    def change_password(self):
        #TODO:
        print("Change password called")      
    
    """
    Display Users
    """  
    def list_users(self):
        #TODO:
        print("list users called")

    """
    Displays the help commands
    """    
    def display_help(self):
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
            else:
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
        
        else: #if user only entered HLP or an incorrect command
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


    
    """
    Imports a database
    """
    def import_database(self):
        #TODO:
        print("import database called")    
    
    """
    Exports current user database 
    """ 
    def export_database(self):
        #TODO:
        print("export database called")    
    
    """
    Adds a new record for user
    """ 
    def add_record(self):
        #TODO:
        print("addd record called")    
    
    """
    Deletes a record from the database
    """ 
    def delete_record(self):
        #TODO:
        print("delete record called")    
    
    """
    Edits a record from the database
    """  
    def edit_record(self):
        #TODO:
        print("edit record called")    
    
    """
    Gets a record from the database 
    """    
    def get_record(self):
        #TODO:
        print("get record called")    
    
    """
    Displays the audit log 
    """     
    def display_audit_log(self):
        #TODO:
        print("display audit log called")   
    
    """
    Deletes a user from the Address Book
    """  
    def delete_user(self):
        #TODO:
        print("delete user called")   
    
    """
    Adds a new user to the Address Book
    """       
    def add_user(self):
        #TODO:
        print("add user called")



if __name__ == "__main__":
    Address_Book()
