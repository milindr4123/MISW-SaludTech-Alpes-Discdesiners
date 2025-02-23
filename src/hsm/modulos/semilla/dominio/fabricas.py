""" Fábricas para la creación de objetos del dominio de semilla

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de semilla

"""

from .entidades import Semilla
from .reglas import MinimoTamano
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from hsm.seedwork.dominio.repositorios import Mapeador
from hsm.seedwork.dominio.fabricas import Fabrica
from hsm.seedwork.dominio.entidades import Entidad
from hsm.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaSemilla(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            semilla: Semilla = mapeador.dto_a_entidad(obj)
            self.validar_regla(MinimoTamano(semilla.length))            
            return semilla

@dataclass
class FabricaSemillas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Semilla.__class__:
            fabrica_semilla = _FabricaSemilla()
            return fabrica_semilla.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

