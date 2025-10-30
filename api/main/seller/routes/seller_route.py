from flask import Blueprint
from flask import current_app as app
from flask import Flask, request, jsonify, render_template
from main.auth import token_required
from main.user.controllers.user_controller import *
from main.user.controllers.product_controller import create_product, get_products, delete_product, update_product
from main.user.controllers.category_controller import get_categories
from main.user.controllers.order_controller import get_user_orders, get_order_by_id
import os
from main.auth import token_required





seller_blueprint = Blueprint('sellers',  __name__, "api/sellers")

@seller_blueprint.route('/', methods=['GET'])
@token_required
def seller_home(current_user):
    return render_template('seller/index.html', user=current_user)

@seller_blueprint.route('/products', methods=['GET', 'POST'])
@token_required
def seller_products(current_user):
    products = get_products()[1]
    if request.method == 'POST':
        data = request.form
        delete_product(data['ID'])
        g_products = get_products()[1]
        return render_template('seller/products.html', products=g_products, user=current_user)
    if products != []:
        return render_template('seller/products.html', products=products, user=current_user)
    return render_template('seller/products.html', user=current_user)

@seller_blueprint.route('/add-product', methods=['GET', 'POST'])
@token_required
def seller_add_product(current_user):
    categories = get_categories()
    if request.method == 'POST':
        data = request.form
        files = request.files
        # create a product
        if create_product(data, files) == True:
            return render_template('seller/add-product.html', message="Product Created Successfully", user=current_user)
        return render_template('seller/add-product.html', messageError="Product Failed To Create", user=current_user)
    return render_template('seller/add-product.html', categories=categories, user=current_user)

@seller_blueprint.route('/product-review', methods=['GET'])
@token_required
def seller_product_review(current_user):
    return render_template('seller/product-review.html', user=current_user)

@seller_blueprint.route('/order-detail', methods=['GET'])
@token_required
def seller_order_detail(current_user):
    # making a get request
    order_id = request.args['orderID']
    details = get_order_by_id(order_id)
    customer = get_user(details['user'])
    return render_template('seller/order-detail.html', order_details=details, customer=customer, user=current_user)

@seller_blueprint.route('/order-list', methods=['GET'])
@token_required
def seller_order_list(current_user):
    user_id = ObjectId("671257b19a1b458f30f18ceb")
    orders_list = get_user_orders(user_id)
    if orders_list != []:
        return render_template('seller/order-list.html', orders=orders_list, user=current_user)
    return render_template('seller/order-list.html', user=current_user)

@seller_blueprint.route('/reports', methods=['GET'])
@token_required
def seller_report(current_user):
    return render_template('seller/reports.html', user=current_user)

@seller_blueprint.route('/add-refund', methods=['GET'])
@token_required
def seller_add_refund(current_user):
    return render_template('seller/return-add.html', user=current_user)

@seller_blueprint.route('/refunds', methods=['GET'])
@token_required
def seller_refunds(current_user):
    return render_template('seller/sale-return.html', user=current_user)

@seller_blueprint.route('/shipping', methods=['GET'])
@token_required
def shipping(current_user):
    return render_template('seller/shippingmethods.html', user=current_user)

@seller_blueprint.route('/stock', methods=['GET', 'POST'])
@token_required
def seller_stock(current_user):
    products = get_products()
    if request.method == 'POST':
        data = request.form
        update_product(data['stock_id'], data)
        update = get_products()
        return render_template('seller/stock-add.html', products=update, refresh='activate', user=current_user)
    if products != []:
        return render_template('seller/stock-add.html', products=products, user=current_user)
    return render_template('seller/stock-add.html', user=current_user)

@seller_blueprint.route('/settings', methods=['GET'])
@token_required
def seller_settings(current_user):
    return render_template('seller/website-setting.html', user=current_user)

@seller_blueprint.route('/tax', methods=['GET'])
@token_required
def seller_tax(current_user):
    return render_template('seller/tax.html', user=current_user)



   






