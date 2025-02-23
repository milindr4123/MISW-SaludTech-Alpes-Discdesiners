from hsm.seedwork.aplicacion.comandos import ComandoHandler
from hsm.modulos.semilla.infraestructura.fabricas import FabricaRepositorio
from hsm.modulos.semilla.dominio.fabricas import FabricaSemilla

class CrearSemillaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaSemilla = FabricaSemilla()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_vuelos(self):
        return self._fabrica_semilla   
    