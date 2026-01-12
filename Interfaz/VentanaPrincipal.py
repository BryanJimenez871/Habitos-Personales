import os
import Interfaz
import Clases_Dao

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QMainWindow, QVBoxLayout, QFrame, QMessageBox,
    QTabWidget)


class VentanaPrincipal(QMainWindow):
    eliminar_todos_registros = Signal()
    eliminar_todos_habitos = Signal()
    def __init__(self):
        super().__init__()
        ruta_icono_ventana = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'habitos_personales.png')
        ruta_icono_menu = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'agregar_nuevo_habito.png')
        ruta_icono_eliminar = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'eliminar.png')
        ruta_iconoco_eliminar_habitos = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'eliminar_todos_habitos.png')
        self.ruta_icono_precaucion = os.path.join(os.path.dirname(__file__), '..', 'Iconos', 'precaucion.png')

        self.setWindowTitle('Habitos Personales')
        self.setWindowIcon(QIcon(ruta_icono_ventana))
        self.resize(1200,800)
        self.graficos = Interfaz.GridGraficos()
        self.entrada_registro_habitos = Interfaz.EntradaRegistroHabitos()
        self.calendario = Interfaz.Calendario()
        self.visualizar_habitos = Interfaz.VisualizarHabitos(self, self.graficos.torta_cantidad_habitos)
        self.visualizar_habitos_join = Interfaz.VisualizarRegistros(self, self.visualizar_habitos,self.graficos.registro_grafico)

        self.boton_guardar_habitos = Interfaz.BotonGuardarRegistroHabitos(self.entrada_registro_habitos, self.calendario)
        self.boton_guardar_habitos. registro_habito_agregado.connect(self.visualizar_habitos_join.agregar_registro_habito) # la misma clase que emite la señal, tiene que ser la misma clase que conecta, y conecta a la clase en donde esta la funcion/slot a realizar.
        self.boton_guardar_habitos.cantidad_registro_grafico.connect(self.graficos.registro_grafico.actualizar_grafico)

        self.visualizar_habitos.habito_selecionado.connect(self.entrada_registro_habitos.habito_rellenado)

        self.entrada_registro_habitos.layout().setContentsMargins(0,0,0,0)

        # Se hizo esto para que no se note el espacio en los distintos layouts, ya que se podía hacer esto perfectamente layout.addWidget(EntradaDatos())
        self.calendario.layout().setContentsMargins(0, 0, 0, 0)


        accion_nuevo_habito = QAction(QIcon(ruta_icono_menu), 'Agregar hábito', self)
        accion_nuevo_habito.triggered.connect(self.abrir_dialogo_habito)

        accion_eliminar_todos_registros_habitos = QAction(QIcon(ruta_icono_eliminar), 'Eliminar todos los registros', self)
        accion_eliminar_todos_registros_habitos.triggered.connect(self.eliminar_todos_los_registros)

        accion_eliminar_todos_los_habitos = QAction(QIcon(ruta_iconoco_eliminar_habitos),'Eliminar todos los los hábitos', self)
        accion_eliminar_todos_los_habitos.triggered.connect(self.eliminar_todos_los_habitos)

        # CREAR PESTAÑAS
        self.tabs = QTabWidget()

        # Crear menu
        menu = self.menuBar()
        ModificarMenu(menu)
        menu_habito = menu.addMenu('Nuevo hábito')
        menu_habito.addAction(accion_nuevo_habito)
        menu_habito.addAction(accion_eliminar_todos_registros_habitos)
        menu_habito.addAction(accion_eliminar_todos_los_habitos)

        # Linea de separador de tabla habitos y tabla registros
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)  # Horizontal
        separador.setFrameShadow(QFrame.Shadow.Plain)

        # # Layout de la tabla habitos
        layout_tabla_habitos = QVBoxLayout()
        layout_tabla_habitos.addWidget(self.visualizar_habitos)
        # ---

        # Layout tabla registro habitos join
        layout_tabla_registro_habitos_join = QVBoxLayout()
        layout_tabla_registro_habitos_join.addWidget(self.visualizar_habitos_join)
        # ---

        # contenedor top
        contenedor_top = QVBoxLayout()
        contenedor_top.addLayout(layout_tabla_habitos,1)
        contenedor_top.addWidget(separador)
        contenedor_top.addLayout(layout_tabla_registro_habitos_join,2)
        # ---

        # Contenedor bottom
        layout_entrada_registro_habitos = QVBoxLayout()
        layout_entrada_registro_habitos.addWidget(self.entrada_registro_habitos,alignment=Qt.AlignmentFlag.AlignTop)

        layout_calendario_y_boton = QVBoxLayout()
        layout_calendario_y_boton.addWidget(self.calendario)
        layout_calendario_y_boton.addWidget(self.boton_guardar_habitos)

        contenedor_botton = QHBoxLayout()
        contenedor_botton.addLayout(layout_entrada_registro_habitos)
        contenedor_botton.addLayout(layout_calendario_y_boton)
        contenedor_botton.setAlignment(Qt.AlignmentFlag.AlignCenter)

        contenedor_principal = QVBoxLayout()
        contenedor_principal.addLayout(contenedor_top,5)
        contenedor_principal.addLayout(contenedor_botton,1)

        central_widget = QWidget()
        central_widget.setLayout(contenedor_principal)


        self.tabs.addTab(central_widget, "Hábitos Personales")
        self.tabs.addTab(self.graficos, "Graficos")
        self.setCentralWidget(self.tabs)

    def abrir_dialogo_habito(self):
        grafico_objetivo = self.graficos.torta_cantidad_habitos
        dialogo = Interfaz.DialogoAgregarHabito(self.visualizar_habitos, grafico_objetivo)
        dialogo.exec()

    def eliminar_todos_los_registros(self):
        caja_mensaje = QMessageBox()
        caja_mensaje.setWindowIcon(QIcon(self.ruta_icono_precaucion))
        caja_mensaje.setIcon(QMessageBox.Icon.Warning)
        caja_mensaje.setWindowTitle("Eliminar todos los registros habitos")
        caja_mensaje.setText("¿Estás seguro de eliminar todos los registros habitos?")
        caja_mensaje.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        caja_mensaje.setDefaultButton(QMessageBox.StandardButton.No)

        if caja_mensaje.exec() == QMessageBox.StandardButton.Yes:
            Clases_Dao.RegistroHabitosDao.eliminar_todo()
            Clases_Dao.FechaDao.eliminar_todo()
            self.eliminar_todos_registros.emit()

    def eliminar_todos_los_habitos(self):
        caja_mensaje = QMessageBox()
        caja_mensaje.setWindowIcon(QIcon(self.ruta_icono_precaucion))
        caja_mensaje.setIcon(QMessageBox.Icon.Warning)
        caja_mensaje.setWindowTitle("Eliminar todos los habitos")
        caja_mensaje.setText("¿Estás seguro de eliminar todos los hábitos?")
        caja_mensaje.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        caja_mensaje.setDefaultButton(QMessageBox.StandardButton.No)
        if caja_mensaje.exec() == QMessageBox.StandardButton.Yes:
            Clases_Dao.RegistroHabitosDao.eliminar_todo()
            Clases_Dao.HabitosDao.eliminar_todo()
            Clases_Dao.FechaDao.eliminar_todo()
            self.visualizar_habitos_join.eliminar_todo()
            self.eliminar_todos_habitos.emit()

class ModificarMenu:
    def __init__(self, menu):
        self.menu = menu
        menu.setStyleSheet("""
        QMenuBar {
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0, 
            x2:1, y2:0, 
            stop:0 #feda75,      /* amarillo */
            stop:0.25 #fa7e1e,   /* naranja */
            stop:0.50 #d62976,   /* rosado fuerte */
            stop:0.75 #962fbf,   /* púrpura */
            stop:1 #4f5bd5       /* azul */
        );
        color: black;
        font-weight: bold;
        font-style: italic;
    }
    QMenuBar::item:selected {
        background: rgba(255,255,255,50);
    }

    QMenu {
        background-color: #2b2b2b;
        color: white;
        font-family: Calibri;
        font-size: 14px;
    }

    QMenu::item:selected {
        background-color: #505050;
    }
    """)
