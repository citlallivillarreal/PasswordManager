import sqlite3
import sys
import os
import masterdb
import json

COMMANDS = ["user", "password", "add", "delete", "exit"]


class Database:

    def __init__(self, client_name=None, master_user=None, master_password=None, database=r'PASSWORDS.db', data=None):
        self.client_name = client_name
        self.master_user = master_user
        self.master_password = master_password
        self.database = database
        self.data = data

    def authenticate(self):
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            self.master_user = input("Please provide username: ")
            self.master_password = input("Please provide your password: ")
            masterdb_init = masterdb.MasterDatabase()
            exist = masterdb_init.user_auth(self.master_user, self.master_password)[0]
            if exist == 0:
                print("Incorrect username or password")
                response = input("Would you like to signup? (Yes or No): ").lower()
                if response == "yes":
                    self.client_name = input("Full Name: ")
                    self.master_user = input("New master username: ")
                    self.master_password = input("New master password: ")
                    connection = sqlite3.connect(self.database)
                    cursor = connection.cursor()
                    cursor.execute("""CREATE TABLE PASSWORDS
                             ([Website] text, [User_Name] text, [Password] text)""")
                    cursor.execute("""SELECT * FROM PASSWORDS""")
                    connection.commit()
                    self.data = json.dumps([])
                    masterdb_init.add(self.client_name, self.master_user, self.master_password, self.database,
                                      self.data)
                    connection.close()
                    break
                else:
                    attempts += 1
            else:
                connection = sqlite3.connect(self.database)
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE PASSWORDS
                                       ([Website] text, [User_Name] text, [Password] text)""")
                connection.close()
                break
        if attempts == max_attempts:
            sys.exit("Maximum attempts reached")

    def user_commands_display(self):
        """
        Displays a set of valid commands to the user.
        """
        print("-----------------COMMAND MENU-----------------------")
        print("--            user - Fetch User                   --")
        print("--            password - Fetch Password           --")
        print("--            add - ADD Website Information       --")
        print("--            delete - DELETE Record              --")
        print("--            exit - Exit Program                 --")
        print("----------------------------------------------------\n")

    def fetch_user(self):
        """
        Displays the username of a website requested by the user (client).

        :param:
        :return:
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        website = input("What website?\n")
        cursor.execute("""SELECT User_Name FROM PASSWORDS where Website =?""", (website,))
        connection.commit()
        username = cursor.fetchone()
        connection.close()
        print(username[0])

    def fetch_password(self):
        """
        Displays the password of a website requested by the user (client).

        :param:
        :return:
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        website = input("What website?\n")
        cursor.execute("""SELECT Password FROM PASSWORDS where Website = ?""", (website,))
        connection.commit()
        password = cursor.fetchone()
        print(password[0])
        connection.close()

    def create_record(self, web, user, password):
        """
        Creates a data entry.

        :param web: client entered website name
        :param user: client entered username
        :param password: client entered password
        :param db_file: the database file
        :return:
        """

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO PASSWORDS (Website, User_Name, Password) VALUES (?, ?, ?)""",
                       (web, user, password))
        connection.commit()
        connection.close()

    def add(self):
        """
        Request clients information: website name, username, and password. Creates a new data entry. ADD uses
        helper function, CREATE_RECORD.

        :param:
        :return:
        """
        website = input("Website Name: ")
        username = input("username: ")
        password = input("password: ")
        if (len(website) | len(username) | len(password)) < 1:
            print("Invalid input length")
            self.add()

        self.create_record(website, username, password)

    def delete(self):
        """
        Delete clients username and password information for a particular website

        :param:
        :return:
        """
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        website = input("Delete login information from what website?")
        cursor.execute("""DELETE FROM PASSWORDS WHERE Website = ?""", (website,))
        connection.commit()
        connection.close()

    def terminate(self):
        """
        Terminates the program if desired by the client.

        :return:
        """
        response = input("Anything else? (Yes or No) \n")
        if response == "No":
            os.remove(self.database)
            sys.exit("Thank you, have a nice day!")
        elif response == "Yes":
            return
        elif response != "Yes" or response != "No":
            print("Invalid command. Try Again")
            self.terminate()

    def main(self):
        self.authenticate()
        print("Access Authorization Completed.\n")
        masterdb_init = masterdb.MasterDatabase()
        json_data = masterdb_init.retrieve_data(self.master_user, self.master_password)

        self.data = json.loads(json_data)
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        # cursor.execute("""CREATE TABLE PASSWORDS
        #             ([Website] text, [User_Name] text, [Password] text)""")
        for lst in self.data:
            cursor.execute("""INSERT INTO PASSWORDS VALUES (?, ?, ?)""", lst)
        connection.commit()
        connection.close()
        self.user_commands_display()
        while True:
            connection = sqlite3.connect(self.database)
            cursor = connection.cursor()
            command = input("Enter Command: ")
            if command in COMMANDS:
                if command == "user":
                    self.fetch_user()
                elif command == "password":
                    self.fetch_password()
                elif command == "add":
                    self.add()
                elif command == "delete":
                    self.delete()
                else:
                    os.remove(self.database)
                    sys.exit("Thank you, have a nice day!")
                cursor.execute("""SELECT * FROM PASSWORDS""")
                connection.commit()
                json_data = json.dumps(cursor.fetchall())
                masterdb_init.update(self.master_user, self.master_password, json_data)
                connection.close()
                self.terminate()
            else:
                print("Command Invalid. Try again.")


if __name__ == "__main__":
    db = Database()
    db.main()
