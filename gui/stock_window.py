from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFileDialog, QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, QComboBox)
from core.database import obtener_productos, agregar_producto, actualizar_producto, eliminar_producto, importar_desde_excel
import logging

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

        # Título
        self.label = QLabel("Gestión de Stock")
        layout.addWidget(self.label)

        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.campo_busqueda)
        self.campo_busqueda.textChanged.connect(self.filtrar_productos)

        # Tabla de productos
        self.tabla_stock = QTableWidget()
        self.tabla_stock.setColumnCount(5)
        self.tabla_stock.setHorizontalHeaderLabels(["ID", "Nombre", "Categoría", "Cantidad", "Precio"])
        self.tabla_stock.setSortingEnabled(True)
        self.tabla_stock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla_stock)

        # Botones de acciones
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

        # Conectar botones a funciones
        self.btn_actualizar.clicked.connect(self.cargar_stock)
        self.btn_agregar.clicked.connect(self.mostrar_dialogo_agregar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_importar.clicked.connect(self.importar_desde_excel)

        self.setLayout(layout)
        self.cargar_stock()

    def cargar_stock(self):
        """Carga el stock de productos en la tabla."""
        self.tabla_stock.setRowCount(0)
        productos = obtener_productos() or []
        for producto in productos:
            fila = self.tabla_stock.rowCount()
            self.tabla_stock.insertRow(fila)
            for j, dato in enumerate(producto):
                self.tabla_stock.setItem(fila, j, QTableWidgetItem(str(dato)))

    def filtrar_productos(self):
        """Filtra los productos en la tabla según el texto ingresado."""
        texto = self.campo_busqueda.text().lower()
        for fila in range(self.tabla_stock.rowCount()):
            item = self.tabla_stock.item(fila, 1)
            self.tabla_stock.setRowHidden(fila, texto not in item.text().lower())

    def mostrar_dialogo_agregar_producto(self):
        """Muestra un cuadro de diálogo para agregar un nuevo producto."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Agregar Producto")
        layout = QFormLayout()

        input_nombre = QLineEdit()
        input_categoria = QComboBox()
        input_categoria.addItems(["Comestibles", "Productos de limpieza", "Bebidas", "Frutas y verduras", "Golosinas", "Otros"])
        input_cantidad = QSpinBox()
        input_cantidad.setMinimum(0)
        input_precio = QDoubleSpinBox()
        input_precio.setMinimum(0.01)
        input_precio.setDecimals(2)

        layout.addRow("Nombre:", input_nombre)
        layout.addRow("Categoría:", input_categoria)
        layout.addRow("Cantidad:", input_cantidad)
        layout.addRow("Precio:", input_precio)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.guardar_producto(dialogo, input_nombre.text(), input_categoria.currentText(), input_cantidad.value(), input_precio.value()))
        layout.addRow(btn_guardar)

        dialogo.setLayout(layout)
        dialogo.exec_()

    def guardar_producto(self, dialogo, nombre, categoria, cantidad, precio):
        """Guarda un nuevo producto en la base de datos."""
        if not nombre.strip():
            QMessageBox.warning(self, "Error", "El nombre del producto no puede estar vacío.")
            return
        if agregar_producto(nombre, categoria, cantidad, precio):
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.cargar_stock()
            dialogo.accept()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el producto.")

    def editar_producto(self):
        """Edita el producto seleccionado."""
        fila = self.tabla_stock.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un producto para editar.")
            return
        id_producto = int(self.tabla_stock.item(fila, 0).text())
        nombre = self.tabla_stock.item(fila, 1).text()
        categoria = self.tabla_stock.item(fila, 2).text()
        cantidad = int(self.tabla_stock.item(fila, 3).text())
        precio = float(self.tabla_stock.item(fila, 4).text())
        if actualizar_producto(id_producto, nombre, categoria, cantidad, precio):
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
        id_producto = int(self.tabla_stock.item(fila, 0).text())
        if eliminar_producto(id_producto):
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el producto.")

    def importar_desde_excel(self):
        """Importa productos desde un archivo Excel."""
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos de Excel (*.xlsx)")
        if archivo and importar_desde_excel(archivo):
            QMessageBox.information(self, "Éxito", "Productos importados correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo importar los productos.")
