from web import app
from models.product import db, Product
from models.user import User
import os
import shutil


def init_db():
    with app.app_context():
        print("Creando directorio instance si no existe...")
        if not os.path.exists('instance'):
            os.makedirs('instance')
            print("Directorio instance creado")

        print("Inicializando base de datos...")
        db.create_all()
        print("Base de datos inicializada")

        # Crear usuario administrador
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@zugar.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Usuario administrador creado")

        # Crear productos de ejemplo
        products = [
            Product(
                name='Collar de Perlas',
                description='Hermoso collar de perlas naturales con cierre de oro',
                price=299.99,
                image_url='img/products/joyas1.png',
                category='Collares',
                stock=10
            ),
            Product(
                name='Anillo de Diamante',
                description='Anillo de compromiso con diamante central',
                price=999.99,
                image_url='img/products/joyas1.png',
                category='Anillos',
                stock=5
            ),
            Product(
                name='Pulsera de Oro',
                description='Pulsera de oro 14k con diseño moderno',
                price=799.99,
                image_url='img/products/joyas1.png',
                category='Pulseras',
                stock=8
            )
        ]

        for product in products:
            if not Product.query.filter_by(name=product.name).first():
                db.session.add(product)
                print(f"Producto {product.name} creado")

        db.session.commit()
        print("Base de datos inicializada con productos de ejemplo")
        print("Usuario administrador creado:")
        print("Username: admin")
        print("Password: admin123")


if __name__ == '__main__':
    init_db()
