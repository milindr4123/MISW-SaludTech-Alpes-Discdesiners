from tokenizacion.seedwork.aplicacion.comandos import Comando
from tokenizacion.modulos.tokenizacion.aplicacion.dto import TokenizacionDTO
from .base import TokenizacionBaseHandler
from dataclasses import dataclass, field
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from tokenizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacion
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokenizacion

@dataclass
class CrearTokenizacion(Comando):
    id:str
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    fecha_creacion: str
    estado: str

class CrearTokenizacionHandler(TokenizacionBaseHandler):
    
    def handle(self, comando: CrearTokenizacion):
        tokenizacion_dto = TokenizacionDTO(
                id=comando.id,
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                fecha_creacion =comando.fecha_creacion,
                estado = comando.estado)

        tokenizacion: Tokenizacion = self.fabrica_tokenizacion.crear_objeto(tokenizacion_dto, MapeadorTokenizacion())
        tokenizacion.crear_tokenizacion(tokenizacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokenizacion.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, tokenizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearTokenizacion)
def ejecutar_comando_crear_tokenizacion(comando: CrearTokenizacion):
    handler = CrearTokenizacionHandler()
    handler.handle(comando)