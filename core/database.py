import sqlite3
import logging
import pandas as pd
from utils.config import DB_PATH  # ✅ Ruta centralizada de la BD

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def conectar_db():
    """Devuelve una conexión a la base de datos utilizando un gestor de contexto."""
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        logging.error(f"❌ Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    """Crea las tablas necesarias en la base de datos si no existen."""
    with conectar_db() as conn:
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
                cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
                precio REAL NOT NULL CHECK (precio >= 0)
            )
        ''')
        conn.commit()
        logging.info("✅ Base de datos inicializada correctamente.")

### **🔹 Funciones para manejar productos**
def obtener_productos():
    """Obtiene la lista de productos desde la base de datos."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener productos: {e}")
        return []

def agregar_producto(nombre, categoria, cantidad, precio):
    """Agrega un producto a la base de datos con la nueva columna de categoría."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
                           (nombre, categoria, cantidad, precio))
            conn.commit()
            logging.info(f"✅ Producto agregado: {nombre} - Categoría: {categoria} - Cantidad: {cantidad} - Precio: {precio}")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al agregar producto: {e}")
        return False

def actualizar_producto(id_producto, nombre, cantidad, precio):
    """Actualiza un producto en la base de datos."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?", 
                           (nombre, cantidad, precio, id_producto))
            conn.commit()
            logging.info(f"✅ Producto actualizado - ID: {id_producto}, Nombre: {nombre}, Cantidad: {cantidad}, Precio: {precio}")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al actualizar producto: {e}")
        return False

def eliminar_producto(id_producto):
    """Elimina un producto de la base de datos."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conn.commit()
            logging.info(f"✅ Producto eliminado - ID: {id_producto}")
            return True
    except sqlite3.Error as e:
        logging.error(f"❌ Error al eliminar producto: {e}")
        return False

def obtener_producto_por_id(id_producto):
    """Obtiene un producto por su ID."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener producto por ID '{id_producto}': {e}")
        return None

def obtener_cantidad_productos():
    """Obtiene la cantidad total de productos registrados."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos")
            cantidad = cursor.fetchone()[0]
            return cantidad
    except sqlite3.Error as e:
        logging.error(f"❌ Error al obtener cantidad de productos: {e}")
        return 0

def importar_desde_excel(archivo):
    """Importa productos desde un archivo Excel y los guarda en la base de datos."""
    try:
        df = pd.read_excel(archivo)

        # Verificar que el archivo tenga las columnas esperadas
        columnas_esperadas = {"Nombre", "Cantidad", "Precio"}
        if not columnas_esperadas.issubset(df.columns):
            logging.error("❌ El archivo Excel no tiene las columnas necesarias: 'Nombre', 'Cantidad', 'Precio'.")
            return False

        with conectar_db() as conn:
            cursor = conn.cursor()

            for _, row in df.iterrows():
                nombre = str(row["Nombre"]).title().strip()  # Normalizar nombre
                cantidad = int(row["Cantidad"]) if pd.notna(row["Cantidad"]) else 0
                precio = float(row["Precio"]) if pd.notna(row["Precio"]) else 0.0

                # Validaciones
                if cantidad < 0 or precio < 0:
                    logging.warning(f"⚠️ Datos inválidos para {nombre}: cantidad y precio deben ser positivos.")
                    continue

                # Insertar o actualizar productos
                cursor.execute("""
                    INSERT INTO productos (nombre, cantidad, precio)
                    VALUES (?, ?, ?)
                    ON CONFLICT(nombre) DO UPDATE SET cantidad = cantidad + ?, precio = ?
                """, (nombre, cantidad, precio, cantidad, precio))

            conn.commit()
        logging.info("✅ Productos importados desde Excel correctamente.")
        return True
    except Exception as e:
        logging.error(f"❌ Error al importar productos desde Excel: {e}")
        return False
