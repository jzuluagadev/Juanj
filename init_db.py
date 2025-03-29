from web import app
from models.product import db, Product, ProductImage
from models.user import User
import os
from werkzeug.security import generate_password_hash


def init_db():
    with app.app_context():
        print("Creando directorio instance si no existe...")
        if not os.path.exists('instance'):
            os.makedirs('instance')
            print("Directorio instance creado")

        print("Inicializando base de datos...")
        db.create_all()
        print("Base de datos inicializada")

        # Crear directorio de imágenes si no existe
        if not os.path.exists('static/img/products'):
            os.makedirs('static/img/products')
            print("Directorio de imágenes creado")

        # Crear usuario administrador si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@zugar.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            print("Usuario administrador creado")

        # Crear productos de ejemplo
        products = [
            {
                'name': 'Collar de Perlas',
                'description': 'Elegante collar de perlas naturales con cierre de oro. Perfecto para ocasiones especiales.',
                'price': 299.99,
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
                'price': 999.99,
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
                'price': 499.99,
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

        # Verificar y crear imágenes de ejemplo si no existen
        example_images = ['joyas1.png', 'joyas2.png', 'joyas3.png']
        for image in example_images:
            image_path = os.path.join('static', 'img', 'products', image)
            if not os.path.exists(image_path):
                print(
                    f"IMPORTANTE: La imagen {image} no existe en static/img/products/")
                print(
                    "Por favor, asegúrate de tener las siguientes imágenes en la carpeta static/img/products/:")
                print("- joyas1.png")
                print("- joyas2.png")
                print("- joyas3.png")
                return

        # Agregar productos a la base de datos
        for product_data in products:
            existing_product = Product.query.filter_by(
                name=product_data['name']).first()
            if not existing_product:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    stock=product_data['stock'],
                    material=product_data['material'],
                    color=product_data['color'],
                    dimensions=product_data['dimensions']
                )
                db.session.add(product)
                db.session.flush()  # Para obtener el ID del producto

                # Agregar imágenes al producto
                for img_data in product_data['images']:
                    image = ProductImage(
                        url=img_data['url'],
                        product_id=product.id,
                        is_main=img_data['is_main']
                    )
                    db.session.add(image)
                print(f"Producto {product_data['name']} creado")

        db.session.commit()
        print("\nBase de datos inicializada con productos de ejemplo")

        if admin:
            print("\nUsuario administrador creado:")
            print("Username: admin")
            print("Password: admin123")


if __name__ == '__main__':
    init_db()
