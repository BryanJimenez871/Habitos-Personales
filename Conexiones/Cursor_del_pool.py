from Conexiones.Logger_base import log
from Conexiones.Conexion import Conexion

class Cursordelpool:
    def __init__(self):
        self._conexion = None
        self._cursor = None

    def __enter__(self):
        self._conexion = Conexion.obtenerconexion()
        self._cursor = self._conexion.cursor()
        return self._cursor

    def __exit__(self, tipo_excepcion, valor_excepcion, detalle_excepcion):
        if tipo_excepcion:
            self._conexion.rollback()
            log.error(f'Ocurrió una excepción: {tipo_excepcion}, {valor_excepcion}, {detalle_excepcion}')
        else:
            self._conexion.commit()
            log.debug('Transacción existosa.')
        self._cursor.close()
        Conexion.liberarconexion(self._conexion)