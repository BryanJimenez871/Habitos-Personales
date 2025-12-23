from Conexiones.Cursor_del_pool import Cursordelpool
from Conexiones.Logger_base import log
from Clases.Fecha import Fecha


class FechaDao:
    _SELECCIONAR = 'SELECT * FROM fecha ORDER BY id_fecha;'
    _INSERTAR = 'INSERT INTO fecha(fecha_habitos) VALUES (%s) RETURNING id_fecha;'
    _ACTUALIZAR = 'UPDATE fecha SET fecha_habitos = %s WHERE id_fecha = %s;'
    _ELIMINAR = 'DELETE FROM fecha WHERE id_fecha = %s;'

    @classmethod
    def seleccionar(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            fechas = []
            for registro in registros:
                fecha = Fecha(registro[0], registro[1])
                fechas.append(fecha)
        return fechas
    @classmethod
    def insertar(cls, fecha):
        with Cursordelpool() as cursor:
            variable = (fecha.fecha_habitos,)
            cursor.execute(cls._INSERTAR, variable)
            id_generado = cursor.fetchone()[0] # fetchone() → devuelve la fila completa como tupla, [0] → toma solo el primer valor, que en tu caso es el id generado automáticamente. Sin hacer [0], obtendrías (5,) en lugar de 5.
            fecha.id_fecha = id_generado   # el id se genera en la BD ya q es de tipo SERIAL, y  “lo traes” a Python para poder seguir trabajando con el objeto. Sin esa asignación, el objeto Python no tiene idea de cuál es su id real.
            log.debug(f'Fecha insertada: {fecha}')
        return id_generado
    @classmethod
    def actualizar(cls, fecha):
        with Cursordelpool() as cursor:
            variables = (fecha.id_fecha,fecha.fecha_habitos)
            cursor.execute(cls._ACTUALIZAR, variables)
            log.debug(f'Fecha actualizada: {fecha}')
        return cursor.rowcount
    @classmethod
    def eliminar(cls, fecha):
        with Cursordelpool() as cursor:
            variable =(fecha.id_fecha,)
            cursor.execute(cls._ELIMINAR, variable)
            log.debug(f'Fecha eliminada: {fecha}')
        return cursor.rowcount

