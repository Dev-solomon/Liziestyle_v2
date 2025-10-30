from flask import Blueprint
from flask import current_app as app
from flask import Flask, request, jsonify
from main.auth import token_required
from main.user.controllers.category_controller import *

category_blueprint = Blueprint("cat",  __name__, "api/categories")

@category_blueprint.route('/', methods=['GET'])
def all_categories():
    if request.method == 'GET':
        return get_categories()
    
@category_blueprint.route('/create', methods=['POST'])
@token_required
def create_categories(current_user):
    if request.method == 'POST':
        return create_category() 

@category_blueprint.route('/<id>', methods=['PUT', 'DELETE'])
@token_required
def category_by_id(current_user,id):
    if request.method == 'PUT':
        return update_category(id)
    elif request.method == 'DELETE':
        return delete_category(id)

@category_blueprint.route('/import', methods=['GET'])
@token_required
def import_categories_route(current_user):
    return import_categories()


