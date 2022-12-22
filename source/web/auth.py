from source.web import app, redis
from source.db import db, bcrypt
from source.db.models.user import User

from flask import request
from flask_httpauth import HTTPTokenAuth

import traceback

import os


auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    if token == os.environ.get("ADMIN_PASSWORD", "admin"):
        return "admin"
    if str("uid-auth-token:" + token) in redis.keys("uid-auth-token:*"):
        uid = str(int(redis.get(str("uid-auth-token:" + token))))
        if redis.get(str("auth-token-uid:" + uid)) == token:
            return db.query(User).get(int(uid))

@app.route("/register", methods=["POST"])
def register():
    post_data = request.get_json()
    # check if user already exists
    user = db.query(User).filter(User.email==post_data.get('email')).first()
    if not user:
        try:
            user = User(
                email=post_data.get('email'),
                password=post_data.get('password')
            )
            # insert the user
            db.add(user)
            db.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.email)
            redis.set(str("uid-auth-token:" + auth_token), user.id)
            redis.set(str("auth-token-uid:" + str(user.id)), auth_token)
            responseObject = {
                'success': True,
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            responseObject = ({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }, 500)
    else:
        responseObject = {
            'success': False,
            'message': 'User already exists. Please Log in.',
        }
    return responseObject


@app.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()
    # check if user already exists
    user = db.query(User).filter(User.email==post_data.get('email')).first()
    
    if not user:
        return ({
                'success': False,
                'message': 'No user with that email found.'
        }, 401)
    pwd_match = bcrypt.check_password_hash(user.password, post_data.get('password'))
    if pwd_match:
        auth_token = user.encode_auth_token(user.email)
        redis.set(str("uid-auth-token:" + auth_token), user.id)
        redis.set(str("auth-token-uid:" + str(user.id)), auth_token)
        return ({
                'success': True,
                'auth_token': auth_token
        }, 200)
    else:
        return ({
                'success': False,
                'message': "Incorrect username or password."
        }, 401)