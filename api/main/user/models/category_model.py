from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Category:
    collection: Collection
    
     # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['name','image'],
        'properties': {
            'name': {
                'bsonType': 'string'
            },
            'image': {
                'bsonType': 'string'
            }
            # Define other properties here
        }
    }
    
    def __init__(self, name: str, image: str):
        self.name = name
        self.image = image
        self.created_at = datetime.datetime.utcnow()
        
  


# Set the collection reference
Category.collection = db['categories']
# Update validator for 'products' collection
db.command({
    'collMod': 'categories',
    'validator': {'$jsonSchema': Category.schema}
})