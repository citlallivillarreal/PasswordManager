import sqlite3
import sys
import os

master_user = "Lali"
master_password = "passwordmanger123"

COMMANDS = ["user", "password", "add", "delete"]


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
    print("----------------------------------------------------\n")


def main():
    user = input("Please provide your user: ")
    user_auth(user)
    print("Access Authorization Completed.\n")
    user_commands_display()
    command = input("Enter Command: ")
    while (True):
        if command in COMMANDS:
            if command == "user":
                pass
            elif command == "password":
                pass
            elif command == "add":
                pass
            else:
                pass
        else:
            print("Command Invalid. Try again.")
            command = input("Enter Command: ")


if __name__ == "__main__":
    main()
