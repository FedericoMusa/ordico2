import sqlite3
import logging
from utils.config import DB_PATH  # ✅ Usa configuración centralizada

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def conectar():
    """Establece una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        logging.error(f"❌ Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    """Crea la tabla de usuarios si no existe."""
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')
            conn.commit()
            logging.info("✅ Base de datos inicializada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"❌ Error al inicializar la base de datos: {e}")
        finally:
            conn.close()

def agregar_usuario(username, password, email, dni, rol):
    """Agrega un usuario a la base de datos con email y DNI."""  
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, email, dni, rol) VALUES (?, ?, ?, ?, ?)",
                           (username, password, email, dni, rol))
            conn.commit()
            logging.info(f"✅ Usuario registrado: {username}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"⚠️ Error: El usuario '{username}', email '{email}' o DNI '{dni}' ya existen.")
            return False
        except sqlite3.Error as e:
            logging.error(f"❌ Error al agregar usuario: {e}")
            return False
        finally:
            conn.close()

def obtener_usuario_por_email(email):
    """Obtiene un usuario por su correo electrónico."""
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por email '{email}': {e}")
            return None
        finally:
            conn.close()

def obtener_usuario_por_dni(dni):
    """Obtiene un usuario por su número de DNI."""  # ✅ Ahora está definida correctamente
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE dni = ?", (dni,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por DNI '{dni}': {e}")
            return None
        finally:
            conn.close()
def obtener_usuario_por_username(username):
    """Obtiene un usuario por su nombre de usuario."""  # ✅ Ahora está definida correctamente
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por username '{username}': {e}")
            return None
        finally:
            conn.close()
def actualizar_password(email, nueva_password):
    """Actualiza la contraseña de un usuario dado su correo electrónico."""
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET password = ? WHERE email = ?", (nueva_password, email))
            conn.commit()
            logging.info(f"✅ Contraseña actualizada para el usuario con email: {email}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar contraseña para '{email}': {e}")
            return False
        finally:
            conn.close()

def eliminar_usuario(username):
    """Elimina un usuario de la base de datos."""
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
            conn.commit()
            logging.info(f"✅ Usuario eliminado: {username}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al eliminar usuario '{username}': {e}")
            return False
        finally:
            conn.close()

