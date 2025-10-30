from pymongo import  DESCENDING
# from bson.objectid import ObjectId
from flask import jsonify, request
import requests
from main.user.models.product_model import Product
from main.user.models.reviews_model import Review
import datetime
import random
import os
import string
import json
from bson import ObjectId
from werkzeug.utils import secure_filename
from main.tools import upload_image
from datetime import datetime, timedelta



# Helper function to delete all products
def delete_products():
    try:
        Product.collection.delete_many({})
        return jsonify("All products deleted from database"), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Example route to create a new product
def create_product(data, files):
    try:
        # Generate a random string of the specified length
        # Define the length of the random string
        length = 24
        # Create a pool of characters (small alphabets and digits)
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        
        # get the images and put them in a list
        imageArray = []
        for file in files.getlist('images'):
            file_path = os.path.join('uploads/', secure_filename(file.filename))
            file.save(file_path)
            # upload file to cloudinary for storage there
            image_url = upload_image(file_path)
            imageArray.append(str(image_url))
            # Remove the file after successful upload
            os.remove(file_path)
            # print(f"Local file removed: {file_path}")
            
            
            
           
            
        featured = data.get('featured', 'off')
        
        tags = data['tagsArray']
        # Split the string and remove any leading/trailing whitespace
        tagsArray = [word.strip() for word in  tags.split(',')]
        
        variants_items = data['items']
        variants = json.loads(variants_items)
            
        
        json_data = {
            "_id": random_string,
            "user": ObjectId(data['user']),
            "title": data['name'],
            "images": imageArray,
            "price": float(data['price']),
            "description": data['description'],
            "category": data['category'],
            "tags": tagsArray,
            "salesOffer": data['discount'],
            "stock": int(data['stock']),
            "variants": variants,
            "weight": data['weight'],
            "featured": featured,
            "units": int(data['units']),
            "video": data['video'],
            "createdAt": datetime.datetime.now()
        }
        

        # Insert the new product into MongoDB
        result = Product.collection.insert_one(json_data)

        # Return the created product
        created_product = Product.collection.find_one({"_id": result.inserted_id})
        print(created_product)
        return True
    except Exception as e:
       print({"message": str(e)})



# Example route to get all products
def get_products(pageNum=1):
    try:
        pageSize = 25
        skip = (int(pageNum) - 1) * pageSize
        
        
        # Count the total number of matching products (for pagination calculation)
        total_count = Product.collection.count_documents({})

        # Calculate total pages
        total_pages = (total_count + pageSize - 1) // pageSize  # Equivalent to ceiling division
        
        
        shop_products = list(Product.collection.find({}).sort('createdAt', DESCENDING).limit(pageSize).skip(skip))
        
        
        return [shop_products, total_pages]
    except Exception as e:
        return print({"message-Products": str(e)})
    

# search for products with tag, and price range
def get_search_products(product_name, tag, min_price, max_price, pageNum):
    try:
        pageSize = 30
        skip = (int(pageNum) - 1) * pageSize
        
        
        # Base query to filter by price
        query_data = {
            "price": {"$gte": int(min_price), "$lte": int(max_price)}  # Price within range
        }
        
        # Add the tag filter only if tag is provided
        if tag:
            query_data["tags"] = tag  # Match products with the specified tag in the tags array
            
       # If product_name is provided, split it into words and check in tags and title
        if product_name:
            words = product_name.split()  # Split the product name into words
            
           # Process the title: split it into words (assuming spaces as word separators)
            # This is done after retrieving the products to check for word matches
            query_data["$or"] = [
                {"tags": {"$in": words}},
                {"category": {"$in": words}},  # Match any of the words in the tags array
            ]
            
            # Add a regex condition to check if any word in product_name matches a word in title
            query_data["$or"].append(
                {"title": {"$regex": "|".join(words), "$options": "i"}}  # Use regular expression for case-insensitive match
            )

            # Count the total number of matching products (for pagination calculation)
        total_count = Product.collection.count_documents(query_data)

        # Calculate total pages
        total_pages = (total_count + pageSize - 1) // pageSize   # Equivalent to ceiling division
        
        # Fetch products from the collection based on query and pagination
        searched_products = list(
            Product.collection.find(query_data)
            .limit(pageSize)
            .skip(skip)
        )
        
        
        
       
        
        return [searched_products, total_pages]

    except Exception as e:
        return print({"message": str(e)})
    
    
    
