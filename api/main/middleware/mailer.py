import os
import requests
import logging
from main.middleware.email_template import order_template
import mailtrap as mt
from flask import jsonify


# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration (Use environment variables for sensitive information)
EMAIL_SENDER = "hello@liziestyle.com"
REPLY_SENDER = "support@liziestyle.com"
    



def send_email(to_email_user, subject, content, order):
    try:
        url = "https://bulk.api.mailtrap.io/api/send"

        payload = {
            "to": [
                {
                    "email": to_email_user,
                }
            ],
            "from": {
                "email": EMAIL_SENDER,
                "name": "Conferma del nuovo ordine"
            },
            "reply_to": {
                "email": REPLY_SENDER,
                "name": "risposta all'e-mail"
            },
            "custom_variables": {
                "user_id": "45982",
                "batch_id": "PSJ-12"
            },
            "headers": { "X-Message-Source": "dev.mydomain.com" },
            "subject": subject,
            "text": content,
            "html": order_template(order),
            "category": "Integration For New Order"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Api-Token": os.getenv('MAILTRAP_TOKEN')
        }

        response = requests.post(url, json=payload, headers=headers)

        logger(response.json())
        
        return response.status_code
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400
        

def send_email_signup(to_email_user, subject, content):
    try:

        # Create mailtrap message
        mail = mt.Mail(
        sender=mt.Address(email=EMAIL_SENDER, name="Verifica il tuo account"),
        to=[mt.Address(email=to_email_user)],
        subject=subject,
        text=content,
        category="Integration For Signup",
)

        # Send the email
        client = mt.MailtrapClient(token=os.getenv('MAILTRAP_TOKEN'))
        response = client.send(mail)
        
        if response['success']  == True:
            return True
        return False
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400
        
        








