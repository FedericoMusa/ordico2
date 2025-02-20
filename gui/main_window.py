from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMenuBar, QAction
from PyQt5.QtCore import Qt
import logging

class MainWindow(QMainWindow):
    """Ventana principal mejorada con diseño tipo Excel."""
    
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

        # ✅ TABLA CENTRAL CON 5 COLUMNAS (ID, Nombre, Precio, Cantidad, Presentación)
        self.tabla = QTableWidget(10, 5)  # 10 filas, 5 columnas
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Cantidad", "Presentación"])
        layout_principal.addWidget(self.tabla)

        # ✅ BOTONES DE ACCIÓN
        layout_botones = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_editar = QPushButton("Editar Producto")
        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_editar)
        layout_principal.addLayout(layout_botones)

        # ✅ ESTABLECER EL LAYOUT PRINCIPAL
        central_widget.setLayout(layout_principal)
        
        # ✅ CONECTAR BOTONES (Por ahora, sin funciones)
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

        if self.user["rol"] in ["admin", "gerente"]:
            gestionar_stock_action = QAction("Gestionar Stock", self)
            gestionar_stock_action.triggered.connect(self.gestionar_stock)
            menu_gestion.addAction(gestionar_stock_action)

        if self.user["rol"] in ["cajero", "vendedor"]:
            generar_ticket_action = QAction("Generar Ticket", self)
            generar_ticket_action.triggered.connect(self.generar_ticket)
            menu_gestion.addAction(generar_ticket_action)

    # ✅ FUNCIONES DE BOTONES (Se implementarán en pasos siguientes)
    def agregar_producto(self):
        logging.info("🔹 Agregar Producto (Función en desarrollo)")

    def eliminar_producto(self):
        logging.info("🔹 Eliminar Producto (Función en desarrollo)")

    def editar_producto(self):
        logging.info("🔹 Editar Producto (Función en desarrollo)")

    def gestionar_stock(self):
        logging.info("🔹 Gestionar Stock (Función en desarrollo)")

    def generar_ticket(self):
        logging.info("🔹 Generar Ticket (Función en desarrollo)")
