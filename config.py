"""
Configuración de la aplicación de la tienda de joyería.
Define las variables de entorno y configuraciones necesarias.
"""

import os
from datetime import timedelta


class Config:
    """Clase de configuración principal."""
    # Configuración básica
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///zugar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    UPLOAD_FOLDER = os.path.join('static', 'img', 'products')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
