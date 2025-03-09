from tokenizacion.seedwork.aplicacion.queries import QueryHandler
from tokenizacion.modulos.tokenizacion.infraestructura.fabricas import FabricaRepositorio
from tokenizacion.modulos.tokenizacion.dominio.fabricas import FabricaTokenizacion

class TokenizacionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_tokenizacion: FabricaTokenizacion = FabricaTokenizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_tokenizacion(self):
        return self._fabrica_tokenizacion