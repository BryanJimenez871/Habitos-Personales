import logging as log
import os

ruta = os.path.join(os.path.dirname(__file__), '..', 'Conexiones', 'capas_datos.log')
log.basicConfig(level=log.WARNING,
                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt = '%d/%m/%Y %I:%M:%S %p',
                handlers = [
                    log.FileHandler(ruta, encoding='utf-8'),
                    log.StreamHandler()
                ]
               )