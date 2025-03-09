from anonimizacion.seedwork.aplicacion.comandos import Comando, ComandoHandler
from anonimizacion.modulos.anonimizacion.aplicacion.dto import AnonimizacionDTO
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioAnonimizacion
from anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class CancelarAnonimizacion(Comando):
    id: str

class CancelarAnonimizacionHandler(ComandoHandler):
    
    def handle(self, comando: CancelarAnonimizacion):
        repositorio = RepositorioAnonimizacion()
        anonimizacion = repositorio.obtener_por_id(comando.id)
        
        if anonimizacion:
            anonimizacion.cancelar_anonimizacion()
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, anonimizacion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

@comando.register(CancelarAnonimizacion)
def ejecutar_comando_cancelar_anonimizacion(comando: CancelarAnonimizacion):
    handler = CancelarAnonimizacionHandler()
    handler.handle(comando)