import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QAction
from PyQt5.QtCore import Qt
import logging

class MainWindow(QMainWindow):
    """Ventana principal mejorada con diseño tipo Excel e importación de archivos."""
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica principal."""
        self.setWindowTitle("Sistema POS - Panel Principal")
        self.setGeometry(100, 100, 900, 600)

        # ✅ MENÚ SUPERIOR
        self.menu_bar = self.menuBar()
        self.configurar_menu()

        # ✅ WIDGET CENTRAL (Contenedor principal)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()

        # ✅ MENSAJE DE BIENVENIDA
        self.label_bienvenida = QLabel(f"Bienvenido {self.user['username']} ({self.user['rol']})")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.label_bienvenida)

        # ✅ TABLA CENTRAL CON 5 COLUMNAS
        self.tabla = QTableWidget(10, 5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Cantidad", "Presentación"])
        layout_principal.addWidget(self.tabla)

        # ✅ BOTONES DE ACCIÓN
        layout_botones = QHBoxLayout()
        self.btn_importar = QPushButton("Importar desde Excel")
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_editar = QPushButton("Editar Producto")

        layout_botones.addWidget(self.btn_importar)
        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_editar)
        layout_principal.addLayout(layout_botones)

        central_widget.setLayout(layout_principal)

        # ✅ CONECTAR BOTONES
        self.btn_importar.clicked.connect(self.importar_excel)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)

    def configurar_menu(self):
        """Configura el menú de la ventana principal."""
        menu_archivo = self.menu_bar.addMenu("Archivo")
        menu_gestion = self.menu_bar.addMenu("Gestión")

        salir_action = QAction("Salir", self)
        salir_action.triggered.connect(self.close)
        menu_archivo.addAction(salir_action)

    def importar_excel(self):
        """Permite seleccionar un archivo de Excel y cargar los datos en la tabla."""
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx)", options=opciones)

        if archivo:
            logging.info(f"🔹 Importando archivo: {archivo}")
            df = pd.read_excel(archivo)  # Leer archivo Excel

            # ✅ Limpiar la tabla antes de cargar nuevos datos
            self.tabla.setRowCount(0)

            # ✅ Ajustar el número de filas y columnas según el archivo importado
            self.tabla.setRowCount(len(df))
            self.tabla.setColumnCount(len(df.columns))

            # ✅ Configurar nombres de columnas según el archivo Excel
            self.tabla.setHorizontalHeaderLabels(df.columns)

            # ✅ Llenar la tabla con los datos del archivo Excel
            for fila in range(len(df)):
                for columna in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[fila, columna]))
                    self.tabla.setItem(fila, columna, item)

            logging.info("✅ Archivo importado exitosamente.")

    # ✅ FUNCIONES DE BOTONES (Se implementarán en pasos siguientes)
    def agregar_producto(self):
        logging.info("🔹 Agregar Producto (Función en desarrollo)")

    def eliminar_producto(self):
        logging.info("🔹 Eliminar Producto (Función en desarrollo)")

    def editar_producto(self):
        logging.info("🔹 Editar Producto (Función en desarrollo)")
