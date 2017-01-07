from db import db

class StoreModel(db.Model): #Extends db.Model

    __tablename__ = "stores"

    id = db.Column(db.Integer , primary_key = True )
    name = db.Column( db.String(80) )
    items = db.relationship('ItemModel' , lazy="dynamic") #This goes to 'ItemModel' and sees that
                                         #there is a many-to-one link from ItemModel
                                         #to StoreModel. This means that you can have
                                         #many items of 'ItemModel' that belong to a
                                         #single store of 'StoreModel' -- this is a
                                         #many-to-one link. SQLAlchemy sees that there
                                         #is store_id and determines the many-to-one
                                         #link because of that and returns a list which
                                         #is set to 'items'.

        #lazy=dynamic basically turns 'items' into a query builder. As seen below
        #we have self.items.all() which means to get all the items that match from the
        #items table. So rather than 'items' being built continuosly every time we
        #create a 'StoreModel', we will only build an 'items' list once we call
        #'json()' -- then it will go into the items table because self.items is a
        #query builder and then get all the items that match with 'id' (self.id which is
        #StoreModel.id). There is a tradeoff: Without lazy=dynamic, StoreModel creation ob
        #object is slow because it needs to load items, but then "json()" is fast because
        #all the items are already loaded. However, with lazy=dynamic, StoreModel creation is
        #pretty fast but then "json()" is slow because it needs to go into items table
        #and populate the 'items' variable.

    def __init__(self , name):
        self.name = name

    def json(self): #Returns JSON representation of 'ItemModel'
        return {'name' : self.name , 'items' : [ item.json() for item in self.items.all() ] }

    @classmethod
    def find_by_name( cls , name ):
        return cls.query.filter_by(name=name).first() #SELECT * FROM iterms WHERE name = name
        #No need to connect or have a cursor ... ItemModel.query belongs to db.Model, and
        #filter_by will filter a Model by name.
        #You can also continue to filter: filter_by(...).filter_by(...).
        #.first() does a LIMIT 1
        #The query is essentially a SQL command

    def save_to_db(self):
        db.session.add(self) #'session' belonds to db and it is a collection of objects we add to.
        db.session.commit() #Note: SQLAlchemy will do an 'update' it actually updates. (upserting)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
