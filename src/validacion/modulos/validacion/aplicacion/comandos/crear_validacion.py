from validacion.seedwork.aplicacion.comandos import Comando
from validacion.modulos.validacion.aplicacion.dto import ValidacionDTO
from .base import ValidacionBaseHandler
from dataclasses import dataclass, field
from validacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from validacion.modulos.validacion.dominio.entidades import Validacion
from validacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacion
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioValidacion

@dataclass
class CrearValidacion(Comando):
    id:str
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    fecha_creacion: str
    estado: str

class CrearValidacionHandler(ValidacionBaseHandler):
    
    def handle(self, comando: CrearValidacion):
        validacion_dto = ValidacionDTO(
                id=comando.id,
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                fecha_creacion =comando.fecha_creacion,
                estado = comando.estado)

        validacion: Validacion = self.fabrica_validacion.crear_objeto(validacion_dto, MapeadorValidacion())
        validacion.crear_validacion(validacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearValidacion)
def ejecutar_comando_crear_validacion(comando: CrearValidacion):
    handler = CrearValidacionHandler()
    handler.handle(comando)