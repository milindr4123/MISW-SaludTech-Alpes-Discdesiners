from hsm.seedwork.aplicacion.queries import QueryHandler
from hsm.modulos.semilla.infraestructura.fabricas import FabricaRepositorio
from hsm.modulos.semilla.dominio.fabricas import FabricaSemillas

class SemillaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_semillas: FabricaSemillas = FabricaSemillas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_semillas(self):
        return self._fabrica_semillas    