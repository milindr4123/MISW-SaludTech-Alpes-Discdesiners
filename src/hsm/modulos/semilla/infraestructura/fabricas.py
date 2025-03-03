""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from hsm.seedwork.dominio.fabricas import Fabrica
from hsm.seedwork.dominio.repositorios import Repositorio
from hsm.seedwork.infraestructura.vistas import Vista
from hsm.modulos.semilla.infraestructura.vistas import VistaSemilla
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.modulos.semilla.dominio.repositorios import  RepositorioSemilla, RepositorioEventosSemilla
from .repositorios import RepositorioSemillaSQLAlchemy,  RepositorioEventosSemillasSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioSemilla:
            return RepositorioSemillaSQLAlchemy()
      
        elif obj == RepositorioEventosSemilla:
            return RepositorioEventosSemillasSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Semilla:
            return VistaSemilla()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')