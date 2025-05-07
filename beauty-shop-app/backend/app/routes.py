from flask import request, jsonify
from . import db
from .models import Product, Service, Booking, ProductSale 
from flask import Blueprint
from datetime import datetime

bp = Blueprint("api", __name__, url_prefix="/api")

# CREATE a product

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
    try:
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ a single product
@bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE a product
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
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# CREATE service
@bp.route("/services", methods=["POST"])
def create_service():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        service = Service(
            name=data["name"],
            description=data.get("description"),
            price=float(data["price"]),
            duration_minutes=int(data["duration_minutes"]) if data.get("duration_minutes") else None
        )
        db.session.add(service)
        db.session.commit()
        return jsonify(service.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# GET all services
@bp.route("/services", methods=["GET"])
def get_services():
    try:
        services = Service.query.all()
        return jsonify([s.to_dict() for s in services])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET one service
@bp.route("/services/<int:id>", methods=["GET"])
def get_service(id):
    try:
        service = Service.query.get_or_404(id)
        return jsonify(service.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE service
@bp.route("/services/<int:id>", methods=["PUT"])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    try:
        service.name = data.get("name", service.name)
        service.description = data.get("description", service.description)
        service.price = float(data.get("price", service.price))
        service.duration_minutes = int(data.get("duration_minutes", service.duration_minutes))
        db.session.commit()
        return jsonify(service.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE service
@bp.route("/services/<int:id>", methods=["DELETE"])
def delete_service(id):
    try:
        service = Service.query.get_or_404(id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# CREATE a booking
@bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    if not data or "service_id" not in data or "customer_name" not in data or "scheduled_time" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        booking = Booking(
            service_id=data["service_id"],
            customer_name=data["customer_name"],
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            status=data.get("status", "scheduled"),
            payment_status=data.get("payment_status", "unpaid")
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify(booking.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# GET all bookings
@bp.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings])

# GET one booking
@bp.route("/bookings/<int:id>", methods=["GET"])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_dict())

# UPDATE booking
@bp.route("/bookings/<int:id>", methods=["PUT"])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    data = request.get_json()
    booking.customer_name = data.get("customer_name", booking.customer_name)
    booking.scheduled_time = datetime.fromisoformat(data.get("scheduled_time")) if data.get("scheduled_time") else booking.scheduled_time
    booking.status = data.get("status", booking.status)
    booking.payment_status = data.get("payment_status", booking.payment_status)
    db.session.commit()
    return jsonify(booking.to_dict())

# DELETE booking
@bp.route("/bookings/<int:id>", methods=["DELETE"])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted successfully"})


# Create a sale
@bp.route("/sales", methods=["POST"])
def create_product_sale():
    data = request.get_json()
    if not data or "product_id" not in data or "quantity_sold" not in data or "sale_price" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Optionally: reduce quantity from stock (optional)
    if product.quantity < data["quantity_sold"]:
        return jsonify({"error": "Not enough stock"}), 400
    product.quantity -= data["quantity_sold"]

    sale = ProductSale(
        product_id=data["product_id"],
        quantity_sold=data["quantity_sold"],
        sale_price=data["sale_price"]
    )
    db.session.add(sale)
    db.session.commit()
    return jsonify(sale.to_dict()), 201

# List all sales
@bp.route("/sales", methods=["GET"])
def get_product_sales():
    sales = ProductSale.query.all()
    return jsonify([s.to_dict() for s in sales])

# Get profit summary
@bp.route("/sales/summary", methods=["GET"])
def get_sales_summary():
    sales = ProductSale.query.all()
    total_revenue = sum(s.quantity_sold * s.sale_price for s in sales)
    total_cost = sum(s.quantity_sold * s.product.cost_price for s in sales)
    profit = total_revenue - total_cost

    return jsonify({
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "net_profit": profit
    })

