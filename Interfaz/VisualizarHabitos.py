from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
                               QAbstractItemView, QLabel)

import Clases
import Clases_Dao


from .MenuContextual import GestorMenuContextual


class VisualizarHabitos(QWidget):
    habito_selecionado = Signal(str)
    habito_eliminado = Signal(str) # aunque el id es int, el item.txt() lo transforma en str
    cantidad_habito_grafico = Signal()
    def __init__(self,ventana_principal, grafico_torta):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ventana_principal.eliminar_todos_habitos.connect(self.eliminar_todo)

        self.grafico_torta = grafico_torta
        self.cantidad_habito_grafico.connect(self.grafico_torta.actualizar_grafico) # actualizar la cantidad de habitos en el grafico luego de eliminar un habito.

        self.mostrar_habitos = Clases_Dao.HabitosDao.seleccionar()

        self.habitos_descripcion = QTableWidget(columnCount=4)
        self.habitos_descripcion.setHorizontalHeaderLabels(['Id','Hábitos','Tipo de Hábito','Descripción'])
        self.habitos_descripcion.verticalHeader().setVisible(False)
        self.habitos_descripcion.setColumnHidden(0, True) # Escondo la columna id para el usuario
        self.habitos_descripcion.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.habitos_descripcion.resizeColumnToContents(3)
        encabezado = self.habitos_descripcion.horizontalHeader()
        encabezado.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        encabezado.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.habitos_descripcion.itemClicked.connect(self.seleccionar_habito) # rellenar automaticamente al seleccionar un habito de la tabla habitos e ingresarlo en el input para la tabla de registro

        self.menu_contextual = GestorMenuContextual(
            tabla = self.habitos_descripcion,
            columna_click = 1, # columna de habitos, es decir, solo te aparecera el "eliminar" en esta columna.
            eliminar = self.eliminar_habito_bd  )

        ModificarTabla(self.habitos_descripcion)
        self.visualizar_tabla()

        titulo_etiqueta_tabla_habitos = QLabel('Tabla de Hábitos')
        fuente = QFont('Calibri', 15)
        fuente.setBold(True)
        titulo_etiqueta_tabla_habitos.setFont(fuente)
        titulo_etiqueta_tabla_habitos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_etiqueta_tabla_habitos.setContentsMargins(0, 0, 50, 0)
        titulo_etiqueta_tabla_habitos.setStyleSheet("color: #5555FF;")
        layout_mostrar_habitos = QVBoxLayout()
        layout_mostrar_habitos.addWidget(titulo_etiqueta_tabla_habitos)
        layout_mostrar_habitos.addWidget(self.habitos_descripcion)
        self.setLayout(layout_mostrar_habitos)

    def visualizar_tabla(self): # viene de la BD
        for habito in self.mostrar_habitos:
            diccionario_habitos = {
                'id': habito.id_habito,
                'habito': habito.nombre_habito,
                'tipo_habito': habito.tipo_habito,
                'descripcion': habito.descripcion,
            }
            self.insertar_fila_tabla_habitos(diccionario_habitos)

    def nuevo_habito(self, id_habito,nombre_habito, tipo_habito, descripcion): # Viene del input
        nuevo_habito_descripcion = {
            'id': id_habito,
            'habito': nombre_habito,
            'tipo_habito': tipo_habito,
            'descripcion': descripcion,
        }
        self.insertar_fila_tabla_habitos(nuevo_habito_descripcion)

        # Al agregar un habito, se agrega a la BD y a la tabla, pero no se agrega a la lista interna  de objetos de self.mostrar_habitos
        # Esto es para que sea en tiempo real y por eso se nececista agregar también a la lista interna.
        habito_obj = Clases.Habitos(
            id_habito=id_habito,
            nombre_habito=nombre_habito,
            tipo_habito=tipo_habito,
            descripcion=descripcion
        )
        self.mostrar_habitos.append(habito_obj)

    def insertar_fila_tabla_habitos(self,diccionario):
        fila = self.habitos_descripcion.rowCount()
        self.habitos_descripcion.insertRow(fila)

        item_id = QTableWidgetItem(str(diccionario['id']))
        self.habitos_descripcion.setItem(fila,0,item_id)

        if diccionario['tipo_habito'] == 'Es bueno':
            f = ModificarItem.alinear_item
        else:
            f = ModificarItem.color_mal_habito

        self.habitos_descripcion.setItem(fila, 1, f(diccionario, 'habito'))
        self.habitos_descripcion.setItem(fila, 2, f(diccionario, 'tipo_habito'))
        self.habitos_descripcion.setItem(fila, 3, f(diccionario, 'descripcion'))

    # acá se usó la señal propia del Widget para saber cual es el item, y luego usar una señal personalizada que sirve para conectarlo con la clase EntradaRegistroHabitos()
    def seleccionar_habito(self,item):
        columna_habitos = 1
        if item.column() == columna_habitos: # si el item pertenece a la columna de habitos, se selecciona el item, de lo contrario no pasa nada B)
            texto_habito = item.text()
            self.habito_selecionado.emit(texto_habito)

    def eliminar_habito_bd(self,fila):
        id_habito = self.habitos_descripcion.item(fila,0).text() # aunque la columna id ya no se muestre para el usuario, sigue siendo muuy util seguir usando el id

        Clases_Dao.RegistroHabitosDao.eliminar_id_habito(int(id_habito))  # Elimino primero el id_habito de la tabla registro_habitos
        Clases_Dao.HabitosDao.eliminar(int(id_habito))  # y ahora recién se puede eliminar el id_habito de la tabla habitos, ya que no se puede eliminar directamente porque comparten el 'foreign key'
        self.habitos_descripcion.removeRow(fila)
        self.habito_eliminado.emit(id_habito)
        self.cantidad_habito_grafico.emit()

    def eliminar_todo(self):
        self.habitos_descripcion.clearContents()
        self.habitos_descripcion.setRowCount(0)
        self.cantidad_habito_grafico.emit()

    def get_tipo_habitos(self):
        lista_tipo_habitos = []
        for habito in self.mostrar_habitos:
            diccionario_habitos = {
                habito.nombre_habito: habito.tipo_habito,
            }
            lista_tipo_habitos.append(diccionario_habitos)
        return lista_tipo_habitos

