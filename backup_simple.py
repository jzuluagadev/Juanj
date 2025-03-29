import os
import shutil
from datetime import datetime


def backup_images():
    # Crear directorio de respaldo si no existe
    backup_dir = 'backup_images'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Directorio de respaldo '{backup_dir}' creado")

    # Crear subdirectorio con fecha
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, date_str)
    os.makedirs(backup_path)
    print(f"Creando respaldo en: {backup_path}")

    # Copiar imágenes
    source_dir = 'static/img/products'
    if os.path.exists(source_dir):
        for file in os.listdir(source_dir):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                source_file = os.path.join(source_dir, file)
                dest_file = os.path.join(backup_path, file)
                shutil.copy2(source_file, dest_file)
                print(f"Imagen respaldada: {file}")
    else:
        print(f"Directorio de origen '{source_dir}' no encontrado")


def restore_images():
    backup_dir = 'backup_images'
    if not os.path.exists(backup_dir):
        print("No se encontró el directorio de respaldo")
        return

    # Obtener el respaldo más reciente
    backups = sorted([d for d in os.listdir(backup_dir)
                     if os.path.isdir(os.path.join(backup_dir, d))])
    if not backups:
        print("No se encontraron respaldos")
        return

    latest_backup = backups[-1]
    backup_path = os.path.join(backup_dir, latest_backup)
    print(f"Restaurando desde: {backup_path}")

    # Crear directorio de destino si no existe
    dest_dir = 'static/img/products'
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Directorio de destino '{dest_dir}' creado")

    # Copiar imágenes
    for file in os.listdir(backup_path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            source_file = os.path.join(backup_path, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(source_file, dest_file)
            print(f"Imagen restaurada: {file}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_images()
    else:
        backup_images()
