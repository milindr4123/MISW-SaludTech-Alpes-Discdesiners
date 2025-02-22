from tokenizacion.seedwork.aplicacion.comandos import ComandoHandler
from tokenizacion.modulos.token.infraestructura.fabricas import FabricaRepositorio
from tokenizacion.modulos.token.dominio.fabricas import FabricaTokens

class CrearTokenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_tokens: FabricaTokens = FabricaTokens()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_tokens(self):
        return self._fabrica_tokens