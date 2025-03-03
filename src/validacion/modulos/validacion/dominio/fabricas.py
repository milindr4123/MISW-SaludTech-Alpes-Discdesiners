""" Fábricas para la creación de objetos del dominio de tokenización

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de tokenización

"""

from .entidades import Token
from .reglas import TextoTokenValido
from .excepciones import TipoObjetoNoExisteEnDominioTokenizacionExcepcion
from validacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from validacion.seedwork.dominio.fabricas import Fabrica
from validacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaToken(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            token: Token = mapeador.dto_a_entidad(obj)

            # self.validar_regla(TextoTokenValido(token))
            
            return token

@dataclass
class FabricaTokenizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Token.__class__:
            fabrica_token = _FabricaToken()
            return fabrica_token.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioTokenizacionExcepcion()