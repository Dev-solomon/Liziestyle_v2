from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]



class Product:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['_id','title','images','price','description','category','tags','stock'],
        'properties': {
            '_id': {
                'bsonType': 'string'
            },
            'user': {
                'bsonType': 'objectId'
            },
            'title': {
                'bsonType': 'string'
            },
            'images': {
                'bsonType': 'array',
            },
            'price': {
                'bsonType': 'double'
            },
            'description': {
                'bsonType': 'string'
            },
            'category': {
                'bsonType': 'string'
            },
            'tags': {
                'bsonType': 'array'
            },
            'stock': {
                'bsonType': 'int'
            },
            # Define other properties here
        }
    }
    
    
    def __init__(self, _id: str, user_id, title: str, images: list, price: float, description: str, category: str, tags: list, salesOffer: str, stock: int, variants: list, weight: str, featured: str, units: int, video: str, productSku: str, product_id: str):
        self._id = _id
        self.user = user_id
        self.title = title
        self.images = images
        self.price = price
        self.description = description
        self.category = category
        self.tags = tags
        self.salesOffer = salesOffer
        self.stock = stock
        self.variants = variants
        self.weight = weight
        self.featured = featured
        self.units = units
        self.video = video
        self.productSku = productSku
        self.product_id = product_id
        self.createdAt = datetime.datetime.utcnow()
        


# Set the collection reference
Product.collection = db['products']
# Update validator for 'products' collection
db.command({
    'collMod': 'products',
    'validator': {'$jsonSchema': Product.schema}
})
