from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.database import db
from app.models.order import Order
from app.models.product import Product

order_ns = Namespace('orders', description='Order operations')

order_model = order_ns.model('Order', {
    'product_id': fields.Integer(required=True, description='ID of the product to order'),
    'quantity': fields.Integer(required=True, description='Quantity to order')
})

status_model = order_ns.model('StatusUpdate', {
    'status': fields.String(required=True, description='New status for the order')
})

@order_ns.route("/")
class OrderList(Resource):
    @order_ns.expect(order_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()

        product = Product.query.get_or_404(data.get("product_id"))
        quantity = data.get("quantity")

        if quantity > product.stock:
            return {"message": "Not enough stock available"}, 400

        total_price = product.price * quantity
        order = Order(
            buyer_id=current_user["id"],
            product_id=product.id,
            quantity=quantity,
            total_price=total_price,
        )

        product.stock -= quantity
        db.session.add(order)
        db.session.commit()

        return {"message": "Order placed successfully", "order_id": order.id}, 201

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        orders = Order.query.filter_by(buyer_id=current_user["id"]).all()

        return [{
            "id": o.id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "status": o.status,
            "created_at": o.created_at
        } for o in orders]

@order_ns.route("/<int:order_id>")
@order_ns.param('order_id', 'The order ID')
class OrderDetail(Resource):
    @order_ns.expect(status_model)
    @jwt_required()
    def put(self, order_id):
        current_user = get_jwt_identity()
        order = Order.query.get_or_404(order_id)
        product = Product.query.get(order.product_id)

        if product.seller_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        order.status = data.get("status", order.status)

        db.session.commit()
        return {"message": "Order status updated"}

    @jwt_required()
    def delete(self, order_id):
        current_user = get_jwt_identity()
        order = Order.query.get_or_404(order_id)

        if order.buyer_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        if order.status != "pending":
            return {"message": "Cannot cancel this order"}, 400

        product = Product.query.get(order.product_id)
        product.stock += order.quantity

        db.session.delete(order)
        db.session.commit()
        return {"message": "Order canceled"}
