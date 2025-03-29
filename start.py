import os
import subprocess
from backup_simple import restore_images


def start_project():
    print("Iniciando proyecto ZUGAR...")

    # Restaurar imágenes
    print("\nRestaurando imágenes...")
    restore_images()

    # Inicializar base de datos
    print("\nInicializando base de datos...")
    subprocess.run(['python', 'init_db.py'])

    # Iniciar servidor web
    print("\nIniciando servidor web...")
    subprocess.run(['python', 'web.py'])


if __name__ == '__main__':
    start_project()
