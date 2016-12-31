from flask import Flask, request
from flask_restful import Resource, Api #Resource is just a 'thing' that our API can handle with or return

#Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

app = Flask(__name__)
api = Api(app)

items = [] #Contains a dictionary for each item

class Item(Resource): #'Item' will inherit from 'Resource'
    def get(self , name): #This resource can only be accessed with 'get' ... if you want 'post' add a post method
        item = next( filter(lambda x : x['name'] == name , items ) , None ) # This returns a filter object, so we can use 'next' to
        return item, 200 if item is not None else 404                       # get the first found item. We can called 'next' many
                                                                            # times. The second parameter 'None' is used to return
                                                                            # 'None' if 'filter' cannot find an item. Performing
                                                                            # 'next' on something not found will produce an error.


    def post(self , name):
        if next( filter(lambda x : x['name'] == name , items ) , None ) is not None: #Item exists
            return { 'message' : 'Item: {} already exists.'.format(name) }, 400
        else:
            data = request.get_json() #When someone sends a request, it is in the 'request' object
            item = { 'name' : name , 'price' : data['price'] }
            items.append(item)
            return item, 201


class ItemList(Resource):
    def get(self):
        return { 'items' : items }

#Passing in 'Item' tells 'Api' that 'Student' is accessible in the API.
api.add_resource(Item , '/item/<string:name>')
api.add_resource(ItemList , '/items')

app.run(port=5000 , debug=True) #debug=True helps you debug easier with HTML pages
