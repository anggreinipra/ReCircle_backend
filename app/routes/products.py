from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.database import db
from app.models.product import Product

product_ns = Namespace('products', description='Product operations')

product_model = product_ns.model('Product', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'category': fields.String(required=True),
    'price': fields.Float(required=True),
    'tags': fields.String(required=False),
    'stock': fields.Integer(required=True),
})

@product_ns.route("/")
class ProductList(Resource):
    @product_ns.doc('get_all_products')
    def get(self):
        products = Product.query.all()
        return [{
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

    @product_ns.expect(product_model)
    @jwt_required()
    def post(self):
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
        return {"message": "Product created successfully"}, 201

@product_ns.route("/<int:product_id>")
@product_ns.param('product_id', 'The product identifier')
class ProductDetail(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "tags": product.tags,
            "stock": product.stock,
            "seller_id": product.seller_id,
            "created_at": product.created_at
        }

    @jwt_required()
    def put(self, product_id):
        current_user = get_jwt_identity()
        product = Product.query.get_or_404(product_id)

        if product.seller_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.category = data.get("category", product.category)
        product.price = data.get("price", product.price)
        product.tags = data.get("tags", product.tags)
        product.stock = data.get("stock", product.stock)

        db.session.commit()
        return {"message": "Product updated successfully"}

    @jwt_required()
    def delete(self, product_id):
        current_user = get_jwt_identity()
        product = Product.query.get_or_404(product_id)

        if product.seller_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}
