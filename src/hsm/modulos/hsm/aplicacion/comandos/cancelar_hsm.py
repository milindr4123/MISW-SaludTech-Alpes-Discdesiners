from hsm.seedwork.aplicacion.comandos import Comando, ComandoHandler
from hsm.modulos.hsm.aplicacion.dto import HsmDTO
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsm
from hsm.modulos.hsm.infraestructura.repositorios import RepositorioHsm
from hsm.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
from hsm.seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class CancelarHsm(Comando):
    id: str

class CancelarHsmHandler(ComandoHandler):
    
    def handle(self, comando: CancelarHsm):
        repositorio = RepositorioHsm()
        hsm = repositorio.obtener_por_id(comando.id)
        
        if hsm:
            hsm.cancelar_hsm()
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, hsm)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

@comando.register(CancelarHsm)
def ejecutar_comando_cancelar_hsm(comando: CancelarHsm):
    handler = CancelarHsmHandler()
    handler.handle(comando)