from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


#Importing Models (user and item) and other files
from security import authenticate , identity
from resources.user import UserRegister
from resources.item import Item, ItemList

#Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

app = Flask(__name__)
app.secret_key = 'zain'
api = Api(app)

jwt = JWT(app , authenticate , identity )


#Passing in 'Item' tells 'Api' that 'Student' is accessible in the API.
api.add_resource(Item , '/item/<string:name>')
api.add_resource(ItemList , '/items')
api.add_resource(UserRegister , '/register')

#In Python, when something is run, it assigns '__main__' to it so we do the if-statement
#below because when we run a file we want to make sure it is app.py.
#This is a safeguard, so if this file is imported it will not perform 'app.run( ... )'.
if __name__ == '__main__':
    app.run(port=5000 , debug=True) #debug=True helps you debug easier with HTML pages
