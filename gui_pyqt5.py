#!/usr/bin/env python3
"""
Implementación de la interfaz de usuario con PyQt5 que funciona correctamente
con el modo oscuro de macOS.
"""
import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, 
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                            QFileDialog, QMessageBox, QGroupBox, QFormLayout, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from excel_manager import ExcelManager
from generador_etiqueta import GeneradorEtiquetas
from reportlab.lib.units import cm

class EtiquetasAppQt(QMainWindow):
    """Aplicación para generar etiquetas usando PyQt5."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Etiquetas")
        self.setGeometry(100, 100, 1000, 700)
        
        # DataFrame para almacenar productos
        self.productos_df = pd.DataFrame(columns=[
            'Clasificación', 'Tipo de producto o servicio', 'Nombre Producto/Servicio',
            'Nombre Etiqueta', 'Variante', 'Tamanio', 'Posicion', 'Marca', 
            'Permite Decimal', 'Código Barras', 'SKU', 'Controla Stock',
            'Stock', 'Costo Neto', 'Precio Unitario', 'Precio x mayor',
            'Precio almacen', 'Precio handtag'
        ])
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear pestañas
        self.tabs = QTabWidget()
        self.tab_agregar = QWidget()
        self.tab_importar = QWidget()
        
        self.tabs.addTab(self.tab_agregar, "Agregar Productos")
        self.tabs.addTab(self.tab_importar, "Importar Excel")
        
        # Configurar contenido de pestañas
        self.setup_tab_agregar()
        self.setup_tab_importar()
        
        main_layout.addWidget(self.tabs)
        
    def setup_tab_agregar(self):
        """Configurar la pestaña para agregar productos manualmente."""
        layout = QVBoxLayout(self.tab_agregar)
        
        # Formulario para datos del producto
        form_group = QGroupBox("Datos del Producto")
        form_layout = QGridLayout()
        
        # Primera fila
        form_layout.addWidget(QLabel("Nombre Producto:"), 0, 0)
        self.txt_nombre = QLineEdit()
        form_layout.addWidget(self.txt_nombre, 0, 1)
        
        form_layout.addWidget(QLabel("Nombre Etiqueta:"), 0, 2)
        self.txt_nombre_etiqueta = QLineEdit()
        form_layout.addWidget(self.txt_nombre_etiqueta, 0, 3)
        
        form_layout.addWidget(QLabel("SKU:"), 0, 4)
        self.txt_sku = QLineEdit()
        form_layout.addWidget(self.txt_sku, 0, 5)
        
        # Segunda fila
        form_layout.addWidget(QLabel("Variante:"), 1, 0)
        self.txt_variante = QLineEdit()
        form_layout.addWidget(self.txt_variante, 1, 1)
        
        form_layout.addWidget(QLabel("Tamaño:"), 1, 2)
        self.txt_tamanio = QLineEdit()
        form_layout.addWidget(self.txt_tamanio, 1, 3)
        
        form_layout.addWidget(QLabel("Posición:"), 1, 4)
        self.txt_posicion = QLineEdit()
        form_layout.addWidget(self.txt_posicion, 1, 5)
        
        # Tercera fila
        form_layout.addWidget(QLabel("Precio Unitario:"), 2, 0)
        self.txt_precio = QDoubleSpinBox()
        self.txt_precio.setMaximum(9999.99)
        form_layout.addWidget(self.txt_precio, 2, 1)
        
        form_layout.addWidget(QLabel("Precio Handtag:"), 2, 2)
        self.txt_precio_handtag = QDoubleSpinBox()
        self.txt_precio_handtag.setMaximum(9999.99)
        form_layout.addWidget(self.txt_precio_handtag, 2, 3)
        
        form_layout.addWidget(QLabel("Stock:"), 2, 4)
        self.txt_stock = QSpinBox()
        self.txt_stock.setMinimum(0)
        self.txt_stock.setMaximum(9999)
        self.txt_stock.setValue(1)
        form_layout.addWidget(self.txt_stock, 2, 5)
        
        # Cuarta fila
        form_layout.addWidget(QLabel("Costo Neto:"), 3, 0)
        self.txt_costo = QDoubleSpinBox()
        self.txt_costo.setMaximum(9999.99)
        form_layout.addWidget(self.txt_costo, 3, 1)
        
        form_layout.addWidget(QLabel("Precio x Mayor:"), 3, 2)
        self.txt_precio_mayor = QDoubleSpinBox()
        self.txt_precio_mayor.setMaximum(9999.99)
        form_layout.addWidget(self.txt_precio_mayor, 3, 3)
        
        form_layout.addWidget(QLabel("Precio Almacén:"), 3, 4)
        self.txt_precio_almacen = QDoubleSpinBox()
        self.txt_precio_almacen.setMaximum(9999.99)
        form_layout.addWidget(self.txt_precio_almacen, 3, 5)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_agregar.clicked.connect(self.agregar_producto)
        btn_layout.addWidget(self.btn_agregar)
        
        self.btn_generar_pdf = QPushButton("Generar Etiquetas PDF")
        self.btn_generar_pdf.clicked.connect(self.generar_pdf)
        btn_layout.addWidget(self.btn_generar_pdf)
        
        self.btn_exportar = QPushButton("Exportar Excel")
        self.btn_exportar.clicked.connect(self.exportar_excel)
        btn_layout.addWidget(self.btn_exportar)
        
        self.btn_limpiar = QPushButton("Limpiar Tabla")
        self.btn_limpiar.clicked.connect(self.limpiar_tabla)
        btn_layout.addWidget(self.btn_limpiar)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Tabla de productos
        table_group = QGroupBox("Productos Agregados")
        table_layout = QVBoxLayout()
        
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Variante", "Tamaño", "Posición", 
            "Precio Unit.", "Precio Handtag", "SKU", "Stock", "Código Barras"
        ])
        
        # Configurar anchos de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nombre
        for i in range(1, 9):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.doubleClicked.connect(self.eliminar_producto)
        
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
    def setup_tab_importar(self):
        """Configurar la pestaña para importar Excel."""
        layout = QVBoxLayout(self.tab_importar)
        
        layout.addWidget(QLabel("Importar archivo Excel con productos:"))
        
        btn_layout = QHBoxLayout()
        self.btn_seleccionar = QPushButton("Seleccionar Archivo Excel")
        self.btn_seleccionar.clicked.connect(self.importar_excel)
        btn_layout.addWidget(self.btn_seleccionar)
        
        self.lbl_excel_path = QLabel("")
        btn_layout.addWidget(self.lbl_excel_path)
        
        layout.addLayout(btn_layout)
        
        self.btn_cargar = QPushButton("Cargar Productos desde Excel")
        self.btn_cargar.clicked.connect(self.cargar_desde_excel)
        layout.addWidget(self.btn_cargar)
        
        self.lbl_info = QLabel("")
        layout.addWidget(self.lbl_info)
        
        layout.addStretch()
        
    def agregar_producto(self):
        """Agregar un producto a la tabla temporal y al DataFrame."""
        # Validar datos básicos
        if not self.txt_nombre.text().strip() or not self.txt_sku.text().strip():
            QMessageBox.critical(self, "Error", "El nombre del producto y SKU son obligatorios")
            return
        
        # Si no se proporciona nombre para etiqueta, usar el nombre del producto
        nombre_etiqueta = self.txt_nombre_etiqueta.text().strip() or self.txt_nombre.text().strip()
        
        # Generar código de barras
        excel_manager = ExcelManager()
        barcode = excel_manager.generar_barcode(self.txt_sku.text())
        
        # Crear un nuevo registro para el DataFrame
        nuevo_producto = {
            'Clasificación': 'Producto',
            'Tipo de producto o servicio': '',
            'Nombre Producto/Servicio': self.txt_nombre.text(),
            'Nombre Etiqueta': nombre_etiqueta,
            'Variante': self.txt_variante.text(),
            'Tamanio': self.txt_tamanio.text(),
            'Posicion': self.txt_posicion.text(),
            'Marca': '',
            'Permite Decimal': 'No',
            'Código Barras': barcode,
            'SKU': self.txt_sku.text(),
            'Controla Stock': 'Si',
            'Stock': self.txt_stock.value(),
            'Costo Neto': self.txt_costo.value(),
            'Precio Unitario': self.txt_precio.value(),
            'Precio x mayor': self.txt_precio_mayor.value(),
            'Precio almacen': self.txt_precio_almacen.value(),
            'Precio handtag': self.txt_precio_handtag.value()
        }
        
        # Agregar al DataFrame
        self.productos_df = pd.concat([self.productos_df, pd.DataFrame([nuevo_producto])], ignore_index=True)
        
        # Agregar a la tabla visual
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(nombre_etiqueta))
        self.table.setItem(row, 1, QTableWidgetItem(self.txt_variante.text()))
        self.table.setItem(row, 2, QTableWidgetItem(self.txt_tamanio.text()))
        self.table.setItem(row, 3, QTableWidgetItem(self.txt_posicion.text()))
        self.table.setItem(row, 4, QTableWidgetItem(f"S/ {self.txt_precio.value():.2f}"))
        self.table.setItem(row, 5, QTableWidgetItem(f"S/ {self.txt_precio_handtag.value():.2f}"))
        self.table.setItem(row, 6, QTableWidgetItem(self.txt_sku.text()))
        self.table.setItem(row, 7, QTableWidgetItem(str(self.txt_stock.value())))
        self.table.setItem(row, 8, QTableWidgetItem(barcode))
        
        # Limpiar el formulario para un nuevo ingreso
        self.limpiar_formulario()
        
        QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
    
    def eliminar_producto(self):
        """Elimina un producto de la tabla al hacer doble clic."""
        row = self.table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                        "¿Desea eliminar este producto?", 
                                        QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Obtener el SKU del producto seleccionado
                sku = self.table.item(row, 6).text()
                
                # Eliminar del DataFrame
                self.productos_df = self.productos_df[self.productos_df['SKU'] != sku]
                
                # Eliminar de la tabla visual
                self.table.removeRow(row)
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.txt_nombre.clear()
        self.txt_nombre_etiqueta.clear()
        self.txt_variante.clear()
        self.txt_tamanio.clear()
        self.txt_posicion.clear()
        self.txt_sku.clear()
        self.txt_precio.setValue(0.0)
        self.txt_stock.setValue(1)
        self.txt_costo.setValue(0.0)
        self.txt_precio_mayor.setValue(0.0)
        self.txt_precio_almacen.setValue(0.0)
        self.txt_precio_handtag.setValue(0.0)
    
    def limpiar_tabla(self):
        """Limpia toda la tabla de productos."""
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Desea eliminar todos los productos de la tabla?", 
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Limpiar DataFrame
            self.productos_df = pd.DataFrame(columns=self.productos_df.columns)
            
            # Limpiar tabla visual
            self.table.setRowCount(0)
    
    def importar_excel(self):
        """Abre un diálogo para seleccionar un archivo Excel."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo Excel", "", 
            "Archivos Excel (*.xlsx *.xls)"
        )
        if filepath:
            self.lbl_excel_path.setText(filepath)
    
    def cargar_desde_excel(self):
        """Carga productos desde un archivo Excel seleccionado."""
        filepath = self.lbl_excel_path.text()
        if not filepath:
            QMessageBox.critical(self, "Error", "Primero seleccione un archivo Excel")
            return
        
        try:
            # Leer Excel
            excel_manager = ExcelManager(filepath)
            excel_manager.cargar_excel()
            
            # Actualizar DataFrame
            self.productos_df = excel_manager.data
            
            # Limpiar tabla visual
            self.table.setRowCount(0)
            
            # Mostrar productos en la tabla
            total_productos = 0
            for _, row in self.productos_df.iterrows():
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                
                nombre_etiqueta = row.get('Nombre Etiqueta', '') or row.get('Nombre Producto/Servicio', '')
                
                self.table.setItem(row_idx, 0, QTableWidgetItem(nombre_etiqueta))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(row.get('Variante', ''))))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(row.get('Tamanio', ''))))
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(row.get('Posicion', ''))))
                self.table.setItem(row_idx, 4, QTableWidgetItem(f"S/ {row.get('Precio Unitario', 0):.2f}"))
                self.table.setItem(row_idx, 5, QTableWidgetItem(f"S/ {row.get('Precio handtag', 0):.2f}"))
                self.table.setItem(row_idx, 6, QTableWidgetItem(str(row.get('SKU', ''))))
                self.table.setItem(row_idx, 7, QTableWidgetItem(str(row.get('Stock', 0))))
                self.table.setItem(row_idx, 8, QTableWidgetItem(str(row.get('Código Barras', ''))))
                
                total_productos += 1
            
            self.lbl_info.setText(f"Se cargaron {total_productos} productos desde el Excel")
            QMessageBox.information(self, "Éxito", f"Se cargaron {total_productos} productos desde el Excel")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el archivo: {str(e)}")
    
    def generar_pdf(self):
        """Genera un PDF con las etiquetas de todos los productos."""
        if self.productos_df.empty:
            QMessageBox.critical(self, "Error", "No hay productos para generar etiquetas")
            return
        
        try:
            # Crear directorio de salida si no existe
            if not os.path.exists("output"):
                os.makedirs("output")
            
            # Crear un ExcelManager temporal con nuestros datos
            excel_manager = ExcelManager()
            excel_manager.data = self.productos_df
            
            # Generar datos para etiquetas
            datos_etiquetas = excel_manager.generar_datos_etiquetas()
            
            if not datos_etiquetas:
                QMessageBox.critical(self, "Error", "No hay productos con stock para generar etiquetas")
                return
            
            # Crear generador de etiquetas
            generador = GeneradorEtiquetas("output/etiquetas_productos.pdf", custom_width=10.02*cm)
            
            # Generar PDF
            generador.generar_pdf(datos_etiquetas)
            
            QMessageBox.information(self, "Éxito", 
                                  f"PDF generado en: output/etiquetas_productos.pdf\n"
                                  f"Se generaron {len(datos_etiquetas)} etiquetas")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar PDF: {str(e)}")
    
    def exportar_excel(self):
        """Exporta los productos a un archivo Excel."""
        if self.productos_df.empty:
            QMessageBox.critical(self, "Error", "No hay productos para exportar")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Guardar Excel", "", "Archivos Excel (*.xlsx)"
        )
        
        if not filepath:
            return
        
        try:
            # Crear directorio si no existe
            output_dir = os.path.dirname(filepath)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Exportar DataFrame a Excel
            self.productos_df.to_excel(filepath, index=False)
            QMessageBox.information(self, "Éxito", f"Excel exportado exitosamente en: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar Excel: {str(e)}")

def main():
    """Función principal para iniciar la aplicación."""
    app = QApplication(sys.argv)
    
    # Usar estilo Fusion que se ve bien en modo claro y oscuro
    app.setStyle('Fusion')
    
    window = EtiquetasAppQt()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()