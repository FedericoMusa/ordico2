from werkzeug.security import generate_password_hash, check_password_hash
from core.usuarios import obtener_usuario_por_email, obtener_usuario_por_nombre, agregar_usuario, obtener_cantidad_usuarios
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def autenticar_usuario(entrada, password):
    """Verifica si las credenciales son correctas. Permite ingresar con nombre o email."""
    usuario = obtener_usuario_por_email(entrada) or obtener_usuario_por_nombre(entrada)

    if usuario:
        hashed_password = usuario[2]  # La contraseña almacenada en la BD
        print(f"🔍 Usuario encontrado: {usuario}")
        print(f"🔍 Hash almacenado en BD: {hashed_password}")
        print(f"🔍 Contraseña ingresada: {password}")

        if check_password_hash(hashed_password, password):
            print(f"✅ Inicio de sesión exitoso para: {entrada}")
            return {
                "username": usuario[1],
                "email": usuario[3],
                "dni": usuario[4],
                "rol": usuario[5]
            }
        else:
            print("❌ Contraseña incorrecta.")
            return None
    else:
        print("❌ Usuario no encontrado.")
        return None
    """Verifica si las credenciales son correctas. Permite ingresar con nombre o email."""
    usuario = obtener_usuario_por_email(entrada) or obtener_usuario_por_nombre(entrada)  # Buscar por email o nombre

    if usuario:
        hashed_password = usuario[2]  # ✅ La contraseña almacenada en la BD está encriptada

        logging.info(f"🔍 Usuario encontrado en la BD: {usuario[1]} ({usuario[3]})")  # Oculta la contraseña del log

        if check_password_hash(hashed_password, password):  # ✅ Comparación segura
            logging.info(f"✅ Inicio de sesión exitoso para: {entrada}")
            return {
                "username": usuario[1], 
                "email": usuario[3], 
                "dni": usuario[4], 
                "rol": usuario[5]
            }
        else:
            logging.warning(f"❌ Intento de inicio de sesión fallido para: {entrada}")
            return None
    else:
        logging.warning(f"❌ Usuario no encontrado con: {entrada}")
        return None

def registrar_usuario(username, password, email, dni, rol="cajero"):
    """Registra un nuevo usuario con validaciones de datos."""
    
    if not username or not password or not email or not dni:
        logging.warning("⚠️ Error: Todos los campos son obligatorios.")
        return "Todos los campos son obligatorios."

    cantidad_usuarios = obtener_cantidad_usuarios()
    logging.info(f"🔍 Cantidad de usuarios en la BD: {cantidad_usuarios}")

    if cantidad_usuarios == 0:
        rol = "admin"

    logging.info(f"🛠 Registrando usuario {username} con rol: {rol}")

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    if agregar_usuario(username, hashed_password, email, dni, rol):
        logging.info(f"✅ Usuario registrado correctamente: {username} con rol {rol}")
        return f"Usuario registrado exitosamente como {rol}."
    else:
        logging.warning(f"⚠️ Error: Usuario '{username}', email '{email}' o DNI '{dni}' ya existen.")
        return "El nombre de usuario, el email o el DNI ya existen."
