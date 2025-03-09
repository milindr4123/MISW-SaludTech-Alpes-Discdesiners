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
class AprobarValidacion(Comando):
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    estado : str
    fecha_creacion: str
    fecha_actualizacion: str

class AprobarValidacionHandler(ValidacionBaseHandler):
    
    def handle(self, comando: AprobarValidacion):
        validacion_dto = ValidacionDTO(
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                estado = comando.estado,
                fecha_creacion =comando.fecha_creacion,
                fecha_actualizacion=comando.fecha_actualizacion)

        validacion: Validacion = self.fabrica_validacion.crear_objeto(validacion_dto, MapeadorValidacion())
        try:
            validacion.aprobar_validacion()
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, validacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(AprobarValidacion)
def ejecutar_comando_crear_validacion(comando: AprobarValidacion):
    handler = AprobarValidacionHandler()
    handler.handle(comando)