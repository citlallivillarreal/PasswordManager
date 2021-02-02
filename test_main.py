import unittest
import main
import sqlite3
from unittest.mock import patch
import os


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = r'testPasswordManager'
        connection = sqlite3.connect(cls.db)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE PASSWORDS
                        ([Website] text, [User_Name] text, [Password] text)""")
        connection.commit()
        connection.close()

    @classmethod
    def tearDownClass(cls):
        cls.db = r'testPasswordManager'
        os.remove(cls.db)


    def test_create_record(self):
        web = "Youtube"
        user = "Mary"
        password = "pass123"
        main.create_record(web, user, password, MyTestCase.db)





if __name__ == '__main__':
    unittest.main()
