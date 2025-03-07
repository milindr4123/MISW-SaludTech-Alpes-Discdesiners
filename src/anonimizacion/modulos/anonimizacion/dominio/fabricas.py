""" Fábricas para la creación de objetos del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de tokenización

"""

from .entidades import Anonimizacion
from .reglas import TextoTokenValido
from .excepciones import TipoObjetoNoExisteEnDominioAnonimizacionExcepcion
from anonimizacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from anonimizacion.seedwork.dominio.fabricas import Fabrica
from anonimizacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            anonimizacion: Anonimizacion = mapeador.dto_a_entidad(obj)

            # self.validar_regla(TextoTokenValido(token))
            
            return anonimizacion

@dataclass
class FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Anonimizacion.__class__:
            fabrica_anonimizacion = _FabricaAnonimizacion()
            return fabrica_anonimizacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAnonimizacionExcepcion()