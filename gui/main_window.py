from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox, QAction
from PyQt5.QtCore import Qt
from gui.admin_user import AdminUsersDialog
import logging

class MainWindow(QMainWindow):  # ✅ Asegurar que la clase se llame correctamente
    """Ventana principal que se muestra después del login."""
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz de la ventana principal."""
        self.setWindowTitle("Sistema POS - Aplicación Principal")
        self.setGeometry(100, 100, 800, 600)

        # Mensaje de bienvenida
        self.central_widget = QLabel(f"Bienvenido {self.user['username']} ({self.user['rol']})")
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)

        # Configuración del menú
        self.menu_bar = self.menuBar()
        self.configurar_menu()

    def configurar_menu(self):
        """Configura el menú según el rol del usuario."""
        menu_archivo = self.menu_bar.addMenu("Archivo")
        menu_gestion = self.menu_bar.addMenu("Gestión")

        # Opciones de menú según el rol del usuario
        if self.user["rol"] == "admin":
            admin_usuarios_action = QAction("Administrar Usuarios", self)
            admin_usuarios_action.triggered.connect(self.abrir_admin_usuarios)
            menu_gestion.addAction(admin_usuarios_action)

        if self.user["rol"] in ["admin", "gerente"]:
            gestionar_stock_action = QAction("Gestionar Stock", self)
            gestionar_stock_action.triggered.connect(self.gestionar_stock)
            menu_gestion.addAction(gestionar_stock_action)

        if self.user["rol"] in ["cajero", "vendedor"]:
            generar_ticket_action = QAction("Generar Ticket", self)
            generar_ticket_action.triggered.connect(self.generar_ticket)
            menu_gestion.addAction(generar_ticket_action)

        salir_action = QAction("Salir", self)
        salir_action.triggered.connect(self.close)
        menu_archivo.addAction(salir_action)

    def abrir_admin_usuarios(self):
        """Abre la ventana de administración de usuarios (solo para administradores)."""
        logging.info("🔹 Abriendo la gestión de usuarios")
        self.admin_users_dialog = AdminUsersDialog()
        self.admin_users_dialog.exec_()

    def gestionar_stock(self):
        """Muestra un mensaje indicando que la funcionalidad de gestión de stock está en desarrollo."""
        logging.info("🔹 Gestión de stock en desarrollo")
        QMessageBox.information(self, "Gestionar Stock", "Funcionalidad para gestionar stock (En desarrollo)")

    def generar_ticket(self):
        """Muestra un mensaje indicando que la funcionalidad de generación de tickets está en desarrollo."""
        logging.info("🔹 Generación de tickets en desarrollo")
        QMessageBox.information(self, "Generar Ticket", "Funcionalidad para generar tickets (En desarrollo)")

    def main(self):
        """Muestra la ventana principal."""
        logging.info("✅ Mostrando ventana principal")
        self.show()