class VisualizarRegistros(QWidget): # Cambiar el nombre a VisualizarRegistros
    cantidad_registro_grafico = Signal()
    def __init__(self,ventana_principal,visualizar_habitos,registro_grafico):
        super().__init__()

        self.visualizar_habitos = visualizar_habitos
        self.visualizar_habitos.habito_eliminado.connect(self.eliminar_habitos_join)

        self.ventana_principal = ventana_principal
        self.ventana_principal.eliminar_todos_registros.connect(self.eliminar_todo)

        self.registro_grafico = registro_grafico
        self.cantidad_registro_grafico.connect(self.registro_grafico.actualizar_grafico)


        self.mostrar_habitos_join = Clases_Dao.RegistroHabitosDao.seleccionar_join()
        self.registro_habitos_join = QTableWidget(columnCount=6)
        self.registro_habitos_join.setHorizontalHeaderLabels(['Id_registro','Id_hábito','Hábito', 'Tipo hábito', 'Fecha', 'Completado'])
        self.registro_habitos_join.verticalHeader().setVisible(False)
        self.registro_habitos_join.setColumnHidden(0, True)
        self.registro_habitos_join.setColumnHidden(1, True)
        self.registro_habitos_join.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # para que la tabla no sea editable y sea solo lectura y seleccionable

        self.menu_contextual = GestorMenuContextual(
            tabla=self.registro_habitos_join,
            columna_click=2, # columna donde está el hábito
            eliminar=self.eliminar_registro_habito_bd)

        ModificarTabla(self.registro_habitos_join)
        self.visualizar_tabla()


        encabezado = self.registro_habitos_join.horizontalHeader()
        encabezado.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # hábito
        encabezado.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # fecha
        encabezado.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch) # completado

        titulo_etiqueta_tabla_registros = QLabel('Tabla de Registros')
        fuente = QFont('Calibri', 15)
        fuente.setBold(True)
        titulo_etiqueta_tabla_registros.setFont(fuente)
        titulo_etiqueta_tabla_registros.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_etiqueta_tabla_registros.setStyleSheet("color: #E33D3D;")
        titulo_etiqueta_tabla_registros.setContentsMargins(0, 0, 50, 0)

        layout_mostrar_habitos_join = QVBoxLayout()
        layout_mostrar_habitos_join.addWidget(titulo_etiqueta_tabla_registros)
        layout_mostrar_habitos_join.addWidget(self.registro_habitos_join)
        self.setLayout(layout_mostrar_habitos_join)

    def visualizar_tabla(self):
        for registro_habito in self.mostrar_habitos_join:
            diccionario_registro_habitos = {
            'id_registro': registro_habito.id_registro_habito,
            'id_habito': registro_habito.habito.id_habito,
            'habito' : registro_habito.habito.nombre_habito,
            'tipo_habito': registro_habito.habito.tipo_habito,
            'fecha' : registro_habito.fecha.fecha_habitos.strftime('%d-%m-%Y'),
            'completado' : registro_habito.completado}

            valor = diccionario_registro_habitos['tipo_habito']
            self.insertar_fila_tabla_join(diccionario_registro_habitos, valor)

    def agregar_registro_habito(self, id_registro_habito, id_habito, nombre_habito, fecha_habitos, completado):

        nuevo_registro_habito = {
            'id_registro': id_registro_habito,
            'id_habito': id_habito,
            'habito': nombre_habito,
            'tipo_habito': None,
            'fecha': fecha_habitos,
            'completado': completado
        }

        lista_tipo_habito = self.visualizar_habitos.get_tipo_habitos()

        for tipo_habito in lista_tipo_habito:
            for llave, valor in tipo_habito.items():
                if llave == nombre_habito:
                    nuevo_registro_habito['tipo_habito'] = valor
                    self.insertar_fila_tabla_join(nuevo_registro_habito, valor)
                    return

    def insertar_fila_tabla_join(self,diccionario,valor):
        fila = self.registro_habitos_join.rowCount()
        self.registro_habitos_join.insertRow(fila)

        item_id_registro = QTableWidgetItem(str(diccionario['id_registro']))
        self.registro_habitos_join.setItem(fila, 0, item_id_registro)

        if valor == 'Es bueno':
            f = ModificarItem.alinear_item
        else:
            f = ModificarItem.color_mal_habito

        self.registro_habitos_join.setItem(fila, 1, f(diccionario, 'id_habito'))
        self.registro_habitos_join.setItem(fila, 2, f(diccionario, 'habito'))
        self.registro_habitos_join.setItem(fila, 3, f(diccionario, 'tipo_habito'))
        self.registro_habitos_join.setItem(fila, 4, f(diccionario, 'fecha'))
        self.registro_habitos_join.setItem(fila, 5, ModificarItem.completado_emoji(diccionario,'completado'))

    def eliminar_registro_habito_bd(self,fila):
        id_registro_habito = self.registro_habitos_join.item(fila,0).text() # aunque la columna id ya no se muestre para el usuario, sigue siendo muuy util seguir usando el id
        Clases_Dao.RegistroHabitosDao.eliminar_id_registro(int(id_registro_habito))  # Elimino primero el id_habito de la tabla registro_habitos # y ahora recién se puede eliminar el id_habito de la tabla habitos, ya que no se puede eliminar directamente porque comparten el 'foreign key'
        self.registro_habitos_join.removeRow(fila)
        self.cantidad_registro_grafico.emit()

    def eliminar_habitos_join(self, id_habito):
        columna_id = 1
        filas = self.registro_habitos_join.rowCount()

        filas_a_eliminar = []

        # Primero recopilamos las filas a eliminar
        for fila in range(filas):
            item = self.registro_habitos_join.item(fila, columna_id)
            if item.text() == str(id_habito):
                filas_a_eliminar.append(fila)

        # Luego eliminamos de abajo hacia arriba
        for fila in reversed(filas_a_eliminar):
            self.registro_habitos_join.removeRow(fila)
        # Si eliminas la fila 5, no afecta a las filas 0–4.
        # Al recorrer de abajo hacia arriba, el índice nunca se desajusta.
        # Esto se hace porque a la hora de borrar un habito, la consecuencia es que se borran todos los registros de ese habito, entonces para hacerlo de manera ordenada, se guarda en una lista y se borra de abajo hacia arriba :)
        self.cantidad_registro_grafico.emit()

    def eliminar_todo(self):
        self.registro_habitos_join.clearContents()
        self.registro_habitos_join.setRowCount(0)
        self.cantidad_registro_grafico.emit()

