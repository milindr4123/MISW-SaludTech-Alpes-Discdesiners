from tokenizacion.seedwork.aplicacion.queries import QueryHandler
from tokenizacion.modulos.tokenizacion.infraestructura.fabricas import FabricaRepositorio
from tokenizacion.modulos.tokenizacion.dominio.fabricas import FabricaTokenizacion

class TokenQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_tokens: FabricaTokenizacion = FabricaTokenizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_tokens(self):
        return self._fabrica_tokens