from flask import current_app as app, jsonify, request, make_response, redirect, url_for, render_template
from pymongo import MongoClient, DESCENDING
from bson import ObjectId, json_util
import datetime
import json
from main.user.models.order_model import Order
from main.user.models.paid_orders_model import PaidOrder
from main.user.models.product_model import Product
from main.stripe.stripe import *
from termcolor import colored
from main.middleware.mailer import send_email
import logging
import requests, ast


app.logger.setLevel(logging.DEBUG)

# Asynchronous utility for handling in loops
# def async_map(func, iterable):
#     return asyncio.gather(*(func(item) for item in iterable))

# Create order function
def create_order():
    try:
        data = request.form.to_dict()
        # convert str data of orderitems to list of dictionaries
        orderItems = ast.literal_eval(data['orderItems'])
        # print(orderItems)
        
        create_new_order = {
                        "user": ObjectId(data['user']),
                        "order_items": orderItems,
                        "payments": json.loads(data['payments']),
                        "total_price": float(data['total_price']),
                        "sub_total_price": float(data['sub_total_price']),
                        "tax_price": float(data['tax_price']),
                        "shipping_address": json.loads(data['shipping_address']), 
                        "createdAt" : datetime.datetime.now().isoformat(),
                    }
        result =  Order.collection.insert_one(create_new_order).inserted_id
        # print(result)
        print(f"New Order by User: {data['user']} at Time: {datetime.datetime.now().isoformat()}")
        return result
    except Exception as e: 
        print({'messagehere': str(e)})
        return False

# Update order to paid function
def update_order_to_paid(customer_order_id, payment_data):
    try: 
        # Convert customer_order to ObjectId
        order = Order.collection.find_one({'_id': ObjectId(customer_order_id)})
        
        if order:
            order_status = {
                'completed': 'completato',
                'canceled': 'annullata'
            }
            
            # Check for payment status and update accordingly
            payment_status = order_status['completed'] if payment_data.get('status') == "complete" else order_status['canceled']
            
            Order.collection.update_one(
                {'_id': ObjectId(customer_order_id)}, 
                {'$set':  {
                    "payments": {
                        "status": payment_status,
                        "method": "stripe",  # Fixed typo from 'methd' to 'method'
                        "payment_date": datetime.datetime.now()
                    },
                    "total_price": payment_data.get('amount_total', 0) / 100,  # Handle missing data
                    "sub_total_price": payment_data.get('amount_subtotal', 0) / 100,
                    "shipping_address": {
                        'fullName': payment_data['customer_details'].get('name'),
                        'email': payment_data['customer_details'].get('email'),
                        'address': f"Line1: {payment_data['shipping_details']['address'].get('line1')}, "
                                   f"Line2: {payment_data['shipping_details']['address'].get('line2')}, "
                                   f"Postal Code: {payment_data['shipping_details']['address'].get('postal_code')}, "
                                   f"State: {payment_data['shipping_details']['address'].get('state')}",
                        'location': f"{payment_data['shipping_details']['address'].get('city')}, "
                                    f"{payment_data['shipping_details']['address'].get('country')}",
                        'phoneNumber': payment_data['customer_details'].get('phone'),
                        'shippingMethod': "CJPacket Ordinary",
                        'shipping_cost': order['shipping_address'].get('shipping_cost', 0)  # Handle missing cost
                    }
                }})
            
            PaidOrder.collection.insert_one({"order_id": ObjectId(customer_order_id), "status": False})
            
            app.logger.info(colored(" ---- A Paid Order Has been Updated ---- ", "yellow"))
            
            
            
            email_order_to_customer = {
            "status": True,
            "orderUrl": f"{os.getenv('CLIENT_URL')}/checkout?order_id={customer_order_id}",
            "products": order.get('order_items', []),
            "subTotal": payment_data.get('amount_subtotal', 0) / 100,
            "shippingCost": order.get('shipping_address', {}).get('shipping_cost', 0),
            "totalPrice": payment_data.get('amount_total', 0) / 100,
            "taxPrice": 3.0,
            "siteName": 'Liziestyle',
            "url": os.getenv('CLIENT_URL', '')
         }

        # Send email
            customer_email = payment_data['customer_details'].get('email')
            customer_name = payment_data['customer_details'].get('name')

            new_email = send_email(
                    customer_email,
                    f"Nuovo ordine di {customer_name}",
                    "Grazie per aver acquistato con liziestyle. \n Il tuo ordine è stato ricevuto ed è in fase di elaborazione sulla piattaforma. In allegato di seguito è riportato il riepilogo del tuo ordine.",
                    email_order_to_customer
            )
            new_email_to_admin = send_email(
                    "support@liziestyle.com",
                    f"New Order Made By {customer_name}",
                    "A customer just made a new order - View attached below to see the summary.",
                    email_order_to_customer
            )

            if new_email == 200:
                app.logger.info("Email-Order sent To Customer ...")
            else:
                app.logger.warning("Failed to send email to customer")
                
            if new_email_to_admin == 200:
                app.logger.info("Email-Order sent To Admin ...")
            else:
                app.logger.warning("Failed to send email to admin")
                
            
            return True
            
    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error for debugging
        return jsonify({'message': str(e)}), 400


