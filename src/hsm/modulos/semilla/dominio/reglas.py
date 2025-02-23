"""Reglas de negocio del dominio de semilla

En este archivo usted encontrará reglas de negocio del dominio de semilla

"""

from hsm.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Formato, Length
from .entidades import Semilla

class MinimoTamano(ReglaNegocio):

    semilla: Semilla

    def __init__(self, semilla, mensaje='Al menos debe tener un tamano de 32'):
        super().__init__(mensaje)
        self.semilla = semilla

    def es_valido(self) -> bool:
        if  self.semilla.length >= 32:
                return True
        return False
