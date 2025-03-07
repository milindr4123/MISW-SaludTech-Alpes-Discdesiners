""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de tokenización

"""

from dataclasses import dataclass
from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.vistas import VistaAnonimizacion
from anonimizacion.seedwork.dominio.fabricas import Fabrica
from anonimizacion.seedwork.dominio.repositorios import Repositorio
from anonimizacion.modulos.anonimizacion.dominio.repositorios import RepositorioAnonimizacion
from anonimizacion.seedwork.infraestructura.vistas import Vista
from .repositorios import RepositorioAnonimizacionSQLite
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion, ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioAnonimizacion:
            return RepositorioAnonimizacionSQLite()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()
        
@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Anonimizacion:
            return VistaAnonimizacion()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')