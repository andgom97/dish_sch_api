from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from errors import *
from file import read_users, write_users
from prcolors import *

auth = HTTPBasicAuth()

users = read_users()

# Function that returns the user credentials if exist
def get_user(username):
    for user in users:
        # if username value is the same return the user
        if user['username']==username:
            return user
    # if no user with that username return None
    return None

# Function that hashes the input password
def hash_password(password):
    return pwd_context.encrypt(password)

def generate_auth_token(username, expiration = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'username' : username })

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        prPurple('Loading token')
        data = s.loads(token)
        prGreen('Token loaded')
    except SignatureExpired:
        prRed('Token expired')
        return None # valid token, but expired
    except BadSignature:
        prRed('Invalid token')
        return None # invalid token
    user = get_user(data['username'])
    return user

# Function to verify credentials
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    prPurple('Verifying user by token')
    if not user:
        # if it isn't a token verify by username and password
        user = get_user(username_or_token)
        prPurple('Verifying user by username and password')
        if not user or not pwd_context.verify(password, user['password_hash']):
            return False
    g.user = user
    prGreen('User verified')
    return True

# Function to register a new users
@app.route('/api/user',methods=['POST'])
def register_user():
    try:
        new_user = {
            'username':request.json['username'],
            'password_hash':hash_password(request.json['password'])
        }
        if get_user(new_user['username'])==None:
            users.append(new_user)
            write_users(users)
            prGreen(f"User {new_user['user']} created") 
            return jsonify({'username':new_user['username']}), 201
        prRed(f"Username {new_user['user']} already in use") 
        return already_exist(409)
    except KeyError:
        return bad_request(400)
    except TypeError:
        return bad_request(400)

# Function to get a new tokens
@app.route('/api/token',methods=['GET'])
@auth.login_required
def get_token():
    prPurple(f"Generating token for {g.user['username']}")
    token = generate_auth_token(g.user['username'])
    prGreen('Token generated')
    return jsonify({ 'token': token.decode('ascii') })