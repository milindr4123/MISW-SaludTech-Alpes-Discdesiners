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
class CrearHsm(Comando):
    id_solicitud: str
    id_paciente : str
    token_anonimo : str
    fecha_creacion: str
    estado: str

class CrearHsmHandler(HsmBaseHandler):
    
    def handle(self, comando: CrearHsm):
        hsm_dto = HsmDTO(
                id_solicitud=comando.id_solicitud,
                id_paciente =comando.id_paciente,
                token_anonimo =comando.token_anonimo,
                fecha_creacion =comando.fecha_creacion,
                estado = comando.estado)

        hsm: Hsm = self.fabrica_hsm.crear_objeto(hsm_dto, MapeadorHsm())
        hsm.crear_hsm(hsm)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioHsm)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, hsm)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@comando.register(CrearHsm)
def ejecutar_comando_crear_hsm(comando: CrearHsm):
    handler = CrearHsmHandler()
    handler.handle(comando)