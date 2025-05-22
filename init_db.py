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
                'name': 'Collar Cristales',
                'description': 'Elegante gargantilla con cristales facetados disponible en tres colores: plateado, negro y blanco',
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
                'stock': 12,
                'material': 'Metal y cristales',
                'color': 'Plateado',
                'dimensions': '19cm',
                'images': [
                    {'url': 'img/products/pulsoh1.jpg', 'is_main': True},
                    {'url': 'img/products/pulsoh2.jpg', 'is_main': False},
                    {'url': 'img/products/pulsoh3.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Broche Elegante',
                'description': 'Hermoso broche con diseño elegante y moderno, perfecto para complementar cualquier atuendo. Fabricado con materiales de alta calidad y detalles delicados.',
                'stock': 8,
                'material': 'Metal y cristales',
                'color': 'Plateado y dorado',
                'dimensions': '4cm x 3cm',
                'images': [
                    {'url': 'img/products/topo1.jpg', 'is_main': True},
                    {'url': 'img/products/topo2.jpg', 'is_main': False},
                    {'url': 'img/products/topo3.jpg', 'is_main': False},
                    {'url': 'img/products/topo4.jpg', 'is_main': False},
                    {'url': 'img/products/topo5.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Pulsera M',
                'description': 'Pulsera M',
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
                'name': 'Conjunto de Plata',
                'description': 'Elegante conjunto de joyas en plata con diseño moderno y minimalista.',
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
                'stock': 15,
                'material': 'Cristales Miyuki, hilo elástico',
                'color': 'Multicolor',
                'dimensions': 'Ajustable, aproximadamente 18cm',
                'images': [
                    {'url': 'img/products/pulsera1.jpg', 'is_main': True},
                    {'url': 'img/products/pulsera2.jpg', 'is_main': False},
                    {'url': 'img/products/pulsera3.jpg', 'is_main': False}
                ]
            },
            {
                'name': 'Collar de Perlas',
                'description': 'Elegante collar de perlas naturales con cierre de oro. Perfecto para ocasiones especiales.',
                'stock': 10,
                'material': 'Perlas naturales, Oro 14k',
                'color': 'Blanco, Dorado',
                'dimensions': '45cm de largo',
                'images': [
                    {'url': 'img/products/joyas1.png', 'is_main': True},
                    {'url': 'img/products/joyas2.png', 'is_main': False},
                    {'url': 'img/products/joyas3.png', 'is_main': False}
                ]
            },
            {
                'name': 'Anillo de Diamante',
                'description': 'Hermoso anillo de compromiso con diamante central y detalles en oro blanco.',
                'stock': 5,
                'material': 'Diamante, Oro blanco 18k',
                'color': 'Transparente, Blanco',
                'dimensions': 'Talla 6-10',
                'images': [
                    {'url': 'img/products/joyas2.png', 'is_main': True},
                    {'url': 'img/products/joyas1.png', 'is_main': False},
                    {'url': 'img/products/joyas3.png', 'is_main': False}
                ]
            },
            {
                'name': 'Pulsera de Oro',
                'description': 'Pulsera de oro amarillo con diseño moderno y elegante.',
                'stock': 8,
                'material': 'Oro amarillo 14k',
                'color': 'Dorado',
                'dimensions': '18cm de largo',
                'images': [
                    {'url': 'img/products/joyas3.png', 'is_main': True},
                    {'url': 'img/products/joyas1.png', 'is_main': False},
                    {'url': 'img/products/joyas2.png', 'is_main': False}
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
