from tokenizacion.seedwork.aplicacion.comandos import Comando
from tokenizacion.modulos.tokenizacion.aplicacion.dto import TokenDTO
from .base import CrearTokenBaseHandler
from dataclasses import dataclass, field
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from tokenizacion.modulos.tokenizacion.dominio.entidades import Token
from tokenizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorToken
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokens

@dataclass
class CrearToken(Comando):
    id: str
    id_paciente : str
    token_anonimo : str
    fecha_creacion: str

class CrearTokenHandler(CrearTokenBaseHandler):
    
    def handle(self, comando: CrearToken):
        token_dto = TokenDTO(
                id=comando.id,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                fecha_creacion =comando.fecha_creacion)

        token: Token = self.fabrica_tokens.crear_objeto(token_dto, MapeadorToken())
        token.crear_token(token)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, token)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearToken)
def ejecutar_comando_crear_token(comando: CrearToken):
    handler = CrearTokenHandler()
    handler.handle(comando)