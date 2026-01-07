from PySide6.QtWidgets import QWidget, QVBoxLayout, QDateEdit, QCalendarWidget, QLabel, QComboBox, QHBoxLayout, \
    QPushButton
from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QTextCharFormat, QColor
import datetime
import Clases_Dao

class Calendario(QWidget):
    def __init__(self):
        super().__init__()

        etiqueta_fecha = QLabel("Escoja la fecha del habito:")
        # Widget de fecha
        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)  # muestra calendario al hacer clic
        self.fecha.setDate(QDate.currentDate())  # fecha por defecto: hoy

        calendario = QCalendarWidget()
        calendario.setGridVisible(True) # Muestra la líneas que separa las fechas
        calendario.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        calendario.setNavigationBarVisible(True)

        calendario.setStyleSheet("""
        QCalendarWidget QAbstractItemView::item:selected {
            color: yellow;
        }
        QCalendarWidget QAbstractItemView::item:hover {
            background-color: gray;
        }
        """)

        fin_de_semana = QTextCharFormat()
        fin_de_semana.setForeground(QColor("white"))

        # Aplicar al sábado y domingo
        calendario.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, fin_de_semana)
        calendario.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, fin_de_semana)

        layout = QVBoxLayout()
        self.fecha.setCalendarWidget(calendario)
        layout.addWidget(etiqueta_fecha)
        layout.addWidget(self.fecha)

        self.setLayout(layout)

    def get_fecha(self):
        calendario = self.fecha.date()
        fecha_habitos = datetime.datetime(calendario.year(), calendario.month(), calendario.day()).date()
        return fecha_habitos


class CambiarFecha(QWidget):
    visualizar_fecha_grafico = Signal()
    def __init__(self):
        super().__init__()
        self.anio_combo = QComboBox()
        self.anio_combo.addItems([str(a) for a in range(2010, 2101)])

        self.mes_combo = QComboBox()
        self.mes_combo.addItems([
            "Sin mes","Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])

        self.dia_combo = QComboBox()
        self.dia_combo.addItem(str("Sin dia"))
        self.dia_combo.addItems([str(a) for a in range(1, 32)])

        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_actualizar.clicked.connect(self.actualizar_fecha)

        layout = QHBoxLayout()
        layout.addWidget(self.anio_combo)
        layout.addWidget(self.mes_combo)
        layout.addWidget(self.dia_combo)
        layout.addWidget(self.boton_actualizar)
        self.setLayout(layout)

    def get_anio(self):
        anio = int(self.anio_combo.currentText())
        fecha_inicio = datetime.date(anio,1,1)
        fecha_fin = datetime.date(anio + 1, 1, 1)
        return fecha_inicio, fecha_fin

