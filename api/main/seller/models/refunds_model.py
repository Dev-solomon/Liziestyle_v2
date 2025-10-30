from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]



class Refund:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['order_id','note','status'],
        'properties': {
            'order_id': {
                'bsonType': 'string'
            },
            'note': {
                'bsonType': 'string',
            },
            'status': {
                'bsonType': 'boolean'
            }, 
            # Define other properties here
        }
    }
    
    
    def __init__(self, order_id: str, note: str, status:bool):
        self.order_id = order_id
        self.note = note
        self.status = status
        self.createdAt = datetime.datetime.now()
        


# Set the collection reference
Refund.collection = db['refunds']
# Update validator for 'products' collection
db.command({
    'collMod': 'refunds',
    'validator': {'$jsonSchema': Refund.schema}
})
