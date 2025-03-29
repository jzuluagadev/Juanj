# ZUGAR - Tienda de Joyería

Sitio web de comercio electrónico para una tienda de joyería, desarrollado con Flask.

## Características

- Catálogo de productos con imágenes múltiples
- Carrusel de imágenes por producto
- Sistema de carrito de compras
- Diseño responsive y moderno
- Integración con WhatsApp
- Panel de administración
- Sistema de respaldo automático de imágenes

## Requisitos

- Python 3.8 o superior
- Flask
- SQLite
- Otros requisitos en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/zugar.git
cd zugar
```

2. Crear entorno virtual:
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

5. Iniciar el servidor:
```bash
python web.py
```

## Uso

- Acceder a la tienda: http://localhost:5000
- Panel de administración: http://localhost:5000/admin
  - Usuario: admin
  - Contraseña: admin123

## Estructura del Proyecto

```
zugar/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/
├── models/
├── instance/
├── backup_images/
├── web.py
├── init_db.py
└── requirements.txt
```

## Licencia

Este proyecto está bajo la Licencia MIT. 