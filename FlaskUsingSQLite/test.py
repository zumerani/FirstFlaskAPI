#How to interact with SQLite

import sqlite3 #Already in Python Standard Library -- allows us to connect to DB and run queries

#Initialize a connection
connection = sqlite3.connect('data.db') #We will create a file called 'data.db' which has our data.

cursor = connection.cursor() #Cursor allows one to select and start things. We can point
                             #the cursor to different places in the databse. Cursors can
                             #run queries, access results, store results, etc.
##Create a table
create_table = "CREATE TABLE users (id int , username text , password text )" #This is a query. Three columns (id, un, and pass)

##Execute one query:

cursor.execute(create_table) #Runs the query above.

user = (1 , 'jose' , 'asdf') #Creates a user tuple.
insert_query = "INSERT INTO users VALUES (? , ? , ?)"
cursor.execute(insert_query , user ) #'user' replaces the question marks above. Cursor knows what to do.

##Exectute many queries

#We have a list of 'user' tuples
users = [
    (2 , 'rolf' , 'asdf') ,
    (3 , 'anne' , 'xyz' )
]

cursor.executemany( insert_query , users ) #This will take each tuple one by one and insert into table.

##Retrieve Data:
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query): #cursor.execute returns a table essentially and we go through each row and print the row.
    print(row)


connection.commit() #In order to write to disk (data.db), we need to run commit().

connection.close()
