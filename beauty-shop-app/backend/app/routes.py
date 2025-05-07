from flask import request, jsonify
from . import db
from .models import Product, Service, Booking, ProductSale, Customer, Order, OrderItem
from flask import Blueprint
from datetime import datetime, timedelta 

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

# Alert Api
@bp.route("/alerts/products", methods=["GET"])
def product_alerts():
    low_stock_threshold = 5
    expiration_threshold = timedelta(days=7)
    slow_sales_threshold_days = 14
    today = datetime.utcnow()

    low_stock = Product.query.filter(Product.quantity <= low_stock_threshold).all()
    near_expiry = Product.query.filter(Product.expiry_date != None).filter(
        Product.expiry_date <= (today + expiration_threshold).date()
    ).all()

    # Products not sold in the last 14 days
    slow_selling_products = []
    all_products = Product.query.all()
    for product in all_products:
        recent_sale = ProductSale.query.filter_by(product_id=product.id).order_by(ProductSale.sale_date.desc()).first()
        if not recent_sale or (today - recent_sale.sale_date).days >= slow_sales_threshold_days:
            slow_selling_products.append(product)

    return jsonify({
        "low_stock": [p.to_dict() for p in low_stock],
        "near_expiry": [p.to_dict() for p in near_expiry],
        "slow_selling": [p.to_dict() for p in slow_selling_products]
    })

# Summary API endpoints
@bp.route("/admin/summary", methods=["GET"])
def admin_summary():
    total_products = Product.query.count()
    total_services = Service.query.count()
    total_bookings = Booking.query.count()
    total_sales = ProductSale.query.count()

    # Total revenue from product sales
    sales = ProductSale.query.all()
    total_revenue = sum(s.quantity_sold * s.sale_price for s in sales)
    total_cost = sum(s.quantity_sold * s.product.cost_price for s in sales)
    net_profit = total_revenue - total_cost

    # Most sold product
    popular_product = db.session.query(
        Product.name, db.func.sum(ProductSale.quantity_sold).label("total_sold")
    ).join(ProductSale).group_by(Product.id).order_by(db.desc("total_sold")).first()

    # Most booked service
    popular_service = db.session.query(
        Service.name, db.func.count(Booking.id).label("total_booked")
    ).join(Booking).group_by(Service.id).order_by(db.desc("total_booked")).first()

    return jsonify({
        "totals": {
            "products": total_products,
            "services": total_services,
            "bookings": total_bookings,
            "sales": total_sales
        },
        "revenue": {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "net_profit": net_profit
        },
        "popular_product": {
            "name": popular_product[0] if popular_product else None,
            "sold": popular_product[1] if popular_product else 0
        },
        "popular_service": {
            "name": popular_service[0] if popular_service else None,
            "booked": popular_service[1] if popular_service else 0
        }
    })


# Register
@bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400

    if Customer.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    customer = Customer(name=data["name"], email=data["email"])
    customer.set_password(data["password"])
    db.session.add(customer)
    db.session.commit()

    return jsonify(customer.to_dict()), 201

# Login
@bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    customer = Customer.query.filter_by(email=data.get("email")).first()
    if not customer or not customer.check_password(data.get("password")):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "customer": customer.to_dict()
    }), 200

# Order
@bp.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    customer_id = data.get("customer_id")
    items = data.get("items")  # [{product_id, quantity}]

    if not customer_id or not items:
        return jsonify({"error": "Missing customer or items"}), 400

    total = 0
    order_items = []

    for item in items:
        product = Product.query.get(item["product_id"])
        if not product or product.quantity < item["quantity"]:
            return jsonify({"error": f"Product {item['product_id']} not available in required quantity"}), 400

        price = product.sale_price
        total += price * item["quantity"]

        order_items.append({
            "product": product,
            "quantity": item["quantity"],
            "price": price
        })

    # Create Order
    order = Order(customer_id=customer_id, total_price=total)
    db.session.add(order)
    db.session.flush()  # Get order.id

    for item in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"]
        )
        db.session.add(order_item)

        # Update product stock
        item["product"].quantity -= item["quantity"]

    db.session.commit()
    return jsonify(order.to_dict()), 201


# Get Order History (by Customer)
@bp.route("/orders/customer/<int:customer_id>", methods=["GET"])
def get_orders_by_customer(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).order_by(Order.order_date.desc()).all()
    return jsonify([order.to_dict() for order in orders])

# Admin Order Status Update
@bp.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["pending", "completed", "cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status == "cancelled":
        return jsonify({"error": "Order already cancelled"}), 400

    # Only restock if order is being cancelled
    if new_status == "cancelled":
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.quantity += item.quantity

    order.status = new_status
    db.session.commit()
    return jsonify(order.to_dict())


# Get All Orders (for admin view)
@bp.route("/orders", methods=["GET"])
def get_all_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return jsonify([order.to_dict() for order in orders])


# Cancel Order with time limit
@bp.route("/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Already cancelled or completed?
    if order.status in ["cancelled", "completed"]:
        return jsonify({"error": f"Cannot cancel a {order.status} order"}), 400

    # Check if within 2 minutes
    time_limit = order.order_date + timedelta(minutes=2)
    if datetime.utcnow() > time_limit:
        return jsonify({"error": "Cancellation window has expired"}), 403

    # Restock products
    for item in order.items:
        product = Product.query.get(item.product_id)
        if product:
            product.quantity += item.quantity

    order.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "Order cancelled and items restocked", "order": order.to_dict()})


# Low Stock Alert
@bp.route("/alerts/low-stock", methods=["GET"])
def low_stock_alerts():
    threshold = request.args.get("threshold", 5, type=int)  # Default threshold is 5
    low_stock_products = Product.query.filter(Product.quantity <= threshold).all()
    return jsonify([product.to_dict() for product in low_stock_products])

# Expiring Soon Alert
@bp.route("/alerts/expiring-soon", methods=["GET"])
def expiring_soon_alerts():
    days = request.args.get("days", 7, type=int)  # Default 7 days
    today = datetime.utcnow().date()
    expiry_limit = today + timedelta(days=days)

    expiring_products = Product.query.filter(
        Product.expiry_date != None,
        Product.expiry_date <= expiry_limit
    ).all()
    return jsonify([product.to_dict() for product in expiring_products])

# Sales Analytics
@bp.route("/analytics/profit-loss", methods=["GET"])
def profit_loss():
    # Optional: filter by date
    start_date_str = request.args.get("start")
    end_date_str = request.args.get("end")

    query = Order.query.filter_by(status="completed")

    if start_date_str:
        start_date = datetime.fromisoformat(start_date_str)
        query = query.filter(Order.order_date >= start_date)
    if end_date_str:
        end_date = datetime.fromisoformat(end_date_str)
        query = query.filter(Order.order_date <= end_date)

    orders = query.all()

    total_revenue = 0
    total_cost = 0

    for order in orders:
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                revenue = item.quantity * item.price
                cost = item.quantity * product.cost_price
                total_revenue += revenue
                total_cost += cost

    total_profit = total_revenue - total_cost

    return jsonify({
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit,
        "from": start_date_str,
        "to": end_date_str
    })
