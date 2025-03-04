import sqlite3
import logging
import pandas as pd
from utils.config import DB_PATH  # ✅ Usa configuración centralizada

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def conectar_db():
    """Establece una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        logging.error(f"❌ Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    """Crea las tablas necesarias en la base de datos si no existen."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')
            # Tabla de productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            conn.commit()
            logging.info("✅ Base de datos inicializada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"❌ Error al inicializar la base de datos: {e}")
        finally:
            conn.close()

### **🔹 Funciones para manejar usuarios**
def agregar_usuario(nombre, password, email, dni, rol):
    """Inserta un nuevo usuario en la base de datos."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, password, email, dni, rol) VALUES (?, ?, ?, ?, ?)",
                       (nombre, password, email, dni, rol))
        conn.commit()
        logging.info(f"✅ Usuario registrado correctamente: {nombre} con rol {rol}")
        return True
    except sqlite3.IntegrityError as e:
        logging.warning(f"⚠️ Error: {e}")
        return False
    except sqlite3.Error as e:
        logging.error(f"❌ Error al agregar usuario: {e}")
        return False
    finally:
        conn.close()
def obtener_usuarios() -> list[tuple]:
    """Obtiene la lista de usuarios desde la base de datos."""
    conn = conectar_db()
    if conn is None:
        logging.error("❌ No se pudo establecer conexión con la base de datos.")
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener usuarios: {e}")
        return []
    finally:
        conn.close()

def obtener_usuario_por_dni(dni):
    """Obtiene un usuario por su número de DNI."""
    conn = conectar_db()
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

def obtener_usuario_por_nombre(nombre):
    """Obtiene un usuario por su nombre de usuario."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por nombre '{nombre}': {e}")
            return None
        finally:
            conn.close()
def obtener_usuario_por_email(email):
    """Obtiene un usuario por su correo electrónico."""
    conn = conectar_db()
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

def eliminar_usuario(id_usuario):
    """Elimina un usuario por su ID."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            logging.info(f"✅ Usuario con ID {id_usuario} eliminado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al eliminar usuario con ID '{id_usuario}': {e}")
            return False
        finally:
            conn.close()

def actualizar_password(email, nueva_password):
    """Actualiza la contraseña de un usuario dado su correo electrónico."""
    conn = conectar_db()
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

def actualizar_rol_usuario(id_usuario, nuevo_rol):
    """Actualiza el rol de un usuario en la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, id_usuario))
            conn.commit()
            logging.info(f"✅ Rol actualizado para usuario ID {id_usuario}: {nuevo_rol}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar rol para usuario ID {id_usuario}: {e}")
            return False
        finally:
            conn.close()
def obtener_cantidad_usuarios():
    """Obtiene la cantidad de usuarios en la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener cantidad de usuarios: {e}")
            return 0
        finally:
            conn.close()

### **🔹 Funciones para manejar productos**

def obtener_productos():
    """Obtiene la lista de productos desde la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener productos: {e}")
            return []
        finally:
            conn.close()

def agregar_producto(nombre, cantidad, precio):
    """Agrega un nuevo producto a la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
            conn.commit()
            logging.info(f"✅ Producto agregado: {nombre}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al agregar producto: {e}")
            return False
        finally:
            conn.close()

def actualizar_producto(id_producto, nombre, cantidad, precio):
    """Actualiza un producto en la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?", (nombre, cantidad, precio, id_producto))
            conn.commit()
            logging.info(f"✅ Producto con ID {id_producto} actualizado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar producto: {e}")
            return False
        finally:
            conn.close()

def eliminar_producto(id_producto):
    """Elimina un producto de la base de datos."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conn.commit()
            logging.info(f"✅ Producto con ID {id_producto} eliminado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al eliminar producto: {e}")
            return False
        finally:
            conn.close()

def obtener_producto_por_id(id_producto):
    """Obtiene un producto por su ID."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener producto por ID '{id_producto}': {e}")
            return None
        finally:
            conn.close()

def obtener_cantidad_productos():
    """Obtiene la cantidad total de productos registrados."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos")
            cantidad = cursor.fetchone()[0]
            return cantidad
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener cantidad de productos: {e}")
            return 0
        finally:
            conn.close()

def importar_desde_excel(archivo):
    """Importa productos desde un archivo Excel y los guarda en la base de datos."""
    try:
        df = pd.read_excel(archivo)

        # Verificar que el archivo tenga las columnas esperadas
        columnas_esperadas = {"Nombre", "Cantidad", "Precio"}
        if not columnas_esperadas.issubset(df.columns):
            logging.error("❌ El archivo Excel no tiene las columnas necesarias.")
            return False

        conn = conectar_db()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            nombre = row["Nombre"]
            cantidad = int(row["Cantidad"])
            precio = float(row["Precio"])
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))

        conn.commit()
        conn.close()
        logging.info("✅ Productos importados desde Excel correctamente.")
        return True
    except Exception as e:
        logging.error(f"❌ Error al importar productos desde Excel: {e}")
        return False
