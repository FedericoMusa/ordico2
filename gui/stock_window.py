from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLineEdit, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QLabel
from core.database import obtener_productos, agregar_producto, actualizar_producto, eliminar_producto, importar_desde_excel
import logging
import pandas as pd

class StockWindow(QWidget):
    """Ventana para la gestión del stock de productos."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de gestión de stock."""
        self.setWindowTitle("Gestión de Stock")
        self.setGeometry(200, 200, 800, 500)

        layout = QVBoxLayout()

        # 🔹 Título
        self.label = QLabel("Gestión de Stock")
        layout.addWidget(self.label)

        # 🔹 Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.campo_busqueda)
        self.campo_busqueda.textChanged.connect(self.filtrar_productos)  # 🔍 Filtrar productos en tiempo real

        # 🔹 Tabla de productos
        self.tabla_stock = QTableWidget()
        self.tabla_stock.setColumnCount(4)
        self.tabla_stock.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Precio"])
        self.tabla_stock.setSortingEnabled(True)  # Habilita la ordenación de columnas

        # 🔹 Ajuste automático de columnas y filas
        self.tabla_stock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_stock.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.tabla_stock)

        # 🔹 Estilo tipo Excel
        self.tabla_stock.setStyleSheet("""
            QTableWidget {
                border: 1px solid gray;
                gridline-color: gray;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)

        # 🔹 Botones de acciones organizados horizontalmente
        botones_layout = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_agregar = QPushButton("Agregar")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_importar = QPushButton("Importar desde Excel")

        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_importar)
        layout.addLayout(botones_layout)

        # 🔹 Conectar botones a sus funciones
        self.btn_actualizar.clicked.connect(self.cargar_stock)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_importar.clicked.connect(self.importar_desde_excel)

        self.setLayout(layout)

        # 🔹 Cargar datos iniciales
        self.cargar_stock()

    def cargar_stock(self):
        """Carga el stock de productos en la tabla."""
        try:
            productos = obtener_productos() or []
            self.tabla_stock.setRowCount(len(productos))
            for i, producto in enumerate(productos):
                for j, dato in enumerate(producto):
                    self.tabla_stock.setItem(i, j, QTableWidgetItem(str(dato)))
        except Exception as e:
            logging.error(f"❌ Error al cargar stock: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo cargar el stock: {e}")

    def filtrar_productos(self):
        """Filtra los productos en la tabla según el texto ingresado."""
        texto = self.campo_busqueda.text().lower()
        self.cargar_stock()

    def agregar_producto(self):
        """Agrega un nuevo producto al stock."""
        nombre = "Nuevo Producto"
        cantidad = 10
        precio = 100.0

        if agregar_producto(nombre, cantidad, precio):
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el producto.")

    def editar_producto(self):
        """Edita el producto seleccionado en la tabla."""
        fila = self.tabla_stock.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un producto para editar.")
            return

        id_producto = int(self.tabla_stock.item(fila, 0).text())
        nombre = self.tabla_stock.item(fila, 1).text()
        cantidad = int(self.tabla_stock.item(fila, 2).text())
        precio = float(self.tabla_stock.item(fila, 3).text())

        if actualizar_producto(id_producto, nombre, cantidad, precio):
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el producto.")

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        fila = self.tabla_stock.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar.")
            return

        id_producto = self.tabla_stock.item(fila, 0).text()

        if eliminar_producto(id_producto):
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el producto.")

    def importar_desde_excel(self):
        """Importa productos desde un archivo Excel."""
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos de Excel (*.xlsx)")
        if archivo:
            if importar_desde_excel(archivo):
                QMessageBox.information(self, "Éxito", "Productos importados correctamente.")
                self.cargar_stock()
            else:
                QMessageBox.warning(self, "Error", "No se pudo importar los productos.")
