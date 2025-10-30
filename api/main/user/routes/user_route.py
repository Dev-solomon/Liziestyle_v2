from flask import Blueprint
import requests
from flask import current_app as app
from flask import Flask, request, jsonify, session, redirect
from main.auth import token_required, del_cookies
from main.user.controllers.user_controller import *
from main.user.models.user_model import User
from authlib.common.security import generate_token
from authlib.integrations.flask_client import OAuth
import json
import datetime

oauth = OAuth(app)


user_blueprint = Blueprint('user',  __name__, "api/user")

@user_blueprint.route('/import', methods=['GET'])
@token_required
def import_all(current_user):
    return import_users()

@user_blueprint.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        return register_user()
    else:
        message_error = request.args.get('message')
        return render_template('user/signup.html', messageError=message_error)


@user_blueprint.route('/verifyemail/<token>', methods=['POST','GET'])
def verify_email(token):
    return register_verified_user(token)


@user_blueprint.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        return login()
    else:
        message_error = request.args.get('message')
        message_success = request.args.get('messageSuccess')
        return render_template('user/login.html', messageError=message_error, message=message_success)

@user_blueprint.route('/', methods=['POST'])
@token_required
def profile(current_user):
    if request.method == 'POST' and request.form.get('_method') == 'PUT':
        return update_profile()
    elif request.method == 'POST' and request.form.get('_method') == 'DELETE':
        return delete_user()

@user_blueprint.route('/password', methods=['POST'])
@token_required
def change_password_route(current_user):
        return change_password()
   
    

@user_blueprint.route('/logout', methods=['POST'])
@token_required
def user_logout(current_user):
    return logout()

# CODE TO LOGIN WITH GOOGLE

CLIENT_ID = "1003891667349-tdpmm4j43ceij66q0s1mq3rnhlqgnp5f.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = None


@user_blueprint.route('/login_google', methods=["POST", 'GET'])
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('user.authorized', _external=True, _scheme='https')
    # print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])


@user_blueprint.route('/login_google/authorized', methods=['POST','GET'])
def authorized():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    # print(" Google User ", session['user'])
    try:
        user = User.collection.find_one({'email': session['user']['email']})
        if user:
            token = encodeAccessToken(user['email'])
            return set_cookies(token, 'home')
        else:
            return del_cookies()
    except Exception as e:
        return jsonify({'message': str(e)}), 400



# CODE TO SIGNUP WITH GOGLE

@user_blueprint.route('/signup_google', methods=["POST", 'GET'])
def signup_google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('user.signup_authorized', _external=True, _scheme='https')
    # print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])


@user_blueprint.route('/signup_google/authorized', methods=['POST','GET'])
def signup_authorized():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    # print(" Google User ", session['user'])
    try:
        user = User.collection.find_one({'email': session['user']['email']})
        if user:
            return redirect(url_for('user.registration', message="L'utente esiste già!"))
        else:
            data = {
                "fullName": session['user']['name'],
                "email": session['user']['email'],
                "createdAt" : datetime.datetime.now().isoformat(),
                "isAdmin": False
            }
            new_user = User.collection.insert_one(data).inserted_id
            created_user = User.collection.find_one({'email': data['email']})
            if(created_user):
                return redirect(url_for('user.user_login', messageSuccess="Utente creato con successo, Accedi!"))
            else:
                 return  redirect(url_for('user.registration', message="Errore durante la creazione dell'utente, riprova!!"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400










