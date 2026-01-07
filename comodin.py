class GridGraficos(QWidget):
    def __init__(self):
        super().__init__()
        self.cambiar_fecha = Interfaz.CambiarFecha()
        self.registro_grafico = GraficoTortaBuenosHabitos(self.cambiar_fecha)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.registro_grafico,1,0)
        self.setLayout(grid_layout)

class GraficoTortaBuenosHabitos(QWidget):
    def __init__(self,cambiar_fecha):
        super().__init__()
        # Aumentamos el ancho (figsize) para que quepan 3 gráficos
        self.figure = Figure(figsize=(12, 5))
        self.canvas = FigureCanvas(self.figure)
        self.cambiar_fecha = cambiar_fecha

        # DEFINIMOS 3 COLUMNAS: [Barra Malo] - [Torta] - [Barra Bueno]
        # width_ratios=[1, 1.5, 1] hace que la torta del medio sea más ancha que las barras
        gs = self.figure.add_gridspec(1, 3, width_ratios=[1, 1.5, 1])
        self.ax_malo = self.figure.add_subplot(gs[0])
        self.ax_torta = self.figure.add_subplot(gs[1])
        self.ax_bueno = self.figure.add_subplot(gs[2])

        self.figure.subplots_adjust(wspace=0.1)  # Un poco de espacio

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.cambiar_fecha)
        self.cambiar_fecha.visualizar_fecha_grafico.connect(self.actualizar_grafico)
        self.grafico_torta()

    def actualizar_grafico(self):
        self.ax_malo.clear()
        self.ax_torta.clear()
        self.ax_bueno.clear()
        self.grafico_torta()
        self.canvas.draw()

class CambiarFecha(QWidget):
    visualizar_fecha_grafico = Signal()
    def __init__(self):
        super().__init__()
        self.anio_combo = QComboBox()
        self.anio_combo.addItems([str(a) for a in range(2010, 2101)])

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
        fecha_fin = datetime.date(anio + 1, 12, 31)
        return fecha_inicio, fecha_fin

    def actualizar_fecha(self):
        fecha_inicio, fecha_fin = self.get_anio()
        Clases_Dao.FechaDao.seleccionar_anio(fecha_inicio, fecha_fin)
        self.visualizar_fecha_grafico.emit()