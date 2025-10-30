from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]



class Blog:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['category','title','content'],
        'properties': {
            'category': {
                'bsonType': 'string'
            },
            'title': {
                'bsonType': 'string'
            },
            'content': {
                'bsonType': 'string',
            },
            # Define other properties here
        }
    }
    
    
    def __init__(self, keywords:str, category: str, title: str, content: str, image: str):     
        self.title= title
        self.category = category
        self.image = image
        self.keywords = keywords
        self.content= content
        self.createdAt = datetime.datetime.utcnow()
        


# Set the collection reference
Blog.collection = db['blogs']
# Update validator for 'blogs' collection
db.command({
    'collMod': 'blogs',
    'validator': {'$jsonSchema': Blog.schema}
})