class ModificarTabla:
    def __init__(self, tabla):
        self.tabla = tabla
        self.tabla.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "background-color: #2D492F;"
            "color: black;"
            "font-family: 'Calibri';"
            "font-size: 11pt;"
            "padding: 4px;"
            "font-weight: bold;"
            "}")

class ModificarItem:
    @staticmethod
    def alinear_item(diccionario, texto):
        valor = str(diccionario[texto])
        item = QTableWidgetItem(valor)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#527D55"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 12))
        return item

    @staticmethod
    def completado_emoji(diccionario, texto):
        valor = str(diccionario[texto]) # primero se necesita el valor, en este caso si es True o False
        if str(valor) == 'True':
            texto_final = '✔'
        else:
            texto_final = '✖︎︎'

        item = QTableWidgetItem(texto_final) # QTableWidget necesita un objeto de tipo QTableWidgetItem, es decir, no acepta un valor tipo string,si uno un objeto, ya que ese objeto abarca muchas más cosas.
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#527D55"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 15))
        return item

    @staticmethod
    def color_mal_habito(diccionario, texto):
        valor = str(diccionario[texto])
        item = QTableWidgetItem(valor)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setBackground(QColor("#D93030"))
        item.setForeground(QColor("black"))
        item.setFont(QFont('Calibri', 12))
        return item
