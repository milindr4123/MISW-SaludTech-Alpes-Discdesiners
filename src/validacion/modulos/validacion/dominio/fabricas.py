""" Fábricas para la creación de objetos del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de tokenización

"""

from .entidades import Validacion
from .reglas import TextoTokenValido
from .excepciones import TipoObjetoNoExisteEnDominioValidacionExcepcion
from validacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from validacion.seedwork.dominio.fabricas import Fabrica
from validacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaValidacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            validacion: Validacion = mapeador.dto_a_entidad(obj)

            # self.validar_regla(TextoTokenValido(token))
            
            return validacion

@dataclass
class FabricaValidacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Validacion.__class__:
            fabrica_validacion = _FabricaValidacion()
            return fabrica_validacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioValidacionExcepcion()