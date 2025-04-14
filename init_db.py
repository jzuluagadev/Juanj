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
                'name': 'Pulsera M',
                'description': 'Pulsera M',
                'price': 29.99,
                'stock': 12,
                'material': 'Metal y cristales',
                'color': 'Plateado',
                'dimensions': 'Ajustable, aproximadamente 18cm',
                'images': [
                    {'url': 'img/products/pulseraM1.jpg', 'is_main': True},
                    {'url': 'img/products/pulseraM2.jpg', 'is_main': False},
                    {'url': 'img/products/pulseraM3.jpg', 'is_main': False},
                    {'url': 'img/products/pulseraM4.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Aretes Maxi',
                'description': 'Maxiaretes',
                'price': 34.99,
                'stock': 15,
                'material': 'Metal bañado en oro',
                'color': 'Dorado',
                'dimensions': 'Largo: 8cm',
                'images': [
                    {'url': 'img/products/maxi1.jpg', 'is_main': True},
                    {'url': 'img/products/maxi2.jpg', 'is_main': False},
                    {'url': 'img/products/maxi3.jpg', 'is_main': False},
                    {'url': 'img/products/maxi4.jpg', 'is_main': False},
                    {'url': 'img/products/maxi5.jpg', 'is_main': False},
                    {'url': 'img/products/maxi6.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Pulsera Miyuki',
                'description': 'Hermosa pulsera hecha con cuentas Miyuki de alta calidad. Perfecta para cualquier ocasión.',
                'price': 29.99,
                'stock': 10,
                'material': 'Cuentas Miyuki, hilo elástico',
                'color': 'Dorado',
                'dimensions': 'Ajustable, aproximadamente 18cm',
                'images': [
                    {'url': 'img/products/pulsoh1.jpg', 'is_main': True},
                    {'url': 'img/products/pulsoh2.jpg', 'is_main': False},
                    {'url': 'img/products/pulsoh3.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Choker Elegante',
                'description': 'Choker elegante con diseño minimalista. Ideal para eventos especiales.',
                'price': 24.99,
                'stock': 15,
                'material': 'Tela satinada, broche ajustable',
                'color': 'Negro',
                'dimensions': 'Ajustable, 35-40cm',
                'images': [
                    {'url': 'img/products/choker1.png.jpg', 'is_main': True},
                    {'url': 'img/products/choker2.png.jpg', 'is_main': False},
                    {'url': 'img/products/choker3.png.jpg', 'is_main': False},
                    {'url': 'img/products/choker4.png.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Topo Decorativo',
                'description': 'Topo decorativo con diseño único. Perfecto para complementar cualquier atuendo.',
                'price': 19.99,
                'stock': 20,
                'material': 'Metal, cristales',
                'color': 'Plateado',
                'dimensions': '3cm x 2cm',
                'images': [
                    {'url': 'img/products/topo1.jpg', 'is_main': True},
                    {'url': 'img/products/topo2.jpg', 'is_main': False},
                    {'url': 'img/products/topo3.jpg', 'is_main': False},
                    {'url': 'img/products/topo4.jpg', 'is_main': False},
                    {'url': 'img/products/topo5.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Conjunto de Plata',
                'description': 'Elegante conjunto de joyas en plata con diseño moderno y minimalista.',
                'price': 49.99,
                'stock': 8,
                'material': 'Plata 925',
                'color': 'Plateado',
                'dimensions': 'Collar: 40cm, Pulsera: 17cm',
                'images': [
                    {'url': 'img/products/plata1.jpg', 'is_main': True},
                    {'url': 'img/products/plata2.jpg', 'is_main': False},
                    {'url': 'img/products/plata3.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Conjunto de Corazones',
                'description': 'Hermoso conjunto de joyas con motivos de corazones. Perfecto para regalar o usar en ocasiones especiales.',
                'price': 34.99,
                'stock': 15,
                'material': 'Metal bañado en plata',
                'color': 'Plateado',
                'dimensions': 'Collar: 42cm, Pulsera: 18cm',
                'images': [
                    {'url': 'img/products/corazon1.jpg', 'is_main': True},
                    {'url': 'img/products/corazon2.jpg', 'is_main': False},
                    {'url': 'img/products/corazon3.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Set de Búho en Miyuki',
                'description': 'Encantador conjunto de joyas con motivos de búho elaborado con cuentas Miyuki. Perfecto para amantes de la naturaleza y la moda.',
                'price': 32.99,
                'stock': 12,
                'material': 'Cuentas Miyuki, hilo elástico',
                'color': 'Multicolor',
                'dimensions': 'Collar: 40cm, Pulsera: 18cm',
                'images': [
                    {'url': 'img/products/buho1.jpg', 'is_main': True},
                    {'url': 'img/products/buho2.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Pulsera Tejida en Cristales',
                'description': 'Pulsera tejida en cristales de miyuki con diseño elegante y moderno. Perfecta para complementar cualquier atuendo.',
                'price': 27.99,
                'stock': 15,
                'material': 'Cristales Miyuki, hilo elástico',
                'color': 'Multicolor',
                'dimensions': 'Ajustable, aproximadamente 18cm',
                'images': [
                    {'url': 'img/products/pulsera1.jpg', 'is_main': True},
                    {'url': 'img/products/pulsera2.jpg', 'is_main': False},
                    {'url': 'img/products/pulsera3.jpg', 'is_main': False}
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
