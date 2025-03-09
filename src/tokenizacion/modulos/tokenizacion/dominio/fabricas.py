""" Fábricas para la creación de objetos del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de tokenización

"""

from .entidades import Tokenizacion
from .reglas import TextoTokenValido
from .excepciones import TipoObjetoNoExisteEnDominioTokenizacionExcepcion
from tokenizacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from tokenizacion.seedwork.dominio.fabricas import Fabrica
from tokenizacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaTokenizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            tokenizacion: Tokenizacion = mapeador.dto_a_entidad(obj)

            # self.validar_regla(TextoTokenValido(token))
            
            return tokenizacion

@dataclass
class FabricaTokenizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Tokenizacion.__class__:
            fabrica_tokenizacion = _FabricaTokenizacion()
            return fabrica_tokenizacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioTokenizacionExcepcion()