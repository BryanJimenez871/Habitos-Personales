from Clases.Habitos import Habitos
from Clases.Fecha import Fecha

class RegistroHabitos:
    def __init__(self, id_registro_habito:int = None, habito:Habitos = None, fecha:Fecha = None, completado:bool = None):
        self._id_registro_habito = id_registro_habito
        self._habito = habito
        self._fecha = fecha
        self._completado = completado

    @property
    def id_registro_habito(self):
        return self._id_registro_habito

    @id_registro_habito.setter
    def id_registro_habito(self, id_registro_habito):
        self._id_registro_habito = id_registro_habito

    @property
    def habito(self):
        return self._habito

    @property
    def fecha(self):
        return self._fecha

    @property
    def completado(self):
        return self._completado

    @completado.setter
    def completado(self, completado):
        if not isinstance(completado, bool):
            raise ValueError("El campo 'completado' debe ser booleano (True/False).")
        self._completado = completado

    def __str__(self):
        return f'Id_Registro: {self._id_registro_habito} | ID Habito: {self._habito} | ID Fecha: {self._fecha} | Completado: {self._completado}'
