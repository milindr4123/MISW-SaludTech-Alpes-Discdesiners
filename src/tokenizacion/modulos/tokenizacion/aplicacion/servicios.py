from tokenizacion.seedwork.aplicacion.servicios import Servicio
from tokenizacion.modulos.tokenizacion.dominio.entidades import Token
from tokenizacion.modulos.tokenizacion.dominio.fabricas import FabricaTokens
from tokenizacion.modulos.tokenizacion.infraestructura.fabricas import FabricaRepositorio
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokens
from tokenizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorToken

from .dto import TokenDTO

import asyncio

class ServicioToken(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_tokens: FabricaTokens = FabricaTokens()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_tokens(self):
        return self._fabrica_tokens       
    
    def crear_token(self, token_dto: TokenDTO) -> TokenDTO:
        token: Token = self.fabrica_tokens.crear_objeto(token_dto, MapeadorToken())
        token.crear_token(token)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, token)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_tokens.crear_objeto(token, MapeadorToken())

    def obtener_token_por_id(self, id) -> TokenDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)
        return self.fabrica_tokens.crear_objeto(repositorio.obtener_por_id(id), MapeadorToken())