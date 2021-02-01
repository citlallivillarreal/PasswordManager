import sqlite3
import sys
import os

master_user = "Lali"
master_password = "passwordmanager123"

COMMANDS = ["user", "password", "add", "delete", "exit"]


def user_auth(user):
    """
    Verifies if client entered the correct USER. Will abort system if attempts are exhausted.

    :param user: the username the client inputs.
    """
    if master_user == user:
        password = input("Hello, Lali! Please provide your password: ")
        password_auth(password)
    else:
        attempts = 3
        tries = 0
        while tries != attempts:
            user = input("Incorrect user. Try Again: ")
            if master_user == user:
                password = input("Hello, Lali! Please provide your password: ")
                password_auth(password)
            tries += 1
        sys.exit("Maximum attempts reached")


def password_auth(password):
    """
    Verifies if user entered the correct PASSWORD. Will abort system if attempts are exhausted.

    :param password: the password the user inputs.
    """
    if master_password == password:
        return
    else:
        attempts = 3
        tries = 0
        while tries != attempts:
            password = input("Incorrect password. Try Again: ")
            if master_password == password:
                return
            tries += 1
        sys.exit("Maximum attempts reached")


def user_commands_display():
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


def fetch_user(db_file):
    """
    Displays the username of a website requested by the user (client).

    :param db_file: the name of the database file
    :return:
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    website = input("What website?\n")
    cursor.execute("""SELECT User_Name FROM PASSWORDS where Website =?""", (website,))
    username = cursor.fetchone()
    print(username[0])
    connection.commit()
    connection.close()

def fetch_password(db_file):
    """
    Displays the password of a website requested by the user (client).

    :param db_file: the name of the database file
    :return:
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    website = input("What website?\n")
    cursor.execute("""SELECT Password FROM PASSWORDS where Website = ?""", (website,))
    password = cursor.fetchone()
    print(password[0])
    connection.commit()
    connection.close()

def create_record(web, user, password, db_file):
    """
    Creates a data entry.

    :param web: client entered website name
    :param user: client entered username
    :param password: client entered password
    :param db_file: the database file
    :return:
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO PASSWORDS (Website, User_Name, Password) VALUES (?, ?, ?)""", (web, user, password))
    connection.commit()
    connection.close()


def add(db_file):
    """
    Request clients information: website name, username, and password. Creates a new data entry. ADD uses
    helper function, CREATE_RECORD.

    :param db_file: the database file
    :return:
    """
    website = input("Website Name: ")
    username = input("username: ")
    password = input("password: ")
    create_record(website, username, password, db_file)

def delete(db_file):
    """
    Delete clients username and password information for a particular website

    :param db_file: the database file
    :return:
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    website = input("Delete login information from what website?")
    cursor.execute("""DELETE FROM PASSWORDS WHERE Website = ?""", (website,))
    connection.commit()
    connection.close()

def terminate():
    """
    Terminates the program if desired by the client.

    :return:
    """
    response = input("Anything else? (Yes or No) \n")
    if response == "No":
        sys.exit("Thank you, have a nice day!")
    elif response == "Yes":
        return
    elif response != "Yes" or response != "No":
        print("Invalid command. Try Again")
        terminate()



def main():
    db = r'PasswordManager.db'
    if not os.path.isfile(db):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE PASSWORDS
                        ([Website] text, [User_Name] text, [Password] text)''')
        connection.commit()
        connection.close()
    username = input("Please provide your user: ")
    user_auth(username)
    print("Access Authorization Completed.\n")
    user_commands_display()
    while (True):
        command = input("Enter Command: ")
        if command in COMMANDS:
            if command == "user":
                fetch_user(db)
            elif command == "password":
                fetch_password(db)
            elif command == "add":
                add(db)
            elif command == "delete":
                delete(db)
            else:
                sys.exit("Thank you, have a nice day!")
            terminate()
        else:
            print("Command Invalid. Try again.")




if __name__ == "__main__":
    main()
