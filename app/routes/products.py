from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.models.product import Product
from app.models.user import User

bp = Blueprint("products", __name__, url_prefix="/products")

@bp.route("/", methods=["GET"])
def get_all_products():
    products = Product.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "category": p.category,
        "price": p.price,
        "tags": p.tags,
        "stock": p.stock,
        "seller_id": p.seller_id,
        "created_at": p.created_at
    } for p in products]
    return jsonify(result)

@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "tags": product.tags,
        "stock": product.stock,
        "seller_id": product.seller_id,
        "created_at": product.created_at
    })

@bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()
    current_user = get_jwt_identity()

    new_product = Product(
        name=data.get("name"),
        description=data.get("description"),
        category=data.get("category"),
        price=data.get("price"),
        tags=data.get("tags"),
        stock=data.get("stock"),
        seller_id=current_user["id"]
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully"}), 201

@bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if product.seller_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.category = data.get("category", product.category)
    product.price = data.get("price", product.price)
    product.tags = data.get("tags", product.tags)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

@bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    current_user = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if product.seller_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
