from flask import Flask
from flask_cors import CORS
from app.database import init_db
from app.utils.auth import jwt
from flask_restx import Api
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)
    jwt.init_app(app)
    CORS(app)

    api = Api(
        app,
        doc="/docs",
        title="ReCircle API",
        version="1.0",
        description="API documentation for ReCircle",
        prefix="/api" 
    )

    from app.routes.users import user_ns
    from app.routes.products import product_ns
    from app.routes.orders import order_ns
    from app.routes.community import community_ns
    from app.routes.misc import misc_ns

    api.add_namespace(user_ns, path="/users")
    api.add_namespace(product_ns, path="/products")
    api.add_namespace(order_ns, path="/orders")
    api.add_namespace(community_ns, path="/community")
    api.add_namespace(misc_ns)

    @app.route("/")
    def home():
        return {"message": "Welcome to ReCircle API!"}

    return app