# search for products with tag, and price range
def get_all_products():
    try:
        # Calculate the date 1 month ago
        one_month_ago = datetime.utcnow() - timedelta(days=30)

        pipeline = [
            # First pipeline: Get 8 random products from 'famiglia'
            {"$match": {"category": "famiglia"}},
            {"$sample": {"size": 8}},

            # Union with 8 random products from 'donne'
            {"$unionWith": {
                "coll": "products",
                "pipeline": [
                    {"$match": {"category": "donne"}},
                    {"$sample": {"size": 8}}
                ]
            }},
            
            
             # Union with 8 random not older than 1 month from current date
            {"$unionWith": {
                "coll": "products",
                "pipeline": [
                    {"$match": {"created_at": {"$gte": one_month_ago} }},
                    {"$sample": {"size": 16}}
                ]
            }},
            

            # Union with 8 random products NOT in 'famiglia' and 'donne'
            {"$unionWith": {
                "coll": "products",
                "pipeline": [
                    {"$match": {
                        "category": { "$nin": ["famiglia", "donne"]}
                    }},
                    {"$sample": {"size": 8}}
                ]
            }}
            
        ]

        products_list = list(Product.collection.aggregate(pipeline))
        
       
        
        return products_list

    except Exception as e:
        return print({"message": str(e)})
    
#  Get a single product by their id
def get_product_by_id(id: str) -> dict:
    try:
        # Fetch product by ID
        product = Product.collection.find_one({'_id': id})
        
        if not product:
            raise ValueError("Product not found")
        
        return product
    except Exception as e:
        raise RuntimeError(f"Error fetching product: {str(e)}")
    
    
def get_related_products(id: str) -> dict:
    try:
        # Fetch product by ID
        product = Product.collection.find_one({'_id': id})
        
        if not product:
            raise ValueError("related Products not found")
        
        # Fetch related products
        related_products = list(Product.collection.find({
            'category': product['category'],
            '_id': {'$ne': id}
        }).limit(20))
        
        
        return related_products
    except Exception as e:
        raise RuntimeError(f"Error fetching product: {str(e)}")
    
def get_other_products(id: str) -> dict:
    try:
        # Fetch product by ID
        product = Product.collection.find_one({'_id': id})
        
        if not product:
            raise ValueError("other Products not foundb")
        
        # Fetch other products
        other_products = list(Product.collection.find({
            'category': {'$ne': product['category']},
            '_id': {'$ne': id}
        }).limit(20))
        
        return other_products
    except Exception as e:
        raise RuntimeError(f"Error fetching product: {str(e)}")


# Example route to update a product by ID
def update_product(id, data):
    try:
        # Fetch product by ID
        product = Product.collection.find_one({'_id': id})
        
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        data_json = {
            "_id": data['stock_id'] ,
            "stock": int(data['stockQuantity']),
            "variants": json.loads(data['stock_variants'])
        }

        # Update the product in MongoDB
        Product.collection.update_one({'_id': id}, {'$set': data_json})

        # Return updated product
        updated_products = Product.collection.find_one({'_id': id})
        return updated_products

    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    
# Get popular tags
def get_popular_tags():
    try:
        pipeline = [
            { '$unwind': '$tags' },
            { '$group': { '_id': '$tags', 'count': { '$sum': 1 } } },
            { '$sort': { 'count': -1 } },
            { '$limit': 5 }
        ]
        
        # Process results into a clean format
        tags = [
            {'tag': tag['_id'], 'count': tag['count']}
            for tag in Product.collection.aggregate(pipeline)
        ]
        
        return tags
    
    except Exception as e:
        # Return error as a JSON response (Flask-specific)
        return jsonify({'message': str(e)}), 400
    
    
