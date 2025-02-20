from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class AdminUsersDialog(QDialog):
    """Ventana de administración de usuarios para el encargado."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Administrar Usuarios")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("Aquí puedes gestionar los usuarios del sistema.")
        layout.addWidget(label)

        self.setLayout(layout)
