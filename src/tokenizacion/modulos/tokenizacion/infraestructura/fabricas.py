""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de tokenización

"""

from dataclasses import dataclass
from tokenizacion.seedwork.dominio.fabricas import Fabrica
from tokenizacion.seedwork.dominio.repositorios import Repositorio
from tokenizacion.modulos.tokenizacion.dominio.repositorios import RepositorioTokens
from .repositorios import RepositorioTokensSQLite
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioTokens:
            return RepositorioTokensSQLite()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()