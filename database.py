import sqlite3
import sys
import os

class Database:

    def __init__(self):
        connection = sqlite3.connect(r'PasswordManger.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE PASSWORDS 
                        ([Website] text, [User_Name] text, [Password] text)''')
        connection.commit()
