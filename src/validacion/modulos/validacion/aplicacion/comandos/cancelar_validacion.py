from validacion.seedwork.aplicacion.comandos import Comando, ComandoHandler
from validacion.modulos.validacion.aplicacion.dto import ValidacionDTO
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacion
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioValidacion
from validacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
from validacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class CancelarValidacion(Comando):
    id: str

class CancelarValidacionHandler(ComandoHandler):
    
    def handle(self, comando: CancelarValidacion):
        repositorio = RepositorioValidacion()
        validacion = repositorio.obtener_por_id(comando.id)
        
        if validacion:
            validacion.cancelar_validacion()
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, validacion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

@comando.register(CancelarValidacion)
def ejecutar_comando_cancelar_validacion(comando: CancelarValidacion):
    handler = CancelarValidacionHandler()
    handler.handle(comando)