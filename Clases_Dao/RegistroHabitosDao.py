from Clases.RegistroHabitos import RegistroHabitos
from Clases.Habitos import Habitos
from Clases.Fecha import Fecha
from Conexiones.Cursor_del_pool import Cursordelpool
from Conexiones.Logger_base import log

class RegistroHabitosDao:
    _SELECCIONAR = 'SELECT * FROM registro_habitos ORDER BY id_registro;'
    _INSERTAR = 'INSERT INTO registro_habitos (id_habito,id_fecha, completado) VALUES (%s, %s, %s) RETURNING id_registro;'
    _ACTUALIZAR = 'UPDATE registro_habitos SET completado = %s WHERE id_registro = %s;'
    _ELIMINAR_ID_HABITO = 'DELETE FROM registro_habitos WHERE id_habito = %s;'
    _ELIMINAR_ID_REGISTRO_HABITO = 'DELETE FROM registro_habitos WHERE id_registro = %s;'
    _ELIMINAR_TODO = 'DELETE FROM registro_habitos;'
    _SELECCIONAR_JOIN = '''
    SELECT 
        r.id_registro, 
        h.id_habito,
        h.nombre_habito,
        h.tipo_habito,
        f.id_fecha,
        f.fecha_habitos, 
        r.completado 
    FROM registro_habitos r 
    JOIN habitos h ON r.id_habito = h.id_habito 
    JOIN fecha f ON r.id_fecha = f.id_fecha 
    ORDER BY f.fecha_habitos;
    '''
    _SELECCIONAR_TORTA_GRAFICO = '''
    SELECT  
	r.id_registro,
    h.id_habito,
	h.tipo_habito,
	f.id_fecha,
	f.fecha_habitos,
	r.completado
    FROM registro_habitos r 
    JOIN habitos h ON r.id_habito = h.id_habito
    JOIN fecha f ON r.id_fecha = f.id_fecha;
    '''

    @classmethod
    def seleccionar(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            registro_habitos = []
            for registro in registros:
                habito = RegistroHabitos(id_registro_habito = registro[0], habito = registro[1], fecha = registro[2], completado = registro[3])
                registro_habitos.append(habito)
        return registro_habitos
    ## Primero selecciona a traves del SELECT que hace en la base de datos, para luego imprimir esos datos seleccionados

    @classmethod
    def seleccionar_join(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR_JOIN)
            registros_join = cursor.fetchall()
            registro_habitos_join = []
            for registro in registros_join:
                habito = Habitos(id_habito=registro[1], nombre_habito=registro[2], tipo_habito=registro[3])
                fecha = Fecha(id_fecha=registro[4],fecha_habitos= registro[5])
                registro_habito = RegistroHabitos(
                    id_registro_habito=registro[0],
                    completado=registro[6],
                    habito = habito,
                    fecha = fecha)
                registro_habitos_join.append(registro_habito)
        return registro_habitos_join

    @classmethod
    def seleccionar_grafio_torta(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._SELECCIONAR_TORTA_GRAFICO)
            registros_torta = cursor.fetchall()
            registro_habitos_torta = []
            for registro in registros_torta:
                habito = Habitos(id_habito=registro[1], tipo_habito=registro[2])
                fecha = Fecha(id_fecha=registro[3], fecha_habitos=registro[4])
                registro_habito = RegistroHabitos(
                    id_registro_habito=registro[0],
                    completado=registro[5],
                    habito = habito,
                    fecha = fecha)
                registro_habitos_torta.append(registro_habito)
        return registro_habitos_torta

    @classmethod
    def insertar(cls, registro_habito):
        with Cursordelpool() as cursor:
            variables = (registro_habito.habito.id_habito,
                         registro_habito.fecha.id_fecha,
                         registro_habito.completado)
            cursor.execute(cls._INSERTAR, variables)
            id_generado = cursor.fetchone()[0]
            registro_habito.id_registro = id_generado
            log.debug(f'Habito insertado: {registro_habito}')
            return id_generado

    @classmethod
    def actualizar(cls, habito):
        with Cursordelpool() as cursor:
            variables = (habito.completado,habito.id_registro)
            cursor.execute(cls._ACTUALIZAR, variables)
            log.debug(f'Habito actualizado: {habito}')
            return cursor.rowcount

    @classmethod
    def eliminar_id_habito(cls, id_habito):
        with Cursordelpool() as cursor:
            variable = (id_habito,) # Lo que pasa realmente es el id, asi que por eso no es algo como registro_habito.habito.id_habito
            cursor.execute(cls._ELIMINAR_ID_HABITO, variable)
            log.debug(f'Habito eliminado: {id_habito}')
            return cursor.rowcount

    @classmethod
    def eliminar_id_registro(cls, id_registro):
        with Cursordelpool() as cursor:
            variable = (id_registro,)
            cursor.execute(cls._ELIMINAR_ID_REGISTRO_HABITO, variable)
            log.debug(f'Habito eliminado: {id_registro}')
            return cursor.rowcount

    @classmethod
    def eliminar_todo(cls):
        with Cursordelpool() as cursor:
            cursor.execute(cls._ELIMINAR_TODO)
            log.debug(f'Se eliminó todo.')
            return cursor.rowcount
