import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QLineEdit, QLabel, QListWidget, QMessageBox, QDialog, )

from Excepciones.excepciones_personalizadas import HabitoException

import Interfaz
class DialogoAgregarHabito(QDialog):

    def __init__(self,visualizar_habitos,grafico_torta):
        super().__init__()
        ruta_icono_menu = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'agregar_nuevo_habito.png')
        self.setWindowIcon(QIcon(ruta_icono_menu))
        self.setWindowTitle('Agregar hábito')
        self.setFixedSize(600, 200)
        self.visualizar_habitos = visualizar_habitos
        self.grafico_torta = grafico_torta
        self.boton_guardar_tabla_habito = Interfaz.BotonGuardarTablaHabitos(self) # este self quiere decir que se pasa como parametro esta misma clase 'DialogoAgregarHabito'
        self.boton_guardar_tabla_habito.habito_descripcion_agregado.connect(self.visualizar_habitos.nuevo_habito) # el habito que se agrega se visualiza en la tabla
        self.boton_guardar_tabla_habito.cantidad_habito_grafico.connect(self.grafico_torta.actualizar_grafico) # actualizar el grafico luego de agregar un habito a la tabla habitos

        self.etiqueta_nombre_habito = QLabel('Ingresa un hábito\n'
                                            '[50 caracteres máx]')
        self.etiqueta_descripcion = QLabel('Ingresa una descripción\n'
                                           '[100 caracteres máx]') # mejor ajustar
        self.etiqueta_tipo_habito = QLabel('¿Es bueno o malo el hábito?')

        #Ingresar hábito
        self.texto_nuevo_habito = QLineEdit()
        self.texto_nuevo_habito.setPlaceholderText('Estudiar')
        self.texto_nuevo_habito.setMaxLength(50)

        #Ingresar descripción del hábito
        self.texto_descripcion = QTextEdit()
        self.texto_descripcion.setPlaceholderText("Estudiaré todos los días miércoles a las 4 pm.")

        #Ingresar el tipo de hábito
        self.lista_tipo_habito = QListWidget()
        self.lista_tipo_habito.addItems(['Es bueno','Es malo'])
        self.lista_tipo_habito.setCurrentRow(0)


        layout_nuevo_habito = QVBoxLayout()
        layout_nuevo_habito.addWidget(self.etiqueta_nombre_habito)
        layout_nuevo_habito.addWidget(self.texto_nuevo_habito)
        layout_nuevo_habito.addWidget(self.boton_guardar_tabla_habito)
        layout_nuevo_habito.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout_descripcion = QVBoxLayout()
        layout_descripcion.addWidget(self.etiqueta_descripcion)
        layout_descripcion.addWidget(self.texto_descripcion)

        layout_tipo_habito = QVBoxLayout()
        layout_tipo_habito.addWidget(self.etiqueta_tipo_habito)
        layout_tipo_habito.addWidget(self.lista_tipo_habito)

        contenedor = QHBoxLayout()
        contenedor.addLayout(layout_nuevo_habito)
        contenedor.addLayout(layout_descripcion)
        contenedor.addLayout(layout_tipo_habito)
        self.setLayout(contenedor)


    # Acá se usa el return por que esto es un metodo y no un SLOT, que los SLOTS son para las señales
    def get_habito(self):
        habito_bruto = self.texto_nuevo_habito.text()
        try:
            if habito_bruto:
                primer_caracter = habito_bruto[0].upper()
                habito = primer_caracter + habito_bruto[1:].lower()
                return habito # devuelve el texto mostrado en ese ítem
            else:
                raise HabitoException('Debes ingresar un hábito.')

        except HabitoException as e:
            Interfaz.MostrarMensaje(QMessageBox.Icon.Critical, 'Crítico', str(e))

    def get_descripcion(self):
        descripcion = self.texto_descripcion.toPlainText()
        return descripcion  # text() es para QLineEdit y toPlainText() es para QTextEdit

    def get_tipo_habito(self):
        tipo_habito = self.lista_tipo_habito.currentItem() # devuelve el ítem seleccionado
        return tipo_habito.text() # devuelve el texto mostrado en ese ítem

class EntradaRegistroHabitos(QWidget):
    def __init__(self):
        super().__init__()

        etiqueta_habito = QLabel('¿Qué habito hiciste hoy? 😎')
        etiqueta_completado = QLabel('¿Completaste el habito?')

        self.texto_habito = QLineEdit()

        self.completado = QListWidget()
        self.completado.addItems(['Si','No'])
        self.completado.setCurrentRow(0)

        layout_habito = QVBoxLayout()
        layout_habito.addWidget(etiqueta_habito)
        layout_habito.addWidget(self.texto_habito)
        layout_habito.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout_completado = QVBoxLayout()
        layout_completado.addWidget(etiqueta_completado)
        layout_completado.addWidget(self.completado)


        layout_principal = QHBoxLayout()
        layout_principal.addLayout(layout_habito)
        layout_principal.addLayout(layout_completado)

        self.setLayout(layout_principal)


    def habito_rellenado(self, habito):
        self.texto_habito.setText(habito) # al hacer click en un habito de la tabla habitos, se rellena automaticamente en la entrada de habitos para la tabla de registros

    def get_habito(self):
        return self.texto_habito.text()

    def get_completado(self): # una vez guardado el valor comparo si es la fila 0 o la fila 1, por defalut es la fila 0, por eso retorna true
        item = self.completado.currentRow()
        if item == 0:
            return True
        elif item == 1:
            return False
        return True # por defecto retorna que si se hizo el hábito
