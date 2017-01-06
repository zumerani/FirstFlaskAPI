from flask_restful import Resource , reqparse
import sqlite3
from flask_jwt import jwt_required , current_identity
from models.item import ItemModel

class Item(Resource): #'Item' will inherit from 'Resource'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required() #You put this as a decorator. The function below will only run once you have a token.
    def get(self , name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #We need to do this since find_by_name does not return a JSON object
        else:
            return {'message:' : 'Item not found'} , 404

    def post(self , name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with the name {} already exists'.format(name) }

        data = Item.parser.parse_args()
        item = ItemModel( name , data['price'] )

        try:
            item.insert()
        except: #If we fail upon insert^ return the error message below ... similar to try and catch
            return {"message": "An error occured during insertion." } , 500 #500 is internal server error

        return item.json() , 201


    def delete(self , name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query , (name,) )

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    #In REST, 'put' methods are idempotent -- No matter how many times called, it will never add anything extra to 'items'.
    def put(self , name):
        data = Item.parser.parse_args() #This will parse the arguments coming through the payload in the line above.

        item = ItemModel.find_by_name(name)
        updatedItem = ItemModel( name , data['price'] )

        if item is None:
            try:
                updatedItem.insert()
            except:
                return {"message": "An error occurred inserting the item" } , 500
        else:
            try:
                updatedItem.update()
            except:
                return {"message" : "An error occurred updating the item." } , 500

        return updatedItem.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute( query )
        items = []
        for row in result:
            items.append( {'name' : row[0] , 'price' : row[1] } )

        connection.close()

        return {'items' : items } #To make it JSON format
