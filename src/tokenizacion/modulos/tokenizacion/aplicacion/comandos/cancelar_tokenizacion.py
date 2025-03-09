from tokenizacion.seedwork.aplicacion.comandos import Comando, ComandoHandler
from tokenizacion.modulos.tokenizacion.aplicacion.dto import TokenizacionDTO
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacion
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokenizacion
from tokenizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class CancelarTokenizacion(Comando):
    id: str

class CancelarTokenizacionHandler(ComandoHandler):
    
    def handle(self, comando: CancelarTokenizacion):
        repositorio = RepositorioTokenizacion()
        tokenizacion = repositorio.obtener_por_id(comando.id)
        
        if tokenizacion:
            tokenizacion.cancelar_tokenizacion()
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, tokenizacion)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

@comando.register(CancelarTokenizacion)
def ejecutar_comando_cancelar_tokenizacion(comando: CancelarTokenizacion):
    handler = CancelarTokenizacionHandler()
    handler.handle(comando)