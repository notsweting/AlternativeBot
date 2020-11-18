import sqlite3

connection = sqlite3.connect('muted.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE MUTEDROLES(ServerID, RoleID)')

connection.commit()
connection.close()