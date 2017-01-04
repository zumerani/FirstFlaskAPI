import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#For auto-incrementing columns we have to use 'INTEGER'. No need to specify ID when creating a new user.
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()
