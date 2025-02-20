import re
import random
import string

def validar_email(email):
    """
    Verifica si el email tiene un formato válido usando una expresión regular.
    """
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.match(regex, email) is not None

def generar_codigo_verificacion(longitud=6):
    """
    Genera un código de verificación aleatorio compuesto por letras y números.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def generar_nueva_contrasena(longitud=8):
    """
    Genera una nueva contraseña aleatoria de una longitud específica.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))
