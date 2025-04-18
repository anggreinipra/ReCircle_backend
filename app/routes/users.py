from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

# Buat namespace khusus untuk user-related endpoints
user_ns = Namespace('users', description='User related operations')

# Swagger model untuk input user
user_model = user_ns.model('User', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

login_model = user_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@user_ns.route('/register')
class Register(Resource):
    @user_ns.expect(user_model)
    def post(self):
        try:      
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if User.query.filter_by(email=email).first():
                return {"message": "Email already registered"}, 409

            hashed_pw = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_pw)

            db.session.add(new_user)
            db.session.commit()

            return {"message": "User registered successfully"}, 201
        
        except Exception as e:
            return {"error": str(e)}, 500

@user_ns.route('/login')
class Login(Resource):
    @user_ns.expect(login_model)
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                return {"message": "Invalid credentials"}, 401

            token = create_access_token(identity={"id": user.id, "role": user.role})
            return {"access_token": token}, 200

        except Exception as e:
            return {"error": str(e)}, 500

@user_ns.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            return {"user": current_user}, 200
        except Exception as e:
            return {"error": str(e)}, 500
