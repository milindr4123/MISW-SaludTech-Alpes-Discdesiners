from anonimizacion.seedwork.aplicacion.comandos import Comando, ComandoHandler
from anonimizacion.modulos.anonimizacion.aplicacion.dto import TokenDTO
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorToken
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioTokens
from anonimizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass

@dataclass
class CancelarToken(Comando):
    id: str

class CancelarTokenHandler(ComandoHandler):
    
    def handle(self, comando: CancelarToken):
        repositorio = RepositorioTokens()
        token = repositorio.obtener_por_id(comando.id)
        
        if token:
            token.cancelar_token()
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, token)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

@comando.register(CancelarToken)
def ejecutar_comando_cancelar_token(comando: CancelarToken):
    handler = CancelarTokenHandler()
    handler.handle(comando)