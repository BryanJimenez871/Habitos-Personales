import os

from PySide6.QtGui import QAction, Qt, QIcon
from PySide6.QtWidgets import QMessageBox, QMenu


class GestorMenuContextual:
    def __init__(self,tabla,columna_click,eliminar):
        self.tabla = tabla
        self.columna_click = columna_click
        self.eliminar = eliminar

        self.tabla.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabla.customContextMenuRequested.connect(self.mostrar_menu_contextual)

    def mostrar_menu_contextual(self, posicion):

        ruta_icono_eliminar = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'eliminar.png')

        # Detectar fila donde se hizo click derecho
        columna = self.tabla.columnAt(posicion.x())
        fila = self.tabla.rowAt(posicion.y()) # se usa .y() porque interesan las filas, fuera .x() si importan las columnas y con rowAt entrega cual es la fila, esto es por pixeles, imagina que la fila 1 está entre los pixles 0-30 y la fila 2: 31-60

        if fila < 0 or columna != self.columna_click:
            return # al hacer click no hace nada.

        menu = QMenu(self.tabla)

        accion_eliminar = QAction(QIcon(ruta_icono_eliminar),'Eliminar', self.tabla)
        accion_eliminar.triggered.connect(lambda:self.confirmar_y_eliminar(fila)) # es lambda es para que se ejecute cada vez independientemente de la fila
        menu.addAction(accion_eliminar)

        menu.exec(self.tabla.mapToGlobal(posicion)) # Transforma coordenadas locales del widget en coordenadas globales para mostrar el menú contextual. Si no usas mapToGlobal, el menú aparece en lugares raros, como la esquina del programa o fuera del área del cursor.
                                                    # En otras palabras, que aparece el menú en donde hiciste click izquierdo
    def confirmar_y_eliminar(self,fila):
        msj_confirmacion = QMessageBox()
        msj_confirmacion.setIcon(QMessageBox.Icon.Warning)
        msj_confirmacion.setWindowTitle('Confirmar eliminación')
        msj_confirmacion.setText('¿Estás seguro que deseas eliminar este elemento?')
        msj_confirmacion.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msj_confirmacion.setDefaultButton(QMessageBox.StandardButton.No)

        if msj_confirmacion.exec() == QMessageBox.StandardButton.Yes:
            self.eliminar(fila)

