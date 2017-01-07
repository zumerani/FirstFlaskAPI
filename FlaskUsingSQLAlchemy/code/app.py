from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


#Importing Models (user and item) and other files
from security import authenticate , identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store , StoreList

#Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #Tells SQLAlchemy where our databse (data.db) is (it is at /data.db). It doesn't have to be 'sqlite' it can be postgres or mysql, etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turns off flask_sqlalchemy modification tracker, but not SQLAlchemy modification behavior
app.secret_key = 'zain'
api = Api(app)

@app.before_first_request
def create_tables(): #Runs the method below ONLY when we have the first request
    db.create_all() #This goes through our model .py files and creates a table based on
                    #__tablename__ and the Column representations. So importing the correct
                    #models/files is very important.

jwt = JWT(app , authenticate , identity )


#Passing in 'Item' tells 'Api' that 'Student' is accessible in the API.
api.add_resource(Item , '/item/<string:name>')
api.add_resource(ItemList , '/items')
api.add_resource(UserRegister , '/register')
api.add_resource(Store , '/store/<string:name>')
api.add_resource(StoreList , '/stores')

#In Python, when something is run, it assigns '__main__' to it so we do the if-statement
#below because when we run a file we want to make sure it is app.py.
#This is a safeguard, so if this file is imported it will not perform 'app.run( ... )'.
if __name__ == '__main__':
    from db import db
    db.init_app(app) #Pass in the flask app
    app.run(port=5000 , debug=True) #debug=True helps you debug easier with HTML pages
