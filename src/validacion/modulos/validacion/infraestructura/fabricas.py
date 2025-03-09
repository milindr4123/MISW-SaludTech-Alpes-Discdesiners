""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de tokenización

"""

from dataclasses import dataclass
from validacion.modulos.validacion.dominio.entidades import Validacion
from validacion.modulos.validacion.infraestructura.vistas import VistaValidacion
from validacion.seedwork.dominio.fabricas import Fabrica
from validacion.seedwork.dominio.repositorios import Repositorio
from validacion.modulos.validacion.dominio.repositorios import RepositorioValidacion
from validacion.seedwork.infraestructura.vistas import Vista
from .repositorios import RepositorioValidacionSQLite
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion, ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioValidacion:
            return RepositorioValidacionSQLite()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()
        
@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Validacion:
            return VistaValidacion()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')