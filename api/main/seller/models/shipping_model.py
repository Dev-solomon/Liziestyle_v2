from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]



class Shipping:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['title','price','status'],
        'properties': {
            'title': {
                'bsonType': 'string'
            },
            'price': {
                'bsonType': 'double',
            },
            'status': {
                'bsonType': 'boolean'
            }, 
            # Define other properties here
        }
    }
    
    
    def __init__(self, title: str, price: float, status:bool):
        self.title = title
        self.price = price
        self.status = status
        self.createdAt = datetime.datetime.utcnow()
        


# Set the collection reference
Shipping.collection = db['shipping']
# Update validator for 'products' collection
db.command({
    'collMod': 'shipping',
    'validator': {'$jsonSchema': Shipping.schema}
})
