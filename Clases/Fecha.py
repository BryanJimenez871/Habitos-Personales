from datetime import date

class Fecha:
    def __init__(self, id_fecha=None, fecha_habitos:date = None):
        self._id_fecha = id_fecha
        self._fecha_habitos = fecha_habitos

    @property
    def id_fecha(self):
        return self._id_fecha
    @id_fecha.setter
    def id_fecha(self, id_fecha):
        self._id_fecha = id_fecha

    @property
    def fecha_habitos(self):
        return self._fecha_habitos
    @fecha_habitos.setter
    def fecha_habitos(self, fecha_habitos):
        self._fecha_habitos = fecha_habitos

    def __str__(self):
        return f'Id_fecha: {self._id_fecha} | Fecha: {self._fecha_habitos}'