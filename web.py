# filepath: /c:/Users/usuario/Desktop/Juanj/web.py
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.product import db, Product
from models.user import User
from models.cart import CartItem
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
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
        user = User.query.filter_by(username=request.form.get('username')).first()
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

@app.route('/api/cart')
@login_required
def get_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.to_dict() for item in cart_items])

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
        price=float(data.get('price')),
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
    print(f"Carpeta de imágenes: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True, host='0.0.0.0', port=5000)
    