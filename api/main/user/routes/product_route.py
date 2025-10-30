from flask import Blueprint
from flask import current_app as app
from flask import Flask, request, jsonify, url_for, redirect, render_template
from main.auth import token_required
from main.user.controllers.product_controller import *

product_blueprint = Blueprint("product",  __name__,"api/products")

@product_blueprint.route('/', methods=['GET'])
def getProducts():
    return get_products()
    
@product_blueprint.route('/create', methods=['POST'])
@token_required
def create_products():
    if request.method == 'POST':
        data = request.form.to_dict()
        files = request.files
        return create_product(data, files)

@product_blueprint.route('/detail/<id>', methods=['GET'])
def product_by_id(id):
    if request.method == 'GET':
        return get_product_by_id(id)
    
@product_blueprint.route('/<id>', methods=['PUT', 'DELETE'])
@token_required
def product_update(id):
    if request.method == 'PUT':
        return update_product(id)
    elif request.method == 'DELETE':
        return delete_product(id)


@product_blueprint.route('/tags', methods=['GET'])
def popular_tags():
    return get_popular_tags()

@product_blueprint.route('/deleteproducts', methods=['DELETE'])
@token_required
def delete_products_route():
    return delete_products()

@product_blueprint.route('/import', methods=['GET'])
@token_required
def import_products():
    return import_products()


@product_blueprint.route('/writereview', methods=['POST'])
@token_required
def user_write_reviews(current_user):
    data = request.form.to_dict()
    data['user_id'] = current_user['_id']
    files = request.files
    if write_product_review(data, files) == True:
        return render_template('user/product.html', product_id=data['product_id'], message="Recensione inviata")
    return render_template('user/product.html', product_id=data['product_id'], messageError="Impossibile inviare la recensione")






