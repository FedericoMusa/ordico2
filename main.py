import sys
import logging
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QMainWindow, QApplication
from gui.login import LoginDialog
from gui.stock_window import StockWindow  # Nueva ventana para gestión de stock
from gui.user_management_window import UserManagementWindow  # Nueva ventana para gestión de usuarios
from gui.sales_window import SalesWindow  # Nueva ventana para cajeros
from core.database import inicializar_db

# Configurar logging para seguimiento de eventos en la aplicación
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz principal según el rol del usuario."""
        self.setWindowTitle("Sistema POS - Panel Principal")
        self.setGeometry(100, 100, 600, 400)  # Ajustar tamaño proporcional

        if self.user_data["rol"] == "admin":
            self.show_admin_interface()
        else:
            self.show_cashier_interface()

    def show_admin_interface(self):
        """Muestra la interfaz de administrador con botones para abrir las ventanas."""
        self.setWindowTitle("Panel de Administración")
        
        # Crear un contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Crear el layout principal
        self.layout = QVBoxLayout()
        
        # Botones para abrir las ventanas
        self.btn_stock = QPushButton("Gestión de Stock")
        self.btn_users = QPushButton("Gestión de Usuarios")

        # Agregar los botones al layout
        self.layout.addWidget(self.btn_stock)
        self.layout.addWidget(self.btn_users)

        # Conectar los botones con sus funciones
        self.btn_stock.clicked.connect(self.abrir_stock_window)
        self.btn_users.clicked.connect(self.abrir_users_window)

        # Aplicar el layout al widget central
        self.central_widget.setLayout(self.layout)

    def abrir_stock_window(self):
        """Abre la ventana de gestión de stock."""
        self.stock_window = StockWindow()
        self.stock_window.show()

    def abrir_users_window(self):
        """Abre la ventana de gestión de usuarios."""
        self.user_management_window = UserManagementWindow()
        self.user_management_window.show()

    def show_cashier_interface(self):
        """Muestra la interfaz de cajero solo con acceso a ventas."""
        self.sales_window = SalesWindow()
        self.sales_window.show()


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
