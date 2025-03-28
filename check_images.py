from web import app
from models.product import Product


def check_image_paths():
    with app.app_context():
        products = Product.query.all()
        print("\nProductos en la base de datos:")
        for product in products:
            print(f"\nNombre: {product.name}")
            print(f"Ruta de imagen: {product.image_url}")
            print(f"Ruta completa: static/{product.image_url}")
            print("-" * 50)


if __name__ == '__main__':
    check_image_paths()
