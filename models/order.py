from datetime import datetime
from models.product import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def calculate_total(self):
        """Calcula el total de la orden"""
        return sum(item.subtotal for item in self.items)
    
    def update_status(self, new_status):
        """Actualiza el estado de la orden"""
        if new_status not in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
            raise ValueError("Estado de orden inválido")
        self.status = new_status
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Precio al momento de la compra
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.quantity * self.price
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.subtotal
        } 