import sys
import logging
from PyQt5.QtWidgets import QApplication
from gui.login import LoginDialog
from gui.main_window import MainWindow  # ✅ Importamos la ventana principal
from core.database import inicializar_db

# Configurar logging para seguimiento de eventos en la aplicación
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    """Punto de entrada de la aplicación."""
    try:
        logging.info("✅ Inicializando la base de datos...")
        inicializar_db()  # Asegura que la base de datos existe antes de arrancar

        logging.info("✅ Creando la aplicación PyQt5...")
        app = QApplication(sys.argv)

        logging.info("✅ Mostrando ventana de inicio de sesión...")
        login_dialog = LoginDialog()

        if login_dialog.exec_():  # ✅ Si el login es exitoso, obtiene el usuario autenticado
            user_data = login_dialog.get_authenticated_user()  # ✅ Recuperamos el usuario autenticado
            
            if not user_data:
                logging.error("❌ No se obtuvo información del usuario autenticado. Saliendo del programa.")
                sys.exit(1)

            logging.info(f"✅ Usuario autenticado: {user_data}")
            logging.info("✅ Inicio de sesión exitoso. Ejecutando la aplicación principal.")
            
            main_window = MainWindow(user_data)  # ✅ Pasamos el usuario a la ventana principal
            main_window.show()
            sys.exit(app.exec_())  # ✅ Mantiene la aplicación en ejecución
        else:
            logging.info("❌ El usuario cerró la ventana de login. Saliendo del programa.")
            sys.exit(0)

    except Exception as e:
        logging.error(f"❌ Error crítico en la aplicación: {e}", exc_info=True)
        print("❌ Ocurrió un error inesperado. Revisa el archivo de logs.")
        sys.exit(1)

if __name__ == "__main__":
    logging.info("🚀 Iniciando aplicación...")
    main()
