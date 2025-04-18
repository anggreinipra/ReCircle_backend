from flask import Flask
from flask_cors import CORS
from app.database import init_db
from app.utils.auth import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    init_db(app)
    jwt.init_app(app)
    CORS(app)

    from app.routes import users, products, orders, community
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(community.bp)

    return app
