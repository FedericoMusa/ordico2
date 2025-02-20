from werkzeug.security import generate_password_hash, check_password_hash
from core.database import obtener_usuario_por_email, obtener_usuario_por_username, agregar_usuario
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def autenticar_usuario(entrada, password):
    """Verifica si las credenciales de un usuario son correctas.
       Permite ingresar con email o username.
    """
    usuario = obtener_usuario_por_email(entrada)  # Intenta buscar por email

    if not usuario:
        usuario = obtener_usuario_por_username(entrada)  # Si no encuentra, busca por username

    if usuario:
        hashed_password = usuario[2]  # ✅ La contraseña almacenada en la BD está encriptada

        # 🔴 Agregar depuración para ver qué se está comparando
        logging.info(f"🔍 Usuario encontrado en la BD: {usuario}")
        logging.info(f"🔍 Contraseña ingresada: {password}")
        logging.info(f"🔍 Hash en la BD: {hashed_password}")

        if check_password_hash(hashed_password, password):  # ✅ Compara correctamente
            logging.info(f"✅ Inicio de sesión exitoso para: {entrada}")
            return {
                "username": usuario[1], 
                "email": usuario[3], 
                "dni": usuario[4], 
                "rol": usuario[5]
            }
        else:
            logging.warning(f"❌ Contraseña incorrecta para: {entrada}")
            return None
    else:
        logging.warning(f"❌ Usuario no encontrado con: {entrada}")
        return None

def registrar_usuario(username, password, email, dni, rol):
    """Registra un nuevo usuario con email y DNI."""
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)  # ✅ Encripta la contraseña

    if agregar_usuario(username, hashed_password, email, dni, rol):
        logging.info(f"✅ Usuario registrado correctamente: {username}")
        return "Usuario registrado exitosamente."
    else:
        logging.warning(f"⚠️ Error: Usuario '{username}', email '{email}' o DNI '{dni}' ya existen.")
        return "El nombre de usuario, el email o el DNI ya existen."
