from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class User:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['fullName','email'],
        'properties': {
            'fullName': {
                'bsonType': 'string'
            },
            'email': {
                'bsonType': 'string'
            }
            # Define other properties here
        }
    }

    def __init__(self, user_id: str, fullName: str, email: str, password: str, phone: str, image: str, isAdmin: bool = False):
        self.user_id = user_id
        self.fullName = fullName
        self.email = email
        self.password = password
        self.phone = phone
        self.image = image
        self.isAdmin = isAdmin


# Set the collection reference
User.collection = db['users']  # Replace 'users' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'users',
    'validator': {'$jsonSchema': User.schema}
})





