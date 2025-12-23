class Habitos:
    def __init__(self,id_habito:int = None, nombre_habito:str = None, tipo_habito:str = None, descripcion:str = None):
        self._id_habito = id_habito
        self._nombre_habito = nombre_habito
        self._tipo_habito = tipo_habito
        self._descripcion = descripcion

    @property
    def id_habito(self):
        return self._id_habito

    @id_habito.setter
    def id_habito(self, id_habito):
        self._id_habito = id_habito

    @property
    def nombre_habito(self):
        return self._nombre_habito

    @nombre_habito.setter
    def nombre_habito(self, nombre_habito):
        self.instancia(nombre_habito,'El habito debe ser un string.')
        self._nombre_habito = nombre_habito

    @property
    def tipo_habito(self):
        return self._tipo_habito

    @tipo_habito.setter
    def tipo_habito(self, tipo_habito):
        self.instancia(tipo_habito, 'El tipo_habito debe ser un string.')
        self._tipo_habito = tipo_habito

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.instancia(descripcion,'La descripcion debe ser un string')
        self._descripcion = descripcion

    @staticmethod
    def instancia(valor, mensaje):
        if not isinstance(valor, str):
            raise ValueError(mensaje)

    def __str__(self):
        return f'Id_habito: {self._id_habito} | Nombre_Habito: {self._nombre_habito} | Tipo Habito: {self._tipo_habito} | Descripcion: {self._descripcion}'