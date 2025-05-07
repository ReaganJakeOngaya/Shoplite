from . import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    expiration_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "created_at": self.created_at.isoformat()
        }

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)  # Optional: How long the service takes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at.isoformat()
        }

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)  # Can be changed to customer_id later
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="scheduled")  # scheduled, completed, cancelled
    payment_status = db.Column(db.String(50), default="unpaid")  # unpaid, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service = db.relationship('Service', backref='bookings')

    def to_dict(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "service_name": self.service.name if self.service else None,
            "customer_name": self.customer_name,
            "scheduled_time": self.scheduled_time.isoformat(),
            "status": self.status,
            "payment_status": self.payment_status,
            "created_at": self.created_at.isoformat()
        }
        
class ProductSale(db.Model):
    __tablename__ = 'product_sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='sales')

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity_sold": self.quantity_sold,
            "sale_price": self.sale_price,
            "sale_date": self.sale_date.isoformat()
        }
        