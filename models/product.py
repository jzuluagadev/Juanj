from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from werkzeug.utils import secure_filename
import os

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)
    weight = db.Column(db.Float)  # en gramos
    dimensions = db.Column(db.String(50))  # formato: "largo x ancho x alto"
    material = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    reviews = db.relationship('Review', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        return price
    
    @validates('stock')
    def validate_stock(self, key, stock):
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return stock
    
    @validates('sku')
    def validate_sku(self, key, sku):
        if not sku:
            raise ValueError("El SKU es obligatorio")
        return sku
    
    def update_stock(self, quantity):
        """Actualiza el stock del producto"""
        if self.stock + quantity < 0:
            raise ValueError("Stock insuficiente")
        self.stock += quantity
        db.session.commit()
    
    def is_available(self):
        """Verifica si el producto está disponible"""
        return self.is_active and self.stock > 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'sku': self.sku,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'material': self.material,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'average_rating': self.get_average_rating(),
            'review_count': len(self.reviews)
        }
    
    def get_average_rating(self):
        """Calcula el promedio de calificaciones"""
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @classmethod
    def search(cls, query, category=None, min_price=None, max_price=None):
        """Búsqueda avanzada de productos"""
        filters = []
        
        if query:
            filters.append(
                db.or_(
                    cls.name.ilike(f'%{query}%'),
                    cls.description.ilike(f'%{query}%'),
                    cls.sku.ilike(f'%{query}%')
                )
            )
        
        if category:
            filters.append(cls.category == category)
        
        if min_price is not None:
            filters.append(cls.price >= min_price)
        
        if max_price is not None:
            filters.append(cls.price <= max_price)
        
        return cls.query.filter(*filters).all() 