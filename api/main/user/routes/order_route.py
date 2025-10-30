from flask import Blueprint
from flask import current_app as app
from flask import Flask, request, jsonify, redirect, url_for, make_response
from main.auth import token_required
from main.user.controllers.order_controller import *
from main.user.models.product_model import Product
from main.stripe.stripe import *
import json
from datetime import timedelta
from termcolor import colored
import requests

order_blueprint = Blueprint("order",  __name__, "api/orders")

@order_blueprint.route('allorders/<userId>', methods=['GET'])
@token_required
def get_singleUser_orders(userId):
    if request.method == 'GET':
        return get_user_orders(userId)
    
@order_blueprint.route('/create', methods=['POST'])
@token_required
def create_new_orders(current_user):
    if request.method == 'POST':
        new_order = create_order()
        if new_order != False:
            return delete_cart_cookie(new_order)
        return render_template('user/index.html', messageError="Inserimento dell'ordine non riuscito!")
    return  None

# @order_blueprint.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
# @token_required
# def getorder_id(id):
#     if request.method == 'GET':
#         return get_order_by_id(id)
#     elif request.method == 'PUT':
#         data = request.json
#         return update_order_to_paid(id, data)
#     elif request.method == 'DELETE':
#         return delete_order(id)


@order_blueprint.route('/<id>', methods=['POST', 'GET'])
@token_required
def delete_single_order(current_user, id):
    return delete_order(id)



@order_blueprint.route('/deleteOrders/<userId>', methods=['DELETE'])
@token_required
def clear_orders_all(userId):
    return delete_all_orders(userId)


@order_blueprint.route('/<orderID>/checkout', methods=['POST'])
@token_required
def check_out_stripe(current_user, orderID):
    response_content = checkout(orderID).get_data().decode('utf-8')
    # print(json.loads(response_content)['url'])
    checkout_url = json.loads(response_content)['url']
    return redirect(checkout_url)

@order_blueprint.route('/webhook', methods=['POST','GET'])
def check_out_stripe_webhook():
    return webhook()



@order_blueprint.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        # Get the cart list from cookies (if it exists)
        cart = request.cookies.get('cart')
        
        if cart:
            # Deserialize the cart JSON string back to a list
            cart = json.loads(cart)
        else:
            # If no cart in cookies, initialize an empty cart list
            cart = []
            
        
        # data from the request (you customize based on your cart's structure)
        data= request.form.to_dict()
        product_variant = data['variant']
        product_id = data['product_id']
        
        # Fetch product from Database
        product = Product.collection.find_one({'_id': product_id})
        
        # Add or update the cart item (check if item exists)
        item_found = False
        for item in cart:
            if item['variant'] == product_variant and item['product_id'] == product_id:
                item_found = True
                break
            
        if product_variant == "":
            return render_template('user/product.html', product_id=product['_id'], messageError="Scegli 1 variante!")
        
        if product.get('salesOffer'):
            new_price = float(product['price']) - (float(product['price']) * float(product['salesOffer']) / 100)
        else:
            new_price = float(product['price'])

        
        if item_found == False:
            # If the item is not already in the cart, add a new entry
            cart.append({
                "variant": data['variant'],
                "title": product['title'],
                "qty": int(data['qty']),
                "images": product['images'],
                "price": round(new_price, 1),
                "product_id": product['_id']
            })
        
            # Serialize the cart list to JSON
            cart_json = json.dumps(cart)
            
            
        
            # Create a response and set the cart in the cookie
            response  = make_response(redirect(url_for('product_detail', product_id=product['_id'], message="Articolo aggiunto al carrello")))
            response.set_cookie('cart', cart_json, max_age=int(timedelta(days=30).total_seconds()))  # Store the cart as a cookie
            
            return response
        
        return render_template('user/product.html', product_id=product['_id'], messageError="Articolo già nel carrello!")
    except Exception as e:
        return jsonify({'message_add_to_cart': str(e)}), 400

@order_blueprint.route('/view_cart')
@token_required
def view_cart(current_user):
    # Get the cart from cookies
    cart = request.cookies.get('cart')
     
    if cart:
        # Deserialize the cart JSON string back to a dictionary
        cart = json.loads(cart)
    else:
        cart = []
    
    return f'Your cart: {cart}'

@order_blueprint.route('/delete_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        # Get the cart from the cookies
        cart = request.cookies.get('cart')
        
        if cart:
            # Deserialize the cart from JSON string to Python list
            cart = json.loads(cart)
        else:
            # If the cart is not in the cookies, initialize an empty list
            cart = []
        
        # Get the item_id to remove from the form data (sent via POST)
        data= request.form.to_dict()
        item_variant = data['variant']
        item_id = data['product_id']# Assuming item_id is passed as form data
        
        
        
        # Remove the item from the cart list
        cart = [item for item in cart if not (item['variant'] == item_variant and item['product_id'] == item_id)]
        
        # Serialize the updated cart back to a JSON string
        cart_json = json.dumps(cart)
        
        # Create a response and set the updated cart in the cookie
        response =  make_response(redirect(url_for('product_detail', product_id=item_id, message="Articolo rimosso dal carrello carrello")))
        response.set_cookie('cart', cart_json, max_age=int(timedelta(days=30).total_seconds()))  # Store the updated cart in the cookie
        
        return response
    
    except Exception as e:
        return jsonify({'message-delete_from_cart': str(e)}), 400
    
    
    





    




