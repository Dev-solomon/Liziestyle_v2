from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]



class Review:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['user_id', 'product_id', 'title','message',],
        'properties': {
            'user_id': {
                'bsonType': 'objectId'
            },
            'product_id': {
                'bsonType': 'string'
            },
            'title': {
                'bsonType': 'string'
            },
            'message': {
                'bsonType': 'string',
            } 
            # Define other properties here
        }
    }
    
    
    def __init__(self, name:str, user_id, product_id: str, title: str, message: str, images:list, rating: int):
        self.name = name
        self.user_id = user_id
        self.product_id = product_id
        self.title = title
        self.message = message
        self.images = images
        self.rating = rating
        


# Set the collection reference
Review.collection = db['reviews']
# Update validator for 'products' collection
db.command({
    'collMod': 'reviews',
    'validator': {'$jsonSchema': Review.schema}
})
