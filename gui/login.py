from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.auth import autenticar_usuario  
from gui.register import RegistroDialog  
from gui.recovery import RecuperarContrasenaDialog  
import logging

class LoginDialog(QDialog):
    """Ventana de inicio de sesión con diseño optimizado."""

    def __init__(self):
        super().__init__()
        self.authenticated_user = None  # Guardar usuario autenticado
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inicio de Sesión - ORDICO")
        self.setGeometry(100, 100, 400, 250)
        self.setMinimumSize(400, 250)

        layout = QVBoxLayout()

        # Campos de entrada
        self.username_label = QLabel("Usuario o Email:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botones
        self.login_button = QPushButton("Iniciar Sesión")
        self.register_button = QPushButton("Registrarse")
        self.forgot_password_button = QPushButton("¿Olvidaste tu contraseña?")

        # Estilos mejorados
        button_style = """
            QPushButton {
                background-color: #8B0000;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """
        self.login_button.setStyleSheet(button_style)
        self.register_button.setStyleSheet(button_style)
        self.forgot_password_button.setStyleSheet("color: #8B0000; font-weight: bold;")

        # Agregar widgets al layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.forgot_password_button)

        self.setLayout(layout)
        logging.info("✅ Ventana de inicio de sesión mostrada correctamente.")

        # Conectar botones a sus funciones
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.open_register)
        self.forgot_password_button.clicked.connect(self.open_recovery)

    def login(self):
        """Verifica las credenciales del usuario y autentica."""
        entrada = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not entrada or not password:
            QMessageBox.warning(self, "Error", "Debe ingresar usuario/email y contraseña.")
            return

        logging.info(f"🔍 Intentando iniciar sesión con usuario/email: {entrada}")
        
        # 🔹 Pasamos la contraseña sin hashear (la comparación se hace en `auth.py`)
        usuario = autenticar_usuario(entrada, password)  

        if usuario:
            logging.info(f"✅ Inicio de sesión exitoso. Usuario: {usuario['username']}")
            self.authenticated_user = usuario
            QMessageBox.information(self, "Éxito", f"Bienvenido {usuario['username']} ({usuario['rol']})")
            self.accept()
        else:
            logging.warning("❌ Credenciales incorrectas.")
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def open_register(self):
        """Abre la ventana de registro."""
        self.registro_dialog = RegistroDialog()
        self.registro_dialog.exec_()

    def open_recovery(self):
        """Abre la ventana de recuperación de contraseña."""
        self.recuperar_contrasena_dialog = RecuperarContrasenaDialog()
        self.recuperar_contrasena_dialog.exec_()

    def get_authenticated_user(self):
        """Retorna el usuario autenticado después de un inicio de sesión exitoso."""
        return self.authenticated_user
