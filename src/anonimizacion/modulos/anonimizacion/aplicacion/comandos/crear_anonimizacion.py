from anonimizacion.seedwork.aplicacion.comandos import Comando
from anonimizacion.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from .base import CrearAnonimizacionBaseHandler
from dataclasses import dataclass, field
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioAnonimizacion

@dataclass
class CrearAnonimizacion(Comando):
    id:str
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    fecha_creacion: str
    estado: str

class CrearAnonimizacionHandler(CrearAnonimizacionBaseHandler):
    
    def handle(self, comando: CrearAnonimizacion):
        anonimizacion_dto = AnonimizacionDTO(
                id=comando.id,
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                fecha_creacion =comando.fecha_creacion,
                estado = comando.estado)

        anonimizacion: Anonimizacion = self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorAnonimizacion())
        anonimizacion.crear_anonimizacion(anonimizacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAnonimizacion.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearAnonimizacion)
def ejecutar_comando_crear_anonimizacion(comando: CrearAnonimizacion):
    handler = CrearAnonimizacionHandler()
    handler.handle(comando)