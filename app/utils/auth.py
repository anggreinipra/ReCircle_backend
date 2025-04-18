import jwt
import os
import datetime
from functools import wraps
from flask import request, jsonify
from app.config import Config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

jwt = JWTManager()

def init_jwt(app):
    jwt.init_app(app)

def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is invalid or expired!"}), 401
        return f(*args, **kwargs)
    return decorated
