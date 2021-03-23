import unittest
import main
import sqlite3
from unittest import mock


import os


class MyTestCase(unittest.TestCase, main.Database):

    test_db = r'testPasswordManager'
    test_database = main.Database('test database', 'testuser', 'testpass', test_db)

    @classmethod
    def setUpClass(cls):

        connection = sqlite3.connect(cls.test_db)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE PASSWORDS
                        ([Website] text, [User_Name] text, [Password] text)""")
        cursor.executemany("""INSERT INTO PASSWORDS (Website, User_Name, Password) VALUES  (?, ?, ?)""",
                           [("Youtube", "mary", "marypass1$"),
                            ("Netflix", "cris", "crispass1$"),
                            ("Hulu", "lali", "lalipass1$"),
                            ("Spotify", "darian", "darianpass1$")])

        connection.commit()
        connection.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_db)

    @mock.patch("builtins.print")
    def test_fetch_user(self, mock_print):
        with mock.patch('builtins.input', side_effect=["Youtube", "Netflix"]):
            self.test_database.fetch_user()
            mock_print.assert_called_with("mary")

            self.test_database.fetch_user()
            mock_print.assert_called_with("cris")


if __name__ == '__main__':
    unittest.main()
