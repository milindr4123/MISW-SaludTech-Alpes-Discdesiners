from hsm.seedwork.aplicacion.comandos import Comando
from hsm.modulos.hsm.aplicacion.dto import HsmDTO
from .base import HsmBaseHandler
from dataclasses import dataclass, field
from hsm.seedwork.aplicacion.comandos import ejecutar_commando as comando

from hsm.modulos.hsm.dominio.entidades import Hsm
from hsm.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsm
from hsm.modulos.hsm.infraestructura.repositorios import RepositorioHsm

@dataclass
class AprobarHsm(Comando):
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    estado : str
    fecha_creacion: str
    fecha_actualizacion: str

class AprobarHsmHandler(HsmBaseHandler):
    
    def handle(self, comando: AprobarHsm):
        hsm_dto = HsmDTO(
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                estado = comando.estado,
                fecha_creacion =comando.fecha_creacion,
                fecha_actualizacion=comando.fecha_actualizacion)

        hsm: Hsm = self.fabrica_hsm.crear_objeto(hsm_dto, MapeadorHsm())
        try:
            hsm.aprobar_hsm()
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioHsm)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, hsm)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(AprobarHsm)
def ejecutar_comando_crear_hsm(comando: AprobarHsm):
    handler = AprobarHsmHandler()
    handler.handle(comando)