from flask import request, jsonify
from . import db
from .models import Product
from flask import Blueprint
from datetime import datetime

bp = Blueprint("api", __name__, url_prefix="/api")

# CREATE a product
from datetime import datetime

@bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data or "quantity" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert expiration_date to a Python date object if provided
        expiration_date = None
        if data.get("expiration_date"):
            try:
                expiration_date = datetime.strptime(data["expiration_date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        product = Product(
            name=data["name"],
            description=data.get("description"),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            expiration_date=expiration_date
        )

        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


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
from datetime import datetime

@bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.quantity = data.get("quantity", product.quantity)

    # Convert expiration_date to a Python date object if provided
    expiration_date = data.get("expiration_date", product.expiration_date)
    if expiration_date:
        try:
            # Only convert if it's a string (not already a date object)
            if isinstance(expiration_date, str):
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    product.expiration_date = expiration_date

    try:
        db.session.commit()
        return jsonify(product.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# DELETE a product
@bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
