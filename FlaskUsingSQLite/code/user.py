import sqlite3 #'User' can now interact with SQLite database.


class User:
    def __init__(self , _id , username , password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls , username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute( query , (username,) ) #'username' fills the ? above.
                                                       #Note: Parameters have to be tuple (single tuple
                                                       #is the username followed by a ',').
        row = result.fetchone()
        if row is not None:
            user = cls( row[0] , row[1] , row[2] ) #0, 1, 2 are columns 0, 1, and 2.
            #user = User( *row ) -- Equivalent to above. *row grabs all.
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls , _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute( query , (_id,) ) #'username' fills the ? above.
                                                       #Note: Parameters have to be tuple (single tuple
                                                       #is the username followed by a ',').
        row = result.fetchone()
        if row is not None:
            user = cls( row[0] , row[1] , row[2] ) #0, 1, 2 are columns 0, 1, and 2.
            #user = User( *row ) -- Equivalent to above. *row grabs all.
        else:
            user = None

        connection.close()
        return user
