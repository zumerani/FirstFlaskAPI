from db import db

class ItemModel(db.Model): #Extends db.Model

    __tablename__ = "items"

    id = db.Column(db.Integer , primary_key = True )
    name = db.Column( db.String(80) )
    price = db.Column( db.Float(precision=2) ) #precision is places after decimal point

    store_id = db.Column( db.Integer , db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') #This is a 'JOIN' between items and store tables
                                          #Now each 'ItemModel' has a property called 'store'
                                          #that is a 'StoreModel' type that matches the store_id^

    def __init__(self , name , price , store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self): #Returns JSON representation of 'ItemModel'
        return {'name' : self.name , 'price' : self.price }

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
