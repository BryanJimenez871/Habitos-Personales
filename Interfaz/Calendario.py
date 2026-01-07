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

        etiqueta_anio = QLabel("Año")
        self.anio_combo = QComboBox()
        self.anio_combo.addItems([str(a) for a in range(2026, 2101)])

        etiqueta_mes = QLabel("Mes")
        self.mes_combo = QComboBox()
        self.mes_combo.addItems([
            "Sin mes","Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])

        etiqueta_dia = QLabel("Día")
        self.dia_combo = QComboBox()
        self.dia_combo.addItem(str("Sin dia"))
        self.dia_combo.addItems([str(a) for a in range(1, 32)])

        layout_anio = QVBoxLayout()
        layout_anio.addWidget(etiqueta_anio)
        layout_anio.addWidget(self.anio_combo)

        layout_mes = QVBoxLayout()
        layout_mes.addWidget(etiqueta_mes)
        layout_mes.addWidget(self.mes_combo)

        layout_dia = QVBoxLayout()
        layout_dia.addWidget(etiqueta_dia)
        layout_dia.addWidget(self.dia_combo)

        layout_principal = QHBoxLayout()
        layout_principal.addLayout(layout_anio)
        layout_principal.addLayout(layout_mes)
        layout_principal.addLayout(layout_dia)

        self.setLayout(layout_principal)

    def get_anio(self):
        anio = int(self.anio_combo.currentText())
        fecha_inicio = datetime.date(anio,1,1)
        fecha_fin = datetime.date(anio + 1, 1, 1)
        return fecha_inicio, fecha_fin

