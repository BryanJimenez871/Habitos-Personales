from Conexiones.Cursor_del_pool import Cursordelpool
from Conexiones.Logger_base import log
from Clases.Habitos import Habitos


class HabitosDao:
    _SELECCIONAR = 'SELECT * FROM habitos ORDER BY id_habito;'
    _INSERTAR = 'INSERT INTO habitos(nombre_habito, tipo_habito, descripcion) VALUES (%s, %s, %s) RETURNING id_habito;'
    _ACTUALIZAR_DESCRIPCION = 'UPDATE habitos SET descripcion = %s WHERE id_habito = %s;'
    _ELIMINAR = 'DELETE FROM habitos WHERE id_habito = %s;'
    _ELIMINAR_TODO = 'DELETE FROM habitos;'
    _SELECCIONAR_ID_HABITO = 'SELECT id_habito FROM habitos WHERE nombre_habito = %s;'
    @classmethod
    def seleccionar(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            habitos = []
            for registro in registros:
                habito = Habitos(registro[0], registro[1], registro[2],registro[3]) #id_habito, nombre_habito, tipo_habito, descripcion
                habitos.append(habito)
        return habitos

    @classmethod
    def buscar_por_nombre(cls, nombre_habito):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR_ID_HABITO, (nombre_habito,))
            row = cursor.fetchone()
            if row:
                return row[0] # si existe, retorna el id
        return None # si no, retorna nada.

    @classmethod
    def insertar(cls, habito):# no puede repetir el mismo habito y por ahora si se repite
        with Cursordelpool() as cursor:
            variables = (habito.nombre_habito, habito.tipo_habito, habito.descripcion)
            cursor.execute(cls._INSERTAR, variables)
            id_generado = cursor.fetchone()[0] # captura el id
            habito.id_habito = id_generado #el id se genera en la BD por si solo, ya q es de tipo SERIAL, y  “lo traes” a Python para poder seguir trabajando con el objeto. Sin esa asignación, el objeto Python no tiene idea de cuál es su id real.
            log.debug(f'Habito insertado: {habito}') # quitar luego está linea
            return id_generado

    @classmethod
    def actualizar(cls, habito):
        with Cursordelpool() as cursor:
            variables = (habito.descripcion, habito.id_habito)
            cursor.execute(cls._ACTUALIZAR_DESCRIPCION, variables)
            log.debug(f'Habito actualizado: {habito}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, habito):
        with Cursordelpool() as cursor:
            variable = (habito,)
            cursor.execute(cls._ELIMINAR, variable)
            log.debug(f'Habito eliminado: {habito}')
            return cursor.rowcount

    @classmethod
    def eliminar_todo(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._ELIMINAR_TODO)
            log.debug(f'Se eliminó todo.')
            return cursor.rowcount