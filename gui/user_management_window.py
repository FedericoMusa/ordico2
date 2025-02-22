from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from core.database import obtener_usuarios, eliminar_usuario, actualizar_rol_usuario
import logging

class UserManagementWindow(QWidget):
    """Ventana para la administración de usuarios."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de gestión de usuarios."""
        self.setWindowTitle("Gestión de Usuarios")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Administración de Usuarios")
        layout.addWidget(self.label)

        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(4)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Email", "Rol"])
        layout.addWidget(self.tabla_usuarios)

        self.btn_actualizar = QPushButton("Actualizar Lista")
        self.btn_eliminar = QPushButton("Eliminar Usuario")
        self.btn_cambiar_rol = QPushButton("Cambiar Rol")

        layout.addWidget(self.btn_actualizar)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.btn_cambiar_rol)

        self.btn_actualizar.clicked.connect(self.cargar_usuarios)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        self.btn_cambiar_rol.clicked.connect(self.cambiar_rol_usuario)

        self.setLayout(layout)
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga los usuarios en la tabla desde la base de datos."""
        usuarios = obtener_usuarios()

        if not usuarios:
            QMessageBox.warning(self, "Aviso", "No hay usuarios registrados.")
            return

        self.tabla_usuarios.setRowCount(len(usuarios))

        for i, usuario in enumerate(usuarios):
            for j, dato in enumerate(usuario):
                self.tabla_usuarios.setItem(i, j, QTableWidgetItem(str(dato)))

    def eliminar_usuario(self):
        """Elimina un usuario seleccionado en la tabla."""
        fila = self.tabla_usuarios.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un usuario para eliminar.")
            return

        id_usuario = self.tabla_usuarios.item(fila, 0).text()

        confirmacion = QMessageBox.question(
            self, "Confirmar Eliminación", f"¿Está seguro de eliminar el usuario ID {id_usuario}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            if eliminar_usuario(id_usuario):
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                self.cargar_usuarios()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario.")

    def cambiar_rol_usuario(self):
        """Cambia el rol de un usuario seleccionado en la tabla."""
        fila = self.tabla_usuarios.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un usuario para cambiar el rol.")
            return

        id_usuario = self.tabla_usuarios.item(fila, 0).text()
        rol_actual = self.tabla_usuarios.item(fila, 3).text()
        nuevo_rol = "admin" if rol_actual == "cajero" else "cajero"

        confirmacion = QMessageBox.question(
            self, "Confirmar Cambio de Rol", f"¿Está seguro de cambiar el rol del usuario {id_usuario} a {nuevo_rol}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            if actualizar_rol_usuario(id_usuario, nuevo_rol):
                QMessageBox.information(self, "Éxito", f"Rol cambiado a {nuevo_rol}.")
                self.cargar_usuarios()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cambiar el rol del usuario.")
