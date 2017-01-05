from flask_restful import Resource , reqparse
import sqlite3
from flask_jwt import jwt_required , current_identity


class Item(Resource): #'Item' will inherit from 'Resource'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required() #You put this as a decorator. The function below will only run once you have a token.
    def get(self , name):
        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {'message:' : 'Item not found'} , 404

    @classmethod
    def find_by_name(cls , name ):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query , (name,) )
        row = result.fetchone() #grabs result (from query)
        connection.close()

        if row:
            return {'item': {'name': row[0] , 'price': row[1] } }


    def post(self , name):
        if self.find_by_name(name):
            return {'message': 'An item with the name {} already exists'.format(name) }

        data = Item.parser.parse_args()
        item = {'name': name , 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (? , ?)"
        cursor.execute(query , (item['name'] , item['price'] ) )

        connection.commit()
        connection.close()

        return item , 201

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
