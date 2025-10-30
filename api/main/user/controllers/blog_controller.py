from pymongo import  DESCENDING
# from bson.objectid import ObjectId
from flask import jsonify, request
import requests
from main.user.models.blog_model import Blog
import datetime
import os
import string
import json
from bson import ObjectId




# Example route to create a new blog post
def create_blog_post(data):
    try:
            
        
        json_data = {
            "title": data['title'],
            "category": data['category'],
            "image": data['image_link'],
            "keywords": data['keywords'],
            "content": data['content'],
            "createdAt": datetime.datetime.now(),
        }
        # print(json_data)

        # Insert the new blog post into MongoDB
        result = Blog.collection.insert_one(json_data)

        # Return the created blog post
        created_blog_post = Blog.collection.find_one({"_id": result.inserted_id})
        # print(created_blog_post)
        return True
    except Exception as e:
       print({"message": str(e)})



def get_blogs(pageNum, category):
    try:
        pageSize = 9
        skip = (int(pageNum) - 1) * pageSize
        
        pipeline_1 = [
            # Get all blogs with random order
            {"$match": {}},
            {"$sample": {"size": pageSize }},
        ]
        
        # Use the existing pipeline_2 from your current document
        pipeline_2 = [
            # Get all blogs, filter by category unless "all" is specified
            {"$match": {"category": category} if category != "all" else {} },
            # Sort by date in descending order
            {"$sort": {"createdAt": DESCENDING }},
            # Skip documents
            {"$skip": skip},
            # Limit documents
            {"$limit": pageSize}
        ]
        
        # Count the total number of matching blogs (for pagination calculation)
        total_count = Blog.collection.count_documents(
            {"category": category} if category != "all" else {}
        )

        # Calculate total pages
        total_pages = (total_count + pageSize - 1) // pageSize  # Ceiling division
        
        # Fetch blogs based on the pipeline
        if category == "all" and pageNum == 1:
            blogs = list(Blog.collection.aggregate(pipeline_1))
        else:
            blogs = list(Blog.collection.aggregate(pipeline_2))
        
        return [blogs, total_pages]
    except Exception as e:
        return {"message-blogs": str(e)}

    
    
#  Get a single product by their id
def get_blog_by_id(id: str) -> dict:
    try:
        # Fetch blog by ID
        blog = Blog.collection.find_one({'_id': ObjectId(id)})
        
        if not blog:
            raise ValueError("blog not found")
        
        return blog
    except Exception as e:
        raise RuntimeError(f"Error fetching Blog: {str(e)}")
    
    
def get_related_blog_categories(id: str) -> dict:
    try:
        # Fetch blog by ID
        blog = Blog.collection.find_one({'_id': ObjectId(id)})
        
        if not blog:
            raise ValueError("related blogs post not found")
        
        # Fetch related blogs
        related_blogs = list(Blog.collection.find({
            'category': blog['category'],
            '_id': {'$ne': ObjectId(id)}
        }).limit(3))
        
        
        return related_blogs
    except Exception as e:
        raise RuntimeError(f"Error fetching product: {str(e)}")
    
def get_other_blog_categories(id: str) -> dict:
    try:
        # Fetch blog by ID
        blog = Blog.collection.find_one({'_id': ObjectId(id)})
        
        if not blog:
            raise ValueError("other Blogs Post not found")
        
        # Fetch other products
        other_blogs = list(Blog.collection.find({
            'category': {'$ne': blog['category']},
            '_id': {'$ne': ObjectId(id)}
        }).limit(3))
        
        return other_blogs
    except Exception as e:
        raise RuntimeError(f"Error fetching product: {str(e)}")



    
    
# Get blog tags
def get_blog_tags():
    try:
        pipeline = [
            { '$group': { '_id': '$category', 'count': { '$sum': 1 } } },
            { '$sort': { 'count': -1 } },
            { '$limit': 5 }
        ]
        
        # Process results into a clean format
        tags = [
            {'category': category['_id'], 'count': category['count']}
            for category in Blog.collection.aggregate(pipeline)
        ]
        
        return tags
    
    except Exception as e:
        # Return error as a JSON response (Flask-specific)
        return jsonify({'message': str(e)}), 400
    
    


# Delete blog post 
def delete_blog_post(post_id):
    try:
        blog = Blog.collection.delete_one({'_id': ObjectId(post_id)})
        return jsonify({'message': 'Post Deleted Successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
    