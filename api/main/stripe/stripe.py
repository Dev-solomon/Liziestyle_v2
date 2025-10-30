import os
from flask import Flask, request, jsonify
from bson import ObjectId
import stripe
from dotenv import load_dotenv
import stripe.error
from main.user.models.order_model import Order
from main.user.models.user_model import User
from main.user.controllers import order_controller

# Load environment variables
load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')  # Set this if you have a webhook secret

pay_currency = 'eur'

def cart(order_items):
    cart_items = []
    for item in order_items:
        cart_items.append({
            'price_data': {
                'currency': pay_currency,
                'product_data': {
                    'name': item['title'],
                    'images': [item['images'][0]],
                    'description': f"Variante: taglia e colore: {item['variant']}",
                    'metadata': {
                        'id': item['product_id'],
                    },
                },
                'unit_amount': round(item['price'] * 100),
            },
            'quantity': item['qty'],
        })
    return cart_items


def checkout(order_id):

    order = Order.collection.find_one({'_id': ObjectId(order_id)})
    
    
    order_items = order["order_items"]
    orderId = order["_id"]
    userId = order["user"]
    shipping_amount = order["shipping_address"]["shipping_cost"] + order['tax_price']
    
    user = User.collection.find_one(userId)
    email = user["email"]
    name = user['fullName']
    
   

    customer = stripe.Customer.create(
        metadata={
            'name': str(name),
            'userId': str(userId),
            'orderId': str(orderId),
            'email': email,
        }
    )

    try:
        session = stripe.checkout.Session.create(
            shipping_address_collection={
                'allowed_countries': ['IT', 'US'],
            },
            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': round(shipping_amount *100),
                            'currency': pay_currency,
                        },
                        'display_name': 'Spedizione + Tasse',
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 7,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 12,
                            },
                        },
                    },
                },
            ],
            line_items=cart(order_items),
            phone_number_collection={
                'enabled': True,
            },
            mode='payment',
            success_url=f"{os.getenv('CLIENT_URL')}/paymentSuccess",
            cancel_url=f"{os.getenv('CLIENT_URL')}/paymentFailed",
            customer=customer.id,
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

 
def webhook():
    sig = request.headers["stripe-signature"]
    payload = request.get_data(as_text=True)

    endpoint_secret = os.getenv('STRIPE_SIGNING_SECRET') #live endpoint signing_secret
    
    try:
        if endpoint_secret: # type: ignore
            event = stripe.Webhook.construct_event(payload, sig, endpoint_secret) # type: ignore
        else:
            event = request.json
            
           

        event_type = event['type']
        data = event['data']['object']
        
        if event_type == "checkout.session.completed":
            customer = stripe.Customer.retrieve(data['customer'])
            customer_orderID = customer["metadata"]["orderId"]
            order_controller.update_order_to_paid(customer_orderID, data)
            
        return '', 200
        
        
    
    except ValueError as e:
        return jsonify({'message': f'Invalid payload: {str(e)}'}), 400
    except stripe.error.SignatureVerificationError as e: 
        return jsonify({'message': f'Signature verification failed: {str(e)}'}), 400



