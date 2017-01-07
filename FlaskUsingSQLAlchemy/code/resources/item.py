from flask_restful import Resource , reqparse
from flask_jwt import jwt_required , current_identity
from models.item import ItemModel

class Item(Resource): #'Item' will inherit from 'Resource'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every store needs a store ID."
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
        item = ItemModel( name , data['price'] , data['store_id'] )

        try:
            item.save_to_db()
        except: #If we fail upon insert^ return the error message below ... similar to try and catch
            return {"message": "An error occured during insertion." } , 500 #500 is internal server error

        return item.json() , 201


    def delete(self , name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "Item deleted"}

    #In REST, 'put' methods are idempotent -- No matter how many times called, it will never add anything extra to 'items'.
    def put(self , name):
        data = Item.parser.parse_args() #This will parse the arguments coming through the payload in the line above.

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name , data['price'] , data['store_id'] ) #Create a new item
        else:
            item.price = data['price'] #Item found, update price

        item.save_to_db() #Either way, found or not, we save to db

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items' : [ item.json() for item in ItemModel.query.all() ] }
        # ^For each ItemModel from query.all(), convert it to JSON.
