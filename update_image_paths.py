from web import app
from models.product import Product, db


def update_image_paths():
    with app.app_context():
        products = Product.query.all()
        for product in products:
            if product.image_url.startswith('images/'):
                product.image_url = product.image_url.replace(
                    'images/', 'img/products/')
        db.session.commit()
        print("Rutas de imágenes actualizadas")


if __name__ == '__main__':
    update_image_paths()
