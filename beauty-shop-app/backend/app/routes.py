from flask import request, jsonify
from . import db
from .models import Product
from flask import Blueprint
from datetime import datetime

bp = Blueprint("api", __name__, url_prefix="/api")

# CREATE a product
@bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    # Convert expiration_date string to a Python date object if provided
    expiration_date = None
    if data.get("expiration_date"):
        expiration_date = datetime.strptime(data["expiration_date"], "%Y-%m-%d").date()

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        quantity=data["quantity"],
        expiration_date=expiration_date
    )

    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# READ all products
@bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

# READ a single product
@bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

# UPDATE a product
@bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.quantity = data.get("quantity", product.quantity)
    product.expiration_date = data.get("expiration_date", product.expiration_date)
    db.session.commit()
    return jsonify(product.to_dict())

# DELETE a product
@bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
