"""
Modelo de Producto para la tienda de joyería.
Define la estructura de datos para los productos y sus imágenes.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductImage(db.Model):
    """Modelo para las imágenes de los productos."""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProductImage {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'is_main': self.is_main,
            'created_at': self.created_at.isoformat()
        }


class Product(db.Model):
    """Modelo principal de Producto."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    material = db.Column(db.String(100))
    color = db.Column(db.String(50))
    dimensions = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con las imágenes
    images = db.relationship(
        'ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')

    @property
    def main_image(self):
        """Retorna la URL de la imagen principal del producto."""
        main_img = next((img for img in self.images if img.is_main), None)
        return main_img.url if main_img else None

    @property
    def image_urls(self):
        """Retorna una lista de todas las URLs de imágenes del producto."""
        return [img.url for img in self.images]

    def to_dict(self):
        """Convierte el producto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'stock': self.stock,
            'material': self.material,
            'color': self.color,
            'dimensions': self.dimensions,
            'main_image': self.main_image,
            'images': self.image_urls,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Product {self.name}>'
