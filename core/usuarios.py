import sqlite3
import logging
from core.database import conectar_db  # Importamos la conexión a la BD

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def agregar_usuario(nombre, password, email, dni, rol):
    """Inserta un nuevo usuario en la base de datos."""
    if not nombre or not password or not email or not dni:
        logging.warning("⚠️ Error: Todos los campos son obligatorios para registrar un usuario.")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nombre, password, email, dni, rol) 
                VALUES (?, ?, ?, ?, ?)
            """, (nombre.strip(), password, email.strip().lower(), dni.strip(), rol.strip()))
            conn.commit()
            logging.info(f"✅ Usuario agregado: {nombre} - Rol: {rol}")
            return True
    except sqlite3.IntegrityError:
        logging.warning(f"⚠️ El usuario '{nombre}' ya existe en la base de datos.")
        return False
    except sqlite3.Error as e:
        logging.error(f"❌ Error al agregar usuario: {e}")
        return False

def obtener_usuarios():
    """Obtiene la lista de todos los usuarios."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, email, dni, rol FROM usuarios")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener usuarios: {e}")
        return []

def obtener_usuario_por_dni(dni):
    """Obtiene un usuario por su DNI."""
    if not dni:
        logging.warning("⚠️ DNI inválido para la búsqueda.")
        return None

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, password, email, dni, rol FROM usuarios WHERE dni = ?", (dni.strip(),))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener usuario por DNI {dni}: {e}")
        return None

def obtener_usuario_por_nombre(nombre):
    """Obtiene un usuario por su nombre de usuario."""
    if not nombre:
        logging.warning("⚠️ Nombre inválido para la búsqueda.")
        return None

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, password, email, dni, rol FROM usuarios WHERE nombre = ?", (nombre.strip(),))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener usuario por nombre '{nombre}': {e}")
        return None

def obtener_usuario_por_email(email):
    """Obtiene un usuario por su correo electrónico."""
    if not email:
        logging.warning("⚠️ Email inválido para la búsqueda.")
        return None

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, password, email, dni, rol 
                FROM usuarios 
                WHERE email = ?
            """, (email.strip().lower(),))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener usuario por email '{email}': {e}")
        return None

def eliminar_usuario(id_usuario):
    """Elimina un usuario por su ID."""
    if not id_usuario:
        logging.warning("⚠️ ID de usuario inválido para la eliminación.")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            if cursor.rowcount == 0:
                logging.warning(f"⚠️ No se encontró el usuario con ID {id_usuario}.")
                return False
            conn.commit()
            logging.info(f"✅ Usuario con ID {id_usuario} eliminado correctamente.")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al eliminar usuario con ID '{id_usuario}': {e}")
        return False

def actualizar_password(email, nueva_password):
    """Actualiza la contraseña de un usuario dado su correo electrónico."""
    if not email or not nueva_password:
        logging.warning("⚠️ Email y nueva contraseña son obligatorios.")
        return False

    usuario = obtener_usuario_por_email(email)
    if not usuario:
        logging.warning(f"⚠️ No se encontró el usuario con email: {email}")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET password = ? WHERE email = ?", (nueva_password, email.strip().lower()))
            conn.commit()
            logging.info(f"✅ Contraseña actualizada para el usuario con email: {email}")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al actualizar contraseña para '{email}': {e}")
        return False

def actualizar_rol_usuario(id_usuario, nuevo_rol):
    """Actualiza el rol de un usuario en la base de datos."""
    if not id_usuario or not nuevo_rol:
        logging.warning("⚠️ ID de usuario y nuevo rol son obligatorios.")
        return False

    usuario = obtener_usuario_por_dni(id_usuario)
    if not usuario:
        logging.warning(f"⚠️ No se encontró el usuario con ID: {id_usuario}")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol.strip(), id_usuario))
            conn.commit()
            logging.info(f"✅ Rol actualizado para usuario ID {id_usuario}: {nuevo_rol}")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al actualizar rol para usuario ID {id_usuario}: {e}")
        return False

def obtener_cantidad_usuarios():
    """Obtiene la cantidad total de usuarios en la base de datos."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            cantidad = cursor.fetchone()[0]
            return cantidad
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener cantidad de usuarios: {e}")
        return 0
