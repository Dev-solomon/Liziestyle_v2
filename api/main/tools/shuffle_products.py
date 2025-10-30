from pymongo import MongoClient, errors
from pymongo.collection import Collection
from datetime import datetime
from termcolor import colored
from bson import ObjectId
import random

# Assuming you have a MongoDB connection URI
client = MongoClient("mongodb+srv://SolomonNtia:%40Jedidiah7@cluster0.6ocpeqp.mongodb.net/")
db = client["liziestyle"]


source_collection = db['enter source']  # Replace with your source collection
target_collection = db['enter target']  # Replace with your target collection

# Fetch all documents from the source collection
documents = list(source_collection.find())

# Shuffle the documents
random.shuffle(documents)
random.shuffle(documents)
random.shuffle(documents)

# Insert shuffled documents into the target collection
if documents:
    target_collection.insert_many(documents)

print(colored("Documents Shuffled and Inserted Successfully.", "green"))
