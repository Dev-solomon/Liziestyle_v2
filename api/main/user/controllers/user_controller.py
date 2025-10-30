from flask import Flask, jsonify, request, make_response, url_for, redirect, render_template
from flask_bcrypt import Bcrypt
from main.user.models.user_model import User
from main.auth import encodeAccessToken, set_cookies, validate_turnstile_token
from flask import current_app as app 
from bson import ObjectId
import datetime
import os
from werkzeug.utils import secure_filename
from main.tools import upload_profile_image
from main.tools import generate_verification_token, verify_email_token, send_verification_email


bcrypt = Bcrypt(app)



# Import users from data - usually for test
def import_users():
    try:
        data = request.json
        User.collection.delete_many({})
        import_users = User.collection.insert_many(data['users'])
        return jsonify({'message': 'Users imported successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Login user
def login():
    try:
        data = request.form.to_dict()
        user = User.collection.find_one({'email': data['email']})
        
        if user and 'password' not in user:
            return render_template("user/login.html", messageError="Nessuna password, prova ad accedere a Google") 
        
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            token = encodeAccessToken(user['email'])
            return set_cookies(token, 'home')
        else:
             return render_template("user/login.html", messageError="E-mail o password non valide")
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    # User by ID
def get_user(id):
    try:
        user = User.collection.find_one({'_id': ObjectId(id)}) 
        if user:
           return user
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    # user by email
def get_user_by_email(email):
    try:
        user = User.collection.find_one({'email': email}) 
        if user:
           return user
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Update user profile
def update_profile():
    try:
        data = request.form.to_dict()
        files = request.files.get('image')
        
        # Exclude '_id' from the update operation
        update_data = {key: value for key, value in data.items() if key != '_method' and key != 'check_email'}
        
        # code for saving file uploaded in profile
        file_path = os.path.join('uploads/', secure_filename(files.filename))
        files.save(file_path)
        # upload file to cloudinary for storage there
        image_url = upload_profile_image(file_path)
        update_data['image'] = str(image_url)
        # Remove the file after successful upload
        os.remove(file_path)
        print(f"Local file removed: {file_path}")
       
        
        update_user = User.collection.update_one(
            {'email': data['check_email']},
            {'$set': update_data}
        )
        if update_user.modified_count > 0:
            return render_template('user/update_profile.html', message="Password aggiornata correttamente")
        else:
            return render_template('user/update_profile.html', messageError="Qualcosa è andato storto, riprova!")
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Change user password
def change_password():
    try:
        data = request.form.to_dict()
        user = User.collection.find_one({'email': data['email']})
        if "password" not in user:
            User.collection.update_one(
                {'email': data['email']},
                {'$set': {'password': bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')}}
            )
            return render_template('user/change_password.html', message="Password aggiornata correttamente")
        
        elif bcrypt.check_password_hash(user['password'], data['oldPassword']):
            User.collection.update_one(
                {'email': data['email']},
                {'$set': {'password': bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')}}
            )
            return render_template('user/change_password.html', message="Password aggiornata correttamente")
        else:
            return render_template('user/change_password.html', messageError="Vecchia password non valida")
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Delete user
def delete_user():
    try:
        data = request.form.to_dict()
        user = User.collection.delete_one({'_id': ObjectId(data['_id'])})
        if user.deleted_count > 0:  
            return render_template('user/login.html', message="Utente eliminato correttamente")
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Register a new user
def register_user():
    try:
        data = request.form.to_dict()
        cloudfare_token = data["cf-turnstile-response"]
        ip = request.headers.get("CF-Connecting-IP")
        user = User.collection.find_one({'email': data['email']})
        if (user):
           return render_template("user/signup.html", message="L'utente esiste già")
        else:
            outcome = validate_turnstile_token(cloudfare_token, ip)
            if outcome.get("success") == True:
                #create a verification email token
                token = generate_verification_token({'email': data['email'], 'fullName': data['fullName'], 'password': data['password']})
                # Send the verification email
                mail_sent = send_verification_email(data['email'], token)
                # print(mail_sent)
                if mail_sent == True:
                    # Alert User to check email for verification link.
                    return render_template("user/signup.html", message="Ti è stata inviata un'e-mail di verifica")
                # Something Wrong with the Email Provided, Could not deliver Email verification to user.
                return render_template("user/signup.html", messageError="Errore nell'invio della verifica all'e-mail!")
            # Alert User, This must be a spam attack, Cloudfare token not verified.
            return render_template("user/signup.html", messageError="Token non valido: verifica di essere umano!")
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
def register_verified_user(token):
    
    data = verify_email_token(token)
    user = User.collection.find_one({'email': data['email']})
    
    if (user):
           return render_template("user/signup.html", message="L'utente esiste già")
    elif data:
            data['createdAt'] = datetime.datetime.now().isoformat()   
            data['isAdmin'] = False
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['password'] = hashed_password
            new_user = User.collection.insert_one(data).inserted_id
            created_user = User.collection.find_one({'email': data['email']})
            if(created_user):
                # token = encodeAccessToken(created_user['email'])
                # print(token)
                return render_template("user/login.html", message="Email verificata con successo, Accedi!")
            else:
                return render_template("user/signup.html", messageError="Il link di verifica non è valido o è scaduto, riprova!")
   

#  Logout a user  and delete cookies
def logout():
    resp = make_response(redirect(url_for('user.user_login'))) 
    resp.delete_cookie('token')
    return resp



