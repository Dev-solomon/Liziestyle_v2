from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
from bson.objectid import ObjectId

# Assuming you have a MongoDB connection URI
# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]

# orderItems = [
#     {
#         'size': 'M',
#         'vid': '123456',
#         'name': 'Product 1',
#         'qty': 2,
#         'image': 'product1.jpg',
#         'price': 20.0,
#         'product_id': 'Product ID'
#     }
# ]

# payments = {
#     'paymentMethod': 'Credit Card',
#     'status': 'pending',
#     'paymentDate': None
# }

# delivery = {
#     'orderId': 'order_id_here',
#     'orderNum': 'ORD123456',
#     'status': 'awaiting',
#     'deliveryDate': None,  # Add date if available
#     'deliveryMethod': 'Courier'
# }

# shippingAddress = {
    # 'fullName': 'John Doe',
    # 'email': 'john.doe@example.com',
    # 'address': '123 Main St',
    # 'location': 'City, State',
    # 'phoneNumber': '123-456-7890',
    # 'shippingMethod': 'Standard',
    # 'shippingCost': 5.0   
# }


class Order:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['user','order_items','payments','total_price','sub_total_price','tax_price'],
        'properties': {
            'user': {
                'bsonType': 'objectId'
            },
            'order_items': {
                'bsonType': 'array'
            },
            'payments': {
                'bsonType': 'object',
            },
            'total_price': {
                'bsonType': 'double'
            },
            'sub_total_price': {
                'bsonType': 'double'
            },
            'tax_price': {
                'bsonType': 'double'
            }
            # Define other properties here
        }
    }

    def __init__(self, user_id, order_items: list, payments: dict, total_price: float, sub_total_price: float, tax_price: float, delivery: dict, shipping_address: dict = {}):
        self.user = user_id
        self.order_items = order_items
        self.payments = payments
        self.total_price = total_price
        self.sub_total_price = sub_total_price
        self.tax_price = tax_price 
        self.delivery = delivery
        self.shipping_address = shipping_address



# Set the collection reference
Order.collection = db['orders']  # Replace 'users' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'orders',
    'validator': {'$jsonSchema': Order.schema}
})





