"""
Modelo de Usuario para la tienda de joyería.
Maneja la autenticación y roles de usuarios.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.product import db


class User(UserMixin, db.Model):
    """Modelo de Usuario con autenticación y roles."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Establece la contraseña hasheada del usuario."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
