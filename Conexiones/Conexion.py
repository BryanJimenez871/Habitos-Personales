import sys
from psycopg2 import pool
from Conexiones.Logger_base import log

class Conexion:
    _DATABASE = 'habitos_personales_prueba'
    _USERNAME = 'postgres'
    _PASSWORD = 'bryan123456'
    _DB_PORT = '5432'
    _HOST = '127.0.0.1'

    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None

    @classmethod
    def obtenerpool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                      host = cls._HOST,
                                                      user = cls._USERNAME,
                                                      password = cls._PASSWORD,
                                                      port = cls._DB_PORT,
                                                      database = cls._DATABASE)
                log.debug(f'Creación de pool exitosa: {cls._pool}')
                return cls._pool
            except Exception as e:
                log.error(f'Ocurrió un error al obtener el pool: {e}')
                sys.exit()
        else:
            return cls._pool

    @classmethod
    def obtenerconexion(cls):
        conexion = cls.obtenerpool().getconn()
        log.debug(f'Conexion exitosa: {conexion}')
        return conexion

    @classmethod
    def liberarconexion(cls,conexion):
        cls.obtenerpool().putconn(conexion)
        log.debug(f'Conexión regresa a la pool: {conexion}')

    @classmethod
    def cerrarconexion(cls):
        cls.obtenerpool().closeall()
        log.debug('Conexión cerrada')


