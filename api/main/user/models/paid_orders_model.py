from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
from bson import ObjectId

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]

class PaidOrder:
    collection: Collection
    
    schema = {
        'bsonType': 'object',
        'required': ['order_id','status'],
        'properties': {
            'order_id': {
                'bsonType': 'objectId'
            },
            'status': {
                'bsonType': 'bool',
            }
            # Define other properties here
        }
    }
    
    def __init__(self, order_id, status: bool):
        self.order_id = order_id
        self.status = status
        self.created_at = datetime.datetime.utcnow() # Assuming you want to add a timestamp



# Set the collection reference
PaidOrder.collection = db['paid_orders']
# Update validator for 'products' collection
db.command({
    'collMod': 'paid_orders',
    'validator': {'$jsonSchema': PaidOrder.schema}
})



