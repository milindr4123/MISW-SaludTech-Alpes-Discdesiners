from anonimizacion.seedwork.aplicacion.servicios import Servicio
from anonimizacion.modulos.anonimizacion.dominio.entidades import Token
from anonimizacion.modulos.anonimizacion.dominio.fabricas import FabricaTokenizacion
from anonimizacion.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioTokens
from anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorToken

from .dto import AnonimizacionDTO

import asyncio


# class ServicioToken(Servicio):

#     def __init__(self):
#         self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
#         self._fabrica_tokens: FabricaTokenizacion = FabricaTokenizacion()

#     @property
#     def fabrica_repositorio(self):
#         return self._fabrica_repositorio
    
#     @property
#     def fabrica_tokens(self):
#         return self._fabrica_tokens       
    
#     def crear_token(self, token_dto: AnonimizacionDTO) -> AnonimizacionDTO:
#         token: Token = self.fabrica_tokens.crear_objeto(token_dto, MapeadorToken())
#         token.crear_token(token)

#         repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)

#         UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, token)
#         UnidadTrabajoPuerto.savepoint()
#         UnidadTrabajoPuerto.commit()

#         return self.fabrica_tokens.crear_objeto(token, MapeadorToken())

#     def obtener_token_por_id(self, id) -> AnonimizacionDTO:
#         repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)
#         return self.fabrica_tokens.crear_objeto(repositorio.obtener_por_id(id), MapeadorToken())

