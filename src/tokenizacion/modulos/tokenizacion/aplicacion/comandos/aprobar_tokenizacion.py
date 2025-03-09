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
class AprobarTokenizacion(Comando):
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    estado : str
    fecha_creacion: str
    fecha_actualizacion: str

class AprobarTokenizacionHandler(TokenizacionBaseHandler):
    
    def handle(self, comando: AprobarTokenizacion):
        tokenizacion_dto = TokenizacionDTO(
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                estado = comando.estado,
                fecha_creacion =comando.fecha_creacion,
                fecha_actualizacion=comando.fecha_actualizacion)

        tokenizacion: Tokenizacion = self.fabrica_tokenizacion.crear_objeto(tokenizacion_dto, MapeadorTokenizacion())
        try:
            tokenizacion.aprobar_tokenizacion()
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokenizacion)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, tokenizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(AprobarTokenizacion)
def ejecutar_comando_crear_tokenizacion(comando: AprobarTokenizacion):
    handler = AprobarTokenizacionHandler()
    handler.handle(comando)