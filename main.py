from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.database import db
from app.utils.auth import jwt
from app import create_app
from app.routes import users, products, orders, community

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi
    db.init_app(app)
    jwt.init_app(app)

    # Blueprint registration
    app.register_blueprint(users.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(community.bp)

    @app.route("/")
    def index():
        return {"message": "ReCircle API is running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