# Function to delete an order
def delete_order(order_id):
    try: 
        result = Order.collection.delete_one({'_id': ObjectId(order_id)})
        if result.deleted_count == 1:
            return redirect(url_for('user_dashboard', message="Ordine eliminato!"))
        else:
            return redirect(url_for('user_dashboard', message="Impossibile eliminare l'ordine!"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Function to get user orders
from bson.objectid import ObjectId
from flask import jsonify
 
def get_user_orders(user_id):
    try:
        orders_cursor = Order.collection.find({'user': ObjectId(user_id)}).sort('createdAt', DESCENDING)
        
        orders_list = list(orders_cursor)  # Retrieve all orders from the cursor
        
        total_orders = len(orders_list)  # Calculate total number of orders
        
        orders_cursor.close()  # Close the cursor
        
        # Format the response as JSON
        # return jsonify({
        #     'orders': json_util.dumps(orders_list),
        #     'total_orders': total_orders
        # })
        return orders_list
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Function to get order by ID
def get_order_by_id(order_id):
    try:
        order = Order.collection.find_one({'_id': ObjectId(order_id)})
        # return jsonify(str(order)), 201
        return order
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Delete all orders
def delete_all_orders(user_id):
    try:
        # Convert user_id to ObjectId if needed
        user_id = ObjectId(user_id)

        # Delete orders where user matches
        result = Order.collection.delete_many({"user": user_id})

        # Check deletion result
        if result.deleted_count > 0:
            return { "message": "Orders Deleted!" }
        else:
            return { "message": "No orders found for this user" }
    
    except Exception as e:
        return { "error": str(e) }
    


def get_cart():
    # Get the cart from cookies
    cart = request.cookies.get('cart')
    
    if cart:
        # Deserialize the cart JSON string back to a dictionary
        cart = json.loads(cart)
        
        
    else:   
        cart = []
    
    return cart



def delete_cart_cookie(order_id):
    """
    Deletes the 'cart' cookie from the browser.
    """
    response = make_response(redirect(url_for('checkout', order_id=order_id, message="Il tuo ordine è stato effettuato!")))  # Create a response object
    response.delete_cookie('cart')  # Specify the cookie name and path
    return response


def track_order(tracking_num):
    try:
       
       
        url = f'https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo?trackNumber={tracking_num}' # query url
       
        headers = {
            # access token of account
            'CJ-Access-Token': "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNzA4NiIsInR5cGUiOiJBQ0NFU1NfVE9LRU4iLCJzdWIiOiJicUxvYnFRMGxtTm55UXB4UFdMWnlyK2FrM2QxTU9HTURrWlU4RHF2bU5vWGtFZWlyenRIc29Na3pkamVSQUwzN1pQUEJ6Y1RYWFhEZzNyOHdqYWxvMDBhSjhTQlZlSWJ0TDNIVFc5U1JQQnU4VTU4Tkw4dXRCaEZSd25iM1pqRmJLM2l5QkxaamoxeGg1Zkh1MmNNbDdKdEwxMkVjYkNRdnM3cnJsWWhueDIxdWMvMUpPV2pPK0V3ZHk5Tm1QRGF3M0VWMHJ6ZUJhVnpNY2lTWnYySTE0L2JOd2lnMTFXVi9DaVdGVllkWUQ3Q0lXZi8xQjVDRVI2UGh2MnZ6UDR5R3lpRjFXS28yZWpNOUpCRVBEODZsa1ZvaTN6OC91M3M1Y1pjOXZjY0MxMD0ifQ.YiLZw9VginUjuiA6zTmNORsj8ZKwYhGlPdjglVsR0J4",  # Replace `token()` with your token function
        }
       
        response = requests.get(url, headers=headers)
      # Raise an error for non-200 HTTP responses
        response.raise_for_status()
        
        result = response.json()
        
        # Validate the API response structure and contents
        if result.get("code") == 200 and result.get("message") == "Success":
            track_results = result.get("data", [])
            return track_results
        
        # Handle unexpected API response format or failure
        return []
    
    except Exception as e:
        return jsonify({'message-tracking_order': str(e)}), 400