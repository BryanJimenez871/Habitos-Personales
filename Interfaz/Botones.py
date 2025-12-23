import os
import datetime
import Clases
import Clases_Dao

from Excepciones.excepciones_personalizadas import HabitoException
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QMessageBox


class BotonGuardarTablaHabitos(QWidget):
    habito_descripcion_agregado = Signal( int,str, str,str)
    cantidad_habito_grafico = Signal()
    def __init__(self, entrada_tabla_habitos):
        super().__init__()
        self.entrada_tabla_habitos = entrada_tabla_habitos

        boton_guardar_tabla_habitos = QPushButton("Agregar Hábito")
        boton_guardar_tabla_habitos.clicked.connect(self.guardar_tabla_habito)

        layout_habito = QHBoxLayout()
        layout_habito.addWidget(boton_guardar_tabla_habitos)
        self.setLayout(layout_habito)

    def guardar_tabla_habito(self):
        try:
            tabla_habitos = Clases_Dao.HabitosDao.seleccionar()
            nombre_habito = self.entrada_tabla_habitos.get_habito()
            descripcion = self.entrada_tabla_habitos.get_descripcion()
            tipo_habito = self.entrada_tabla_habitos.get_tipo_habito()

            lista_nombre_habitos = [habito.nombre_habito for habito in tabla_habitos]

            if nombre_habito in lista_nombre_habitos:
                raise HabitoException('El hábito ya existe.')

            if any(caracter.isdigit() for caracter in nombre_habito): # nombre_habito = Correr , caracter = C, O,R, R, E, R, 5
                raise HabitoException('El hábito no debe tener números.')

            if len(descripcion) > 100:
                raise HabitoException('La descripción debe ser menor de 100 caracteres.')

            habitos_obj = Clases.Habitos(nombre_habito=nombre_habito, descripcion=descripcion,tipo_habito=tipo_habito)
            id_habito = Clases_Dao.HabitosDao.insertar(habitos_obj)

            self.habito_descripcion_agregado.emit(id_habito, nombre_habito,tipo_habito, descripcion)
            self.cantidad_habito_grafico.emit()

        except HabitoException as e:
            MostrarMensaje(QMessageBox.Icon.Information,'Información', str(e))

class BotonGuardarRegistroHabitos(QWidget):
    registro_habito_agregado = Signal(int,int,str,datetime.date,bool)
    cantidad_registro_grafico = Signal()
    def __init__(self,entrada_registro,calendario):
        super().__init__()
         # Aca estoy usando la refencia de EntradaDatos, no lo estoy llamando/ejecutando!
        self.entrada_registro = entrada_registro
        self.calendario = calendario # Si fuera self.calendario = Calendario() si volveria a ejecutar la instancia es decir, la volveria a llamar  y los datos guardados anteriormente ya no estarían

        boton_guardar = QPushButton('Guardar')
        boton_guardar.clicked.connect(self.guardar_registro_habito)
        layout_boton_guardar = QHBoxLayout()
        layout_boton_guardar.addWidget(boton_guardar)
        self.setLayout(layout_boton_guardar)

    def guardar_registro_habito(self):
        try:
            nombre_habito = self.entrada_registro.get_habito()
            completado = self.entrada_registro.get_completado()

            fecha_habitos = self.calendario.get_fecha() # Para la BD
            fecha_visualizacion = fecha_habitos.strftime('%d-%m-%Y') # Para la tabla de visualización

            id_habito_existente = Clases_Dao.HabitosDao.buscar_por_nombre(nombre_habito)

            if id_habito_existente:
                habitos_obj = Clases.Habitos(id_habito=id_habito_existente, nombre_habito=nombre_habito)
            else:
                raise HabitoException('El habito no existe, primero tienes que crearlo.')

            # Crear el objeto fecha y se insertar en la BD
            fecha_obj = Clases.Fecha(fecha_habitos=fecha_habitos)
            Clases_Dao.FechaDao.insertar(fecha_obj) # como esto retorna el id_fecha puedo guardarlo en una variable

            # Insertar el registro usando los objetos ya con el 'id'
            habito_registrado = Clases.RegistroHabitos(habito=habitos_obj,fecha=fecha_obj,completado=completado)
            id_registro_habito = Clases_Dao.RegistroHabitosDao.insertar(habito_registrado) # aca va mi RegistroHabitosDao, y dentro de insertar, entra el objeto entero de Habitos, pero solo usa el registro_habito.habito.id_habito ! lo mismo con el obj de fecha
            self.registro_habito_agregado.emit(id_registro_habito, id_habito_existente, nombre_habito,fecha_visualizacion,completado) # señal
            self.cantidad_registro_grafico.emit()
        except HabitoException as e:
            MostrarMensaje(QMessageBox.Icon.Critical, "Crítico", str(e)) # se usa str() ya que es 'e' vendria ser un objeto y para mostrar el mensaje legible nesitas el __str__ y eso hace el str()

class MostrarMensaje(QMessageBox):
    def __init__(self, tipo_icono, titulo, mensaje):
        super().__init__()
        self.tipo_icono = tipo_icono
        self.titulo = titulo
        self.mensaje = mensaje
        ruta_icono = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'precaucion.png')
        caja = QMessageBox()
        caja.setIcon(self.tipo_icono)
        caja.setWindowTitle(self.titulo)
        caja.setWindowIcon(QIcon(ruta_icono))
        caja.setText(self.mensaje)
        caja.exec()


