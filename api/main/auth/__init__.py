from flask import current_app as app, make_response, redirect, url_for, session, render_template
from flask import request
from functools import wraps
from main.tools import JsonResp
import jwt
import os
import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from main.user.models.user_model import User
from flask import make_response
import datetime
import requests

print(datetime.datetime.utcnow() + datetime.timedelta(hours=1))

client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]
bcrypt = Bcrypt(app)



# Auth Decorator
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		access_token = request.cookies.get('token')
  		# google_access = session.get('user')
		# print(access_token)	
  
		if not access_token:
			return render_template('user/login.html')

		if access_token:
			try:
				data = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=["HS256"])
				current_user = User.collection.find_one({'email': data['email']})
				if not current_user:
					raise Exception("User not found")
			except Exception as e:
				return render_template('user/login.html')

		# if google_access != None:
		# 	try: 
		# 		user = google_access['email']
		# 		current_user = User.collection.find_one({'user': user})
		# 	except Exception as e:
		# 		return JsonResp({ "message": "Token is invalid", "exception": str(e) }, 401)
  

		kwargs['current_user'] = current_user  # Pass current_user to the wrapped function
		return f(*args, **kwargs)	

	return decorated

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		access_token = request.cookies.get('token')
		# print(access_token)
  
		if not access_token:
			return render_template('user/login.html')

		try:
			data = jwt.decode(access_token, app.config['SECRET_KEY'],  algorithms=["HS256"])
			current_user = User.collection.find_one({'user': data })
		except Exception as e:
			return JsonResp({ "message": "Token is invalid", "exception": str(e) }, 401)

		return f(*args, **kwargs)	

	return decorated

def set_cookies(token, redirect_url):
  resp = make_response(redirect(url_for(redirect_url))) 
  resp.set_cookie('token', str(token))
  return resp

def del_cookies():
    resp = make_response(redirect(url_for('user.user_login', message="Non effettuato l'accesso"))) 
    resp.delete_cookie('session')
    return resp

def encodeAccessToken(email):
	expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)
	accessToken = jwt.encode({
		"email": email,
		"exp": expiration_date,  # The token will expire in 15 minutes
	}, app.config["SECRET_KEY"], algorithm="HS256")

	return accessToken

def encodeRefreshToken(email):

	refreshToken = jwt.encode({
		"email": email,
		"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) # The token will expire in 4 weeks
	}, app.config["SECRET_KEY"], algorithm="HS256")

	return refreshToken

def refreshAccessToken(refresh_token):

	# If the refresh_token is still valid, create a new access_token and return it
	try:
		user = app.db.users.find_one({ "refresh_token": refresh_token }, { "_id": 0, "id": 1, "email": 1 })

		if user:
			decoded = jwt.decode(refresh_token, app.config["SECRET_KEY"])
			new_access_token = encodeAccessToken(decoded["email"])
			result = jwt.decode(new_access_token, app.config["SECRET_KEY"])
			result["new_access_token"] = new_access_token
			resp = JsonResp(result, 200)
		else:
			result = { "message": "Auth refresh token has expired" }
			resp = JsonResp(result, 403)

	except:
		result = { "message": "Auth refresh token has expired" }
		resp = JsonResp(result, 403)

	return resp

def validate_turnstile_token(token, ip):
	url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
	data = {
		"secret": os.getenv('CLOUDFARE_SECRET_KEY'),
		"response": token,
		"remoteip": ip
	}
	response = requests.post(url, data=data)
	
	return response.json()
	
