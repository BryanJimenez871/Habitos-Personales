import Clases_Dao

from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GridGraficos(QWidget):
    def __init__(self):
        super().__init__()

        self.torta_cantidad_habitos = GraficoTortaCantidadHabitos()
        self.registro_grafico = GraficoTortaBuenosHabitos()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.torta_cantidad_habitos,0,0)
        grid_layout.addWidget(self.registro_grafico,1,0)
        self.setLayout(grid_layout)


class GraficoTortaCantidadHabitos(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.grafico_torta()

    def grafico_torta(self):

        tabla_habitos = Clases_Dao.HabitosDao.seleccionar()

        lista_diccionario = []

        for habito in tabla_habitos:
            diccionario_registro_habitos = {
                'tipo_habito': habito.tipo_habito}
            lista_diccionario.append(diccionario_registro_habitos)

        buen_habito = 0
        mal_habito = 0

        for diccionario in lista_diccionario:
            if diccionario['tipo_habito'] == 'Es bueno':
                buen_habito += 1
            else:
                mal_habito += 1

        categorias = ["Buenos", "Malos"]
        valores =[buen_habito, mal_habito]
        explode = (0.09, 0)

        if sum(valores) == 0:
            self.ax.text(0.5,0.5,"Sin datos", ha='center')
            self.ax.axis("off")
            self.canvas.draw()
            return

        wedges, *_ = self.ax.pie(
            valores,
            explode=explode,
            labels=categorias,
            autopct=lambda pct: self.mostrar_porcentaje_y_gramos(pct, valores)
        )
        for w in wedges: # Son los sectores del gráfico (las “rebanadas” del círculo).
            w.set_edgecolor('black')

        self.ax.set_title("Cantidad de hábitos")
        self.canvas.draw()

    @staticmethod
    def mostrar_porcentaje_y_gramos(porcentaje, valores_totales):
        total = sum(valores_totales)
        cantidad = int((porcentaje / 100) * total)  # (7,5/100) * 1000 = 75. PCT, es una variable que viene de matplotlib que por defecto ya saca los %, entonces para mostrarlo como valor absoluto, se necesita calcular de manera inversa.
        texto = f"{porcentaje:.1f}%\n({cantidad} hábitos)"  # formatea el texto
        return texto

    def actualizar_grafico(self):
        self.ax.clear()
        self.grafico_torta()
        self.canvas.draw()

class GraficoTortaBuenosHabitos(QWidget):
    def __init__(self):
        super().__init__()
        # Aumentamos el ancho (figsize) para que quepan 3 gráficos
        self.figure = Figure(figsize=(12, 5))
        self.canvas = FigureCanvas(self.figure)

        # DEFINIMOS 3 COLUMNAS: [Barra Malo] - [Torta] - [Barra Bueno]
        # width_ratios=[1, 1.5, 1] hace que la torta del medio sea más ancha que las barras
        gs = self.figure.add_gridspec(1, 3, width_ratios=[1, 1.5, 1])
        self.ax_malo = self.figure.add_subplot(gs[0])
        self.ax_torta = self.figure.add_subplot(gs[1])
        self.ax_bueno = self.figure.add_subplot(gs[2])

        self.figure.subplots_adjust(wspace=0.1)  # Un poco de espacio

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.grafico_torta()

    def grafico_torta(self):
        # Ocultamos ejes por defecto (se activan solo si hay datos)
        self.ax_malo.axis('off')
        self.ax_torta.axis('off')
        self.ax_bueno.axis('off')

        # 2. Obtención y Procesamiento de Datos
        tabla_registro = Clases_Dao.RegistroHabitosDao.seleccionar_grafio_torta()

        # Inicializamos contadores
        mejora_personal = 0
        deterioro_personal = 0
        detalle_mejora = [0, 0]  # [Bueno Completado, Malo Evitado]
        detalle_deterioro = [0, 0]  # [Bueno No Hecho, Malo Completado]

        for registro in tabla_registro:
            tipo = registro.habito.tipo_habito
            completado = registro.completado

            # Lógica simplificada de clasificación
            es_mejora = (tipo == 'Es bueno' and completado) or (tipo == 'Es malo' and not completado)

            if es_mejora:
                mejora_personal += 1
                idx = 0 if tipo == 'Es bueno' else 1
                detalle_mejora[idx] += 1
            else:  # Es deterioro
                deterioro_personal += 1
                idx = 0 if tipo == 'Es malo' else 1
                detalle_deterioro[idx] += 1

        # 3. Configuración General de la Torta
        valores_torta = [mejora_personal, deterioro_personal]
        total = sum(valores_torta)

        # Validación de vacío
        if total == 0:
            self.ax_torta.text(0.5, 0.5, "Sin datos", ha='center')
            self.canvas.draw()
            return

        categorias_torta = ["Mejora", "Deterioro"]
        # Siempre usamos los mismos colores. Si un valor es 0, ese color no se verá.
        colors = ['#90EE90', '#FF7F7F']
        explode = (0.05, 0)  # Separamos siempre el "slice" de la mejora

        # Calculamos el ángulo para que la línea divisoria quede siempre vertical.
        # Esta fórmula funciona incluso si uno de los valores es 0.
        angle = -180 * (valores_torta[0] / total)

        # 4. Dibujar Torta
        wedges, *_ = self.ax_torta.pie(
            valores_torta,
            autopct=lambda pct: self.mostrar_porcentaje(pct, total),
            startangle=angle,
            labels=categorias_torta,
            explode=explode,
            colors=colors
        )

        for w in wedges: w.set_edgecolor('black')

        # 5. Dibujar Barras Laterales (Condicionales Independientes)

        # --- Barra DERECHA (Mejora) ---
        if mejora_personal:
            self.dibujar_barra_detalle(
                ax=self.ax_bueno,
                valores=detalle_mejora,
                labels=["H. Bueno\nCompletado", "H. Malo\nNo Completado"],
                color_base='#90EE90',
                lado="derecha"
            )

        # --- Barra IZQUIERDA (Deterioro) ---
        if deterioro_personal:
            self.dibujar_barra_detalle(
                ax=self.ax_malo,
                valores=detalle_deterioro,
                labels=["H. Malo\nCompletado", "H. Bueno\nNo completado"],
                color_base='#FF7F7F',
                lado="izquierda"
            )
        self.ax_torta.set_title("Detalle sobre los registro de hábitos")
        self.canvas.draw()

    @staticmethod
    def dibujar_barra_detalle(ax, valores, labels, color_base, lado):
        total = sum(valores)
        if total == 0: return

        width = 0.3
        ratios = [v / total for v in valores]
        bottom = 0

        # Dibujar barras apiladas
        for j, (height, label) in enumerate((zip(ratios, labels))):
            alpha = 0.5 + (0.4 * j) # la definicion del color, y que la clave es la j.
            bc = ax.bar(0, height, width, bottom=bottom, label=label,
                        color=color_base, alpha=alpha, edgecolor='black')
            ax.bar_label(bc, labels=[f"{valores[j]}\n({height:.0%})"], label_type='center')
            bottom += height

        ax.set_xlim(-0.5, 0.5)
        ax.axis('off')

        # Leyenda
        loc_anchor = (0.7, 0.5) if lado == "derecha" else (0.3, 0.5)
        loc_align = "center left" if lado == "derecha" else "center right"
        handles, labels_legend = ax.get_legend_handles_labels() # obtiene la leyenda tal como Matplotlib la creó
        ax.legend(
            handles[::-1], # como está apilado la barra y la legenda no, se muestra al revez. # EL cuadradito
            labels_legend[::-1], # El texto
            loc=loc_align,
            bbox_to_anchor=loc_anchor,
            fontsize='small'
        )

    @staticmethod
    def mostrar_porcentaje(pct, total_abs):
        cantidad = int((pct / 100) * total_abs)
        return f"{pct:.1f}%\n({cantidad})"

    def actualizar_grafico(self):
        self.ax_malo.clear()
        self.ax_torta.clear()
        self.ax_bueno.clear()
        self.grafico_torta()
        self.canvas.draw()

