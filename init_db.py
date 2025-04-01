from web import app
from models.product import db, Product, ProductImage
from models.user import User
from werkzeug.security import generate_password_hash
import os


def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()

        # Verificar si ya existe un usuario administrador
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        # Datos de productos
        products = [
            {
                'name': 'Pulsera Miyuki',
                'description': 'Pulsera elegante con cuentas Miyuki en tonos dorados',
                'price': 89.99,
                'stock': 10,
                'material': 'Cuentas Miyuki',
                'color': 'Dorado',
                'dimensions': '18cm',
                'images': [
                    {'url': 'img/products/joyas1.png', 'is_main': True},
                    {'url': 'img/products/joyas2.png', 'is_main': False},
                    {'url': 'img/products/joyas3.png', 'is_main': False}
                ]
            },
            {
                'name': 'Collar Cristales',
                'description': 'Elegante gargantilla con cristales facetados disponible en tres colores: plateado, negro y blanco',
                'price': 79.99,
                'stock': 15,
                'material': 'Cristales facetados',
                'color': 'Plateado/Negro/Blanco',
                'dimensions': '35cm',
                'images': [
                    {'url': 'img/products/choker1.png.jpg', 'is_main': True},
                    {'url': 'img/products/choker2.png.jpg', 'is_main': False},
                    {'url': 'img/products/choker3.png.jpg', 'is_main': False},
                    {'url': 'img/products/choker4.png.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Pulsera Elegante',
                'description': 'Hermosa pulsera con diseño elegante y moderno',
                'price': 69.99,
                'stock': 12,
                'material': 'Metal y cristales',
                'color': 'Plateado',
                'dimensions': '19cm',
                'images': [
                    {'url': 'img/products/pulsoh1.jpg', 'is_main': True},
                    {'url': 'img/products/pulsoh2.jpg', 'is_main': False},
                    {'url': 'img/products/pulsoh3.jpg', 'is_main': False}
                ]
            }
        ]

        # Crear productos
        for product_data in products:
            product = Product.query.filter_by(
                name=product_data['name']).first()
            if not product:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    stock=product_data['stock'],
                    material=product_data['material'],
                    color=product_data['color'],
                    dimensions=product_data['dimensions'],
                )
                db.session.add(product)
                db.session.flush()  # Para obtener el ID del producto

                # Crear imágenes del producto
                for image_data in product_data['images']:
                    image = ProductImage(
                        url=image_data['url'],
                        product_id=product.id,
                        is_main=image_data['is_main']
                    )
                    db.session.add(image)

        # Guardar cambios
        db.session.commit()


if __name__ == '__main__':
    init_db()
