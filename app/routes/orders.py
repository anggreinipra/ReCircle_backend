
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.models.order import Order
from app.models.product import Product

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json()
    current_user = get_jwt_identity()

    product = Product.query.get_or_404(data.get("product_id"))
    quantity = data.get("quantity")

    if quantity > product.stock:
        return jsonify({"message": "Not enough stock available"}), 400

    total_price = product.price * quantity
    order = Order(
        buyer_id=current_user["id"],
        product_id=product.id,
        quantity=quantity,
        total_price=total_price,
    )

    # Kurangi stok
    product.stock -= quantity

    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order placed successfully", "order_id": order.id}), 201

@bp.route("/", methods=["GET"])
@jwt_required()
def get_user_orders():
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(buyer_id=current_user["id"]).all()

    result = [{
        "id": o.id,
        "product_id": o.product_id,
        "quantity": o.quantity,
        "total_price": o.total_price,
        "status": o.status,
        "created_at": o.created_at
    } for o in orders]

    return jsonify(result)

@bp.route("/<int:order_id>", methods=["PUT"])
@jwt_required()
def update_order_status(order_id):
    current_user = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    product = Product.query.get(order.product_id)

    if product.seller_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    order.status = data.get("status", order.status)

    db.session.commit()
    return jsonify({"message": "Order status updated"})

@bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def cancel_order(order_id):
    current_user = get_jwt_identity()
    order = Order.query.get_or_404(order_id)

    if order.buyer_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    if order.status != "pending":
        return jsonify({"message": "Cannot cancel this order"}), 400

    # Kembalikan stok
    product = Product.query.get(order.product_id)
    product.stock += order.quantity

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order canceled"})
