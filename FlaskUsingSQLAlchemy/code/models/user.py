from db import db

class UserModel(db.Model): #Extends db.Model
    __tablename__ = "users" #Tells SQLAlchemy what the name of our table is

    ##Note: The following three (id, user, pass) need to match with whatever
    ##you are passing in the constructor!! (__init__)

    id = db.Column(db.Integer , primary_key = True ) #Tells SQLAlchemy that there is a column called id
                                                     #Primary Key makes it unique.
                                                     #Whenever we create a UserModel through SQLAlchemy,
                                                     #an ID is automatically generated and given to us.

    username = db.Column(db.String(80)) #80 characters maximum
    password = db.Column(db.String(80))

    def __init__(self , username , password):
        #No need to specify ID, SQLAlchemy autmoatically does it
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls , username):
        return cls.query.filter_by(username=username).first() #Grabs the first row -- Then SQLAlchemy converts it to a UserModel type.

    @classmethod
    def find_by_id(cls , _id):
        return cls.query.filter_by(id=_id)

    def save_to_db(self):
        db.session.add(self) #Adds 'UserModel' to session container
        db.session.commit()
