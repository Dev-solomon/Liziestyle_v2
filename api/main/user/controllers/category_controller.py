from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from main.user.models.category_model import Category
from main.user.controllers.data import categories
import datetime

# @desc Import categories
# @route POST /api/categories/import
# @access Private
def import_categories():
    try:
        # Remove all existing categories
        Category.collection.delete_many({})
        
        # Insert new categories
        created_categories = Category.collection.insert_many(categories)
        
        return jsonify([str(cat_id) for cat_id in created_categories.inserted_ids]), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# @desc Create a new category
# @route POST /api/categories
# @access Private
def create_category():
    try:
        data = request.json
        data['createdAt'] = datetime.datetime.utcnow()
        
        # Check if category already exists
        exists_cat = Category.collection.find_one({'name': data['name']})
        if exists_cat:
            return jsonify({'message': 'Category already exists'}), 400
        
        # Insert new category
        created_category = Category.collection.insert_one(data)
        
        return jsonify({"category created successful": str(created_category.inserted_id)}), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# @desc Get all categories
# @route GET /api/categories
# @access Public
def get_categories():
    try:
        categories = list(Category.collection.find({}))
        return categories
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# @desc Update a category
# @route PUT /api/categories/<id>
# @access Private
def update_category(id):
    try:
        data = request.json
        
        # Find category by id
        category = Category.collection.find_one({'_id': ObjectId(id)})
        if not category:
            return jsonify({'message': 'Category not found'}), 404
        
        # Update category fields
        new_values = {'$set': data}
        Category.collection.update_one({'_id': ObjectId(id)}, new_values)
        
        updated_category = Category.collection.find_one({'_id': ObjectId(id)})
        
        return jsonify(str(updated_category))
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# @desc Delete a category
# @route DELETE /api/categories/<id>
# @access Private
def delete_category(id):
    try:
        # Find category by id and delete
        result = Category.collection.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 1:
            return jsonify({'message': 'Category Successfully removed'})
        else:
            return jsonify({'message': 'Category not found'}), 404
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