# Get sizes filter
def get_popular_variants():
    try:
        pipeline = [
            { '$unwind': '$variants' },
            { '$group': { '_id': '$variants', 'count': { '$sum': 1 } } },
            { '$sort': { 'count': -1 } },
            # { '$limit': 5 }
        ]
        
        # Process results into a clean format
        variants = [
            {'variant': variant['_id'], 'count': variant['count']}
            for variant in Product.collection.aggregate(pipeline)
        ]
        
        return variants
    
    except Exception as e:
        # Return error as a JSON response (Flask-specific)
        return jsonify({'message': str(e)}), 400

# Delete product  
def delete_product(product_id):
    try:
        product = Product.collection.delete_one({'_id': product_id})
        return jsonify({'message': 'Product Deleted Successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
    
def write_product_review(data, files):
    try:
        
        # get the images and put them in a list
        imageArray = []
        invalid_files = all(file.filename == '' or len(file.read()) == 0 for file in files.getlist('images'))
        
        if invalid_files == True:
            imageArray = []
        else:
            for file in files.getlist('images'):
                file_path = os.path.join('uploads', secure_filename(file.filename))
                file.save(file_path)
                # upload file to cloudinary for storage there
                image_url = upload_image(file_path)
                imageArray.append(str(image_url))
                # Remove the file after successful upload
                os.remove(file_path)
                # print(f"Local file removed: {file_path}")
            # print(imageArray)
            
            
        
        json_data = {
            "name": data['name'],
            "user_id": ObjectId(data['user_id']),
            "product_id": data['product_id'],
            "title": data['title'],
            "message": data['message'],
            "images": imageArray,
            "rating": data['rating'],
            "createdAt": datetime.datetime.utcnow()
        }
        

        # Insert the new product into MongoDB
        result = Review.collection.insert_one(json_data)

        # Return the created Review
        created_review = Review.collection.find_one({"_id": result.inserted_id})
        # print(created_review)
        return True
    except Exception as e:
       print({"message": str(e)})
       
       
def get_user_reviews(product_id, pageNum=1):
    try:
        pageSize = 4
        skip = (int(pageNum) - 1) * pageSize
        
        
        # Count the total number of matching products (for pagination calculation)
        total_count = Review.collection.count_documents({"product_id": product_id})

        # Calculate total pages
        total_pages = (total_count + pageSize - 1) // pageSize  # Equivalent to ceiling division
        
        
        reviews = list(Review.collection.find({"product_id": product_id}).sort('createdAt', DESCENDING).limit(pageSize).skip(skip))
        
        return [reviews, [total_count, total_pages]]
    except Exception as e:
        return print({"message-Products": str(e)})
    
    
def get_all_reviews():
    try:
    
        all_reviews = list(Review.collection.find({}).sort('createdAt', DESCENDING))
        
        return all_reviews
    except Exception as e:
        return print({"message-Products": str(e)})
    
    
# def get_userReviews_related_and_other_products(related_product_id, other_product_id) -> list:
#     try:
#         # Count the total number of matching products (for pagination calculation)
#         # total_count_related = Review.collection.count_documents({"product_id": related_product_id})
#         # total_count_others = Review.collection.count_documents({"product_id": other_product_id})

#         print(related_product_id, other_product_id)
        
#         reviews_relatedProducts = list(Review.collection.find({"product_id": related_product_id}).sort('createdAt', DESCENDING))
#         reviews_otherProducts = list(Review.collection.find({"product_id": other_product_id}).sort('createdAt', DESCENDING))
        
#         return [reviews_relatedProducts, reviews_otherProducts]
#     except Exception as e:
#         return print({"message-Products": str(e)})
    




