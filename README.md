# ZUGAR - Tienda de Joyas y Accesorios

Sitio web de comercio electrónico para la venta de joyas y accesorios.

## Características

- Catálogo de productos con diseño horizontal
- Sistema de carrito de compras
- Panel de administración
- Autenticación de usuarios
- Diseño responsive
- Base de datos SQLite

## Requisitos

- Python 3.8 o superior
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/zugar.git
cd zugar
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializar la base de datos:
```bash
python init_db.py
```

5. Ejecutar la aplicación:
```bash
python web.py
```

## Acceso

- Sitio web: http://localhost:5000
- Panel de administración: http://localhost:5000/admin
  - Usuario: admin
  - Contraseña: admin123

## Estructura del Proyecto

```
zugar/
├── instance/           # Base de datos SQLite
├── models/            # Modelos de la base de datos
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── templates/         # Plantillas HTML
├── web.py            # Aplicación principal
├── config.py         # Configuración
├── init_db.py        # Script de inicialización
└── requirements.txt  # Dependencias
```

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 