# from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
#
#
# class GraficoTortaBuenosHabitos(QWidget):
#     def __init__(self,cambiar_fecha):
#         super().__init__()
#         # Aumentamos el ancho (figsize) para que quepan 3 gráficos
#         self.figure = Figure(figsize=(12, 5))
#         self.canvas = FigureCanvas(self.figure)
#         self.cambiar_fecha = cambiar_fecha
#
#         # DEFINIMOS 3 COLUMNAS: [Barra Malo] - [Torta] - [Barra Bueno]
#         # width_ratios=[1, 1.5, 1] hace que la torta del medio sea más ancha que las barras
#         gs = self.figure.add_gridspec(1, 3, width_ratios=[1, 1.5, 1])
#         self.ax_malo = self.figure.add_subplot(gs[0])
#         self.ax_torta = self.figure.add_subplot(gs[1])
#         self.ax_bueno = self.figure.add_subplot(gs[2])
#
#         self.figure.subplots_adjust(wspace=0.1)  # Un poco de espacio
#
#         self.boton_actualizar = QPushButton("Actualizar")
#         self.boton_actualizar.clicked.connect(self.actualizar_grafico_anio)
#
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.canvas)
#
#         layout_cambiar_fecha = QHBoxLayout()
#         layout_cambiar_fecha.addWidget(self.cambiar_fecha)
#         layout_cambiar_fecha.addWidget(self.boton_actualizar)
#
#         contenedor = QVBoxLayout()
#         contenedor.addLayout(layout)
#         contenedor.addLayout(layout_cambiar_fecha)
#         self.grafico_torta()
#
#     @staticmethod
#     def dibujar_barra_detalle(ax, valores, labels, color_base, lado):
#         total = sum(valores)
#         if total == 0: return
#
#         width = 0.3
#         ratios = [v / total for v in valores]
#         bottom = 0
#
#         # Dibujar barras apiladas
#         for j, (height, label) in enumerate((zip(ratios, labels))):
#             alpha = 0.5 + (0.4 * j) # la definicion del color, y que la clave es la j.
#             bc = ax.bar(0, height, width, bottom=bottom, label=label,
#                         color=color_base, alpha=alpha, edgecolor='black')
#             ax.bar_label(bc, labels=[f"{valores[j]}\n({height:.0%})"], label_type='center')
#             bottom += height
#
#         ax.set_xlim(-0.5, 0.5)
#         ax.axis('off')
#
#         # Leyenda
#         loc_anchor = (0.7, 0.5) if lado == "derecha" else (0.3, 0.5)
#         loc_align = "center left" if lado == "derecha" else "center right"
#         handles, labels_legend = ax.get_legend_handles_labels() # obtiene la leyenda tal como Matplotlib la creó
#         ax.legend(
#             handles[::-1], # como está apilado la barra y la legenda no, se muestra al revez. # EL cuadradito
#             labels_legend[::-1], # El texto
#             loc=loc_align,
#             bbox_to_anchor=loc_anchor,
#             fontsize='small'
#         )
#
#     def grafico_solo_anio(self):
#         self.ax_malo.axis('off')
#         self.ax_torta.axis('off')
#         self.ax_bueno.axis('off')
#         fecha_inicio, fecha_fin = self.cambiar_fecha.get_anio()
#         tabla_anio = Clases_Dao.FechaDao.seleccionar_anio(fecha_inicio,fecha_fin)
#         mejora_personal = 0
#         deterioro_personal = 0
#         detalle_mejora = [0, 0]  # [Bueno Completado, Malo Evitado]
#         detalle_deterioro = [0, 0]  # [Bueno No Hecho, Malo Completado]
#
#         for registro in tabla_anio:
#             tipo = registro.habito.tipo_habito
#             completado = registro.completado
#
#             # Lógica simplificada de clasificación
#             es_mejora = (tipo == 'Es bueno' and completado) or (tipo == 'Es malo' and not completado)
#
#             if es_mejora:
#                 mejora_personal += 1
#                 idx = 0 if tipo == 'Es bueno' else 1
#                 detalle_mejora[idx] += 1
#             else:  # Es deterioro
#                 deterioro_personal += 1
#                 idx = 0 if tipo == 'Es malo' else 1
#                 detalle_deterioro[idx] += 1
#
#         # 3. Configuración General de la Torta
#         valores_torta = [mejora_personal, deterioro_personal]
#         total = sum(valores_torta)
#
#         # Validación de vacío
#         if total == 0:
#             self.ax_torta.text(0.5, 0.5, "Sin datos", ha='center')
#             self.canvas.draw()
#             return
#
#         categorias_torta = ["Mejora", "Deterioro"]
#         # Siempre usamos los mismos colores. Si un valor es 0, ese color no se verá.
#         colors = ['#90EE90', '#FF7F7F']
#         explode = (0.05, 0)  # Separamos siempre el "slice" de la mejora
#
#         # Calculamos el ángulo para que la línea divisoria quede siempre vertical.
#         # Esta fórmula funciona incluso si uno de los valores es 0.
#         angle = -180 * (valores_torta[0] / total)
#
#         # 4. Dibujar Torta
#         wedges, *_ = self.ax_torta.pie(
#             valores_torta,
#             autopct=lambda pct: self.mostrar_porcentaje(pct, total),
#             startangle=angle,
#             labels=categorias_torta,
#             explode=explode,
#             colors=colors
#         )
#
#         for w in wedges: w.set_edgecolor('black')
#
#         # 5. Dibujar Barras Laterales (Condicionales Independientes)
#
#         # --- Barra DERECHA (Mejora) ---
#         if mejora_personal:
#             self.dibujar_barra_detalle(
#                 ax=self.ax_bueno,
#                 valores=detalle_mejora,
#                 labels=["H. Bueno\nCompletado", "H. Malo\nNo Completado"],
#                 color_base='#90EE90',
#                 lado="derecha"
#             )
#
#         # --- Barra IZQUIERDA (Deterioro) ---
#         if deterioro_personal:
#             self.dibujar_barra_detalle(
#                 ax=self.ax_malo,
#                 valores=detalle_deterioro,
#                 labels=["H. Malo\nCompletado", "H. Bueno\nNo completado"],
#                 color_base='#FF7F7F',
#                 lado="izquierda"
#             )
#         self.ax_torta.set_title("Detalle sobre los registro de hábitos")
#         self.canvas.draw()
#
#     @staticmethod
#     def mostrar_porcentaje(pct, total_abs):
#         cantidad = int((pct / 100) * total_abs)
#         return f"{pct:.1f}%\n({cantidad})"
#
#
#     def actualizar_grafico_anio(self):
#         print("actualizando")
#         self.ax_malo.clear()
#         self.ax_torta.clear()
#         self.ax_bueno.clear()
#         self.grafico_solo_anio()
#         self.canvas.draw()
#
# class CambiarFecha(QWidget):
#     visualizar_fecha_grafico = Signal()
#     def __init__(self):
#         super().__init__()
#         self.anio_combo = QComboBox()
#         self.anio_combo.addItems([str(a) for a in range(2010, 2101)])
#
#         self.mes_combo = QComboBox()
#         self.mes_combo.addItems([
#             "Sin mes","Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
#             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
#         ])
#
#         self.dia_combo = QComboBox()
#         self.dia_combo.addItem(str("Sin dia"))
#         self.dia_combo.addItems([str(a) for a in range(1, 32)])
#
#         self.boton_actualizar = QPushButton("Actualizar")
#         #self.boton_actualizar.clicked.connect(self.actualizar_fecha)
#
#         layout = QHBoxLayout()
#         layout.addWidget(self.anio_combo)
#         layout.addWidget(self.mes_combo)
#         layout.addWidget(self.dia_combo)
#         layout.addWidget(self.boton_actualizar)
#         self.setLayout(layout)
#
#     def get_anio(self):
#         anio = int(self.anio_combo.currentText())
#         fecha_inicio = datetime.date(anio,1,1)
#         fecha_fin = datetime.date(anio + 1, 1, 1)
#         return fecha_inicio, fecha_fin
#
# class FechaDao:
#     _SELECCIONAR_ANIO = '''
#     SELECT
#         h.tipo_habito,
#         r.completado,
# 		f.fecha_habitos
#     FROM registro_habitos r
#     JOIN habitos h ON r.id_habito = h.id_habito
# 	JOIN fecha f ON r.id_fecha = f.id_fecha
#     WHERE fecha_habitos >= %s
#     AND fecha_habitos <  %s;
#     '''
#
#
#     @classmethod
#     def seleccionar_anio(cls,fecha_inicio,fecha_fin):
#         with Cursordelpool() as cursor:
#             cursor.execute(cls._SELECCIONAR_ANIO, (fecha_inicio,fecha_fin))
#             registros_torta = cursor.fetchall()
#             registro_habitos_torta = []
#             for registro in registros_torta:
#                 habito = Habitos(tipo_habito=registro[0])
#                 fecha = Fecha(fecha_habitos=registro[2])
#                 registro_habito = RegistroHabitos(
#                     completado=registro[1],
#                     habito=habito,
#                     fecha=fecha)
#                 registro_habitos_torta.append(registro_habito)