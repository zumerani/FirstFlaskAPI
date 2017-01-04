from flask import Flask, request
from flask_restful import Resource, Api, reqparse #Resource is just a 'thing' that our API can handle with or return
from flask_jwt import JWT, jwt_required, current_identity #jwt_required is a decorator
from security import authenticate , identity #import the two functions from security.py
#Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

app = Flask(__name__)
app.secret_key = 'zain'
api = Api(app)

jwt = JWT(app , authenticate , identity )

items = [] #Contains a dictionary for each item

class Item(Resource): #'Item' will inherit from 'Resource'
    @jwt_required() #You put this as a decorator. The function below will only run once you have a token.
    def get(self , name): #This resource can only be accessed with 'get' ... if you want 'post' add a post method
        print("Username is: {}".format(current_identity.username))
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
            print("data is {}".format(data))
            item = { 'name' : name , 'price' : data['price'] }
            items.append(item)
            return item, 201

    def delete(self , name):
        global items
        items = list(filter(lambda x: x['name'] != name , items))
        return {'message': 'Item deleted'}

    #In REST, 'put' methods are idempotent -- No matter how many times called, it will never add anything extra to 'items'.
    def put(self , name):
        parser = reqparse.RequestParser()
        parser.add_argument('price' , type=float , required=True ,
            help="This field cannot be left blank!") #This ensures that whatever the user requests is a float, and is
                                                     #actually present.

        data = parser.parse_args() #This will parse the arguments coming through the payload in the line above.

        #Whats cool is that data will only have a 'price' field. Even if the user passes another key to 'PUT' like
        #'name' ... it will not be a key in the 'data' dictionary because our parser does not expect anything but
        #'price'.

        item = next( filter( lambda x: x['name'] == name , items ) , None )
        if item is None:
            item = {'name' : name , 'price': data['price'] }
            items.append(item)
        else:
            item.update(data) #The update function will replace the dictionary in the list with 'data'.
        return item


class ItemList(Resource):
    def get(self):
        return { 'items' : items }

#Passing in 'Item' tells 'Api' that 'Student' is accessible in the API.
api.add_resource(Item , '/item/<string:name>')
api.add_resource(ItemList , '/items')

app.run(port=5000 , debug=True) #debug=True helps you debug easier with HTML pages
