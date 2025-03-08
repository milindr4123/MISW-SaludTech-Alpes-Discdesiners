""" Fábricas para la creación de objetos del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de tokenización

"""

from .entidades import Hsm
from .reglas import TextoTokenValido
from .excepciones import TipoObjetoNoExisteEnDominioHsmExcepcion
from hsm.seedwork.dominio.repositorios import Mapeador, Repositorio
from hsm.seedwork.dominio.fabricas import Fabrica
from hsm.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaHsm(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            hsm: Hsm = mapeador.dto_a_entidad(obj)

            # self.validar_regla(TextoTokenValido(token))
            
            return hsm

@dataclass
class FabricaHsm(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Hsm.__class__:
            fabrica_hsm = _FabricaHsm()
            return fabrica_hsm.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioHsmExcepcion()