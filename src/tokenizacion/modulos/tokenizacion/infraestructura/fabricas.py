""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de tokenización

"""

from dataclasses import dataclass
from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from tokenizacion.modulos.tokenizacion.infraestructura.vistas import VistaTokenizacion
from tokenizacion.seedwork.dominio.fabricas import Fabrica
from tokenizacion.seedwork.dominio.repositorios import Repositorio
from tokenizacion.modulos.tokenizacion.dominio.repositorios import RepositorioTokenizacion
from tokenizacion.seedwork.infraestructura.vistas import Vista
from .repositorios import RepositorioTokenizacionSQLite
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion, ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioTokenizacion:
            return RepositorioTokenizacionSQLite()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()
        
@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Tokenizacion:
            return VistaTokenizacion()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')