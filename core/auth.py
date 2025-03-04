from werkzeug.security import generate_password_hash, check_password_hash
from core.database import obtener_usuario_por_email, obtener_usuario_por_nombre, agregar_usuario, obtener_cantidad_usuarios  # ✅ Importación correcta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def autenticar_usuario(entrada, password):
    """Verifica si las credenciales son correctas. Permite ingresar con nombre o email."""
    usuario = obtener_usuario_por_email(entrada)  # Buscar por email
    if not usuario:
        usuario = obtener_usuario_por_nombre(entrada)  # Buscar por nombre

    if usuario:
        hashed_password = usuario[2]  # ✅ La contraseña almacenada en la BD está encriptada

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

def registrar_usuario(username, password, email, dni, rol="cajero"):
    """Registra un nuevo usuario con rol seleccionado o por defecto."""
    cantidad_usuarios = obtener_cantidad_usuarios()
    logging.info(f"🔍 Cantidad de usuarios en la BD: {cantidad_usuarios}")

    if cantidad_usuarios == 0:
        rol = "admin"

    print(f"🛠 Registrando usuario {username} con rol: {rol}")

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    if agregar_usuario(username, hashed_password, email, dni, rol):
        logging.info(f"✅ Usuario registrado correctamente: {username} con rol {rol}")
        return f"Usuario registrado exitosamente como {rol}."
    else:
        logging.warning(f"⚠️ Error: Usuario '{username}', email '{email}' o DNI '{dni}' ya existen.")
        return "El nombre de usuario, el email o el DNI ya existen."
