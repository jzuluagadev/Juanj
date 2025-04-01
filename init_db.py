from web import app
from models.product import db, Product, ProductImage
from models.user import User
from werkzeug.security import generate_password_hash
import os


def init_db():
    # Crear el directorio instance si no existe
    if not os.path.exists('instance'):
        os.makedirs('instance')

    with app.app_context():
        # Crear todas las tablas
        db.create_all()

        # Crear usuario administrador
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)

        # Datos de productos
        products_data = [
            {
                'name': 'Pulsera Miyuki',
                'description': 'Hermosa pulsera elaborada con cuentas Miyuki de alta calidad',
                'price': 89.99,
                'stock': 10,
                'material': 'Cuentas Miyuki',
                'color': 'Multicolor',
                'dimensions': '18cm ajustable',
                'images': [
                    {'url': 'img/products/joyas1.png', 'is_main': True},
                    {'url': 'img/products/joyas2.png', 'is_main': False},
                    {'url': 'img/products/joyas3.png', 'is_main': False}
                ]
            }
        ]

        # Crear productos
        for product_data in products_data:
            product = Product.query.filter_by(
                name=product_data['name']).first()
            if not product:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    stock=product_data.get('stock', 0),
                    material=product_data.get('material', ''),
                    color=product_data.get('color', ''),
                    dimensions=product_data.get('dimensions', '')
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
