# filepath: /c:/Users/usuario/Desktop/Juanj/web.py
"""
Aplicación principal de la tienda de joyería Zugar.
Maneja las rutas, autenticación y operaciones CRUD de productos.
"""

# Importaciones de Flask y extensiones
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

# Importaciones de modelos
from models.product import db, Product
from models.user import User
from models.cart import CartItem

# Importaciones de configuración y utilidades
from config import Config
import os
from datetime import timedelta

# Inicialización de la aplicación
app = Flask(__name__)
app.config.from_object(Config)

# Configuración de seguridad
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Inicialización de extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Crear las tablas de la base de datos
with app.app_context():
    print("Creando directorio instance si no existe...")
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("Directorio instance creado")

    print("Inicializando base de datos...")
    db.create_all()
    print("Base de datos inicializada")

# Rutas principales


@app.route('/')
def home():
    print("Accediendo a la página principal...")
    try:
        products = Product.query.all()
        print(f"Productos encontrados: {len(products)}")
        return render_template('index.html', products=products)
    except Exception as e:
        print(f"Error en la página principal: {str(e)}")
        return str(e), 500


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Rutas de autenticación


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('home'))
        flash('Usuario o contraseña incorrectos')
    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Rutas de API


@app.route('/api/products')
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


@app.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({'error': 'Stock insuficiente'}), 400

    cart_item = CartItem(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity
    )
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': 'Producto agregado al carrito'})


@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'Producto eliminado del carrito'})


@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json()
    quantity = data.get('quantity', 1)

    if quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()

    return jsonify({'message': 'Carrito actualizado'})


@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': item.id,
        'product': item.product.to_dict(),
        'quantity': item.quantity
    } for item in cart_items])

# Rutas de administración


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)


@app.route('/api/admin/products', methods=['POST'])
@login_required
def create_product():
    if not current_user.is_admin:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.form
    image = request.files.get('image')

    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = f'img/products/{filename}'
    else:
        image_url = data.get('image_url')

    product = Product(
        name=data.get('name'),
        description=data.get('description'),
        image_url=image_url,
        category=data.get('category'),
        stock=int(data.get('stock'))
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict())


@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        return jsonify({'error': 'No autorizado'}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    print("Iniciando servidor web...")
    print(f"Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Carpeta de imágenes: {os.path.abspath('static/img/products')}")
    app.run(debug=True, host='0.0.0.0')
