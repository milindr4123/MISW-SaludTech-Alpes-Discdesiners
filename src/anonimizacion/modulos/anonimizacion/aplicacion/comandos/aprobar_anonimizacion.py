from anonimizacion.seedwork.aplicacion.comandos import Comando
from anonimizacion.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from .base import AnonimizacionBaseHandler
from dataclasses import dataclass, field
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioAnonimizacion

@dataclass
class AprobarAnonimizacion(Comando):
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    estado : str
    fecha_creacion: str
    fecha_actualizacion: str

class AprobarAnonimizacionHandler(AnonimizacionBaseHandler):
    
    def handle(self, comando: AprobarAnonimizacion):
        anonimizacion_dto = AnonimizacionDTO(
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                estado = comando.estado,
                fecha_creacion =comando.fecha_creacion,
                fecha_actualizacion=comando.fecha_actualizacion)

        anonimizacion: Anonimizacion = self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorAnonimizacion())
        try:
            anonimizacion.aprobar_anonimizacion()
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAnonimizacion)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(AprobarAnonimizacion)
def ejecutar_comando_crear_anonimizacion(comando: AprobarAnonimizacion):
    handler = AprobarAnonimizacionHandler()
    handler.handle(comando)