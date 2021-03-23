import sqlite3
import os


class MasterDatabase:
    db = r'MasterDatabase.db'

    def __init__(self):
        if not os.path.isfile(MasterDatabase.db):
            connection = sqlite3.connect(MasterDatabase.db)
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE MASTER ([Full_Name] text, [Master_User] text, 
                            [Master_Password] text, [Database_Name] db,[Information] json)""")
            connection.commit()
            connection.close()

    def add(self, client_name, master_user, master_pass, db_file, data):
        connection = sqlite3.connect(MasterDatabase.db)
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO MASTER (Full_Name, Master_User, Master_Password, Database_Name, Information) 
                        VALUES (?, ?, ?, ?, ?)""", (client_name, master_user, master_pass, db_file, data))
        connection.commit()
        connection.close()

    def delete(self, client_name, master_user, master_pass):
        connection = sqlite3.connect(MasterDatabase.db)
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM MASTER WHERE (Full_Name = ? AND Master_User = ? AND Master_Password = ?)""",
                       (client_name, master_user, master_pass))
        connection.commit()
        connection.close()

    def update(self, master_user, master_pass, data):
        connection = sqlite3.connect(MasterDatabase.db)
        cursor = connection.cursor()
        cursor.execute("""UPDATE MASTER SET Information = ? WHERE
                        (Master_User = ? AND Master_Password = ?) """,
                       (data, master_user, master_pass))
        connection.commit()
        connection.close()

    def user_auth(self, master_user, master_password):
        connection = sqlite3.connect(MasterDatabase.db)
        cursor = connection.cursor()
        cursor.execute("""SELECT EXISTS (SELECT 1 FROM MASTER WHERE Master_User = ? AND Master_Password = ?)""",
                       (master_user, master_password))
        exist = cursor.fetchone()
        connection.commit()
        connection.close()
        return exist

    def retrieve_data(self, master_user, master_password):
        connection = sqlite3.connect(MasterDatabase.db)
        cursor = connection.cursor()
        cursor.execute("""SELECT Information FROM MASTER WHERE (Master_User = ? AND Master_Password = ?)""",
                       (master_user, master_password))
        data = cursor.fetchone()

        return data[0]
