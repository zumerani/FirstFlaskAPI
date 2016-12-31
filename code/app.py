from flask import Flask, request
from flask_restful import Resource, Api #Resource is just a 'thing' that our API can handle with or return

#Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

app = Flask(__name__)
api = Api(app)

items = [] #Contains a dictionary for each item

class Item(Resource): #'Student' will inherit from 'Resource'
    def get(self , name): #This resource can only be accessed with 'get' ... if you want 'post' add a post method
        for item in items:
            if item['name'] == name:
                return item #We are using flask_restful, so no need to return JSON, it is done for you.
        return {'item' : None }, 404

    def post(self , name):
        item = {'name' : name , 'price' : 12.00 }
        items.append(item)
        return item, 201

#Passing in 'Item' tells 'Api' that 'Student' is accessible in the API.
api.add_resource(Item , '/item/<string:name>')

app.run(port=5000)
