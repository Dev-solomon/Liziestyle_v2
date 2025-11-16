from flask import current_app as app, url_for
from pytz import timezone, UTC
from datetime import timedelta
import time, datetime
import random
import uuid
import cloudinary
import requests
import os
import json, re
from termcolor import colored
import cloudinary.api   
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from itsdangerous import  URLSafeSerializer
from main.middleware.mailer import send_email_signup

def nowDatetimeUserTimezone(user_timezone):
	tzone = timezone(user_timezone)
	return datetime.datetime.now(tzone)

def nowDatetimeUTC():
	tzone = UTC
	now = datetime.datetime.now(tzone)
	return now

def JsonResp(data, status):
	from flask import Response
	from bson import json_util
	import json
	return Response(json.dumps(data, default=json_util.default), mimetype="application/json", status=status)

def randID():
	randId = uuid.uuid4().hex
	return randId

def randString(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890")

	return randString

def randStringCaps(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")

	return randString

def randStringNumbersOnly(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("23456789")

	return randString

def validEmail(email):
	import re

	if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
		return True
	else:
		return False

cloudinary.config(
       cloud_name="dns8ckviy",
       api_key=os.getenv('cloudinary_api_key'),
       api_secret=os.getenv('cloudinary_api_secret')
)

def upload_image(file_path):
# Example usage
# uploaded_image_url = upload_image("path/to/your/image.jpg")

# Upload from a remote URL
# response = cloudinary.uploader.upload("https://example.com/image.jpg")

# Upload with options (e.g., specifying a folder or tags)
# response = cloudinary.uploader.upload("path/to/image.jpg", folder="my_images", tags=["sample", "test"])
    try: 
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(file_path, folder="products_images")
        
        # Get the URL of the uploaded image
        url = response.get("url")
        # print(f"Image uploaded successfully: {url}")
        return url
    except Exception as e:
        print("Error on uploading file.")
        return 'Error on uploading file.'
    
def upload_profile_image(file_path):
# Example usage
# uploaded_image_url = upload_image("path/to/your/image.jpg")

# Upload from a remote URL
# response = cloudinary.uploader.upload("https://example.com/image.jpg")

# Upload with options (e.g., specifying a folder or tags)
# response = cloudinary.uploader.upload("path/to/image.jpg", folder="my_images", tags=["sample", "test"])
    try:
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(file_path, folder="profile_images")
        
        # Get the URL of the uploaded image
        url = response.get("url")
        print(f"Image uploaded successfully: {url}")
        return url
    except Exception as e:
        print("Error on uploading file.")
        return 'Error on uploading file.'
    
serializer = URLSafeSerializer(os.getenv('SECRET_KEY'))
    
def generate_verification_token(user_data):
    return serializer.dumps(user_data, salt='email-confirmation-salt')


def send_verification_email(user_email, token):
    verification_url = url_for('user.verify_email', token=token, _external=True, _scheme='https')
    
    send_a_mail = send_email_signup(user_email, "[Azione richiesta] - liziestyle", f"Verifica la tua email facendo clic sul collegamento riportato di seguito: \n {verification_url}. \n Il collegamento scade tra 15 minuti.")
    return send_a_mail
    
def verify_email_token(token, expiration=900): # 900 seconds = 15 minutes
    try:
        user_data = serializer.loads(token, salt='email-confirmation-salt', max_age=expiration)
        return user_data
    except:
        return None
    

# Try to get User's Location
def get_country_code_from_ip():
    # 1) Try ipapi.co
    try:
        r = requests.get("https://ipapi.co/json/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country")
            if code:
                return code
        # if 429 or other issue, fall through to next provider
    except Exception:
        pass

    # 2) Try ipinfo.io
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country")
            if code:
                return code
    except Exception:
        pass

    # 3) Try ipwho.is
    try:
        r = requests.get("https://ipwho.is/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            code = data.get("country_code")
            if code:
                return code
    except Exception:
        pass

    # If everything fails
    return None
	
# Get the Exact Location of the Client Shopping to detech which currency to show
def get_currency_symbol():
    country_code = get_country_code_from_ip()

    if country_code == "US":
        print(colored(f"Country Detected:=> {country_code}", "cyan"))
        return "$"
    elif country_code is None:
        # total failure – choose a default for your store
        print(colored(f"Country Detected Is None", "cyan"))
        return "€"   # or "$" depending on your main market
    else:
        # For now: anything not US → euro
        print(colored(f"Country Detected:=> {country_code}", "cyan"))
        return "€"



    

    

	
 

