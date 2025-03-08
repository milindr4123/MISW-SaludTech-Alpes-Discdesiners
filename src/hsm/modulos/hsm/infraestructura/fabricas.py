""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de tokenización

"""

from dataclasses import dataclass
from hsm.modulos.hsm.dominio.entidades import Hsm
from hsm.modulos.hsm.infraestructura.vistas import VistaHsm
from hsm.seedwork.dominio.fabricas import Fabrica
from hsm.seedwork.dominio.repositorios import Repositorio
from hsm.modulos.hsm.dominio.repositorios import RepositorioHsm
from hsm.seedwork.infraestructura.vistas import Vista
from .repositorios import RepositorioHsmSQLite
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion, ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioHsm:
            return RepositorioHsmSQLite()
        else:
            raise NoExisteImplementacionParaTipoFabricaExcepcion()
        
@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Hsm:
            return VistaHsm()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')