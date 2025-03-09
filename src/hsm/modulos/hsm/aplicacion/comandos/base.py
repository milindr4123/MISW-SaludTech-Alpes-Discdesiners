from hsm.seedwork.aplicacion.comandos import ComandoHandler
from hsm.modulos.hsm.infraestructura.fabricas import FabricaRepositorio
from hsm.modulos.hsm.dominio.fabricas import FabricaHsm

class HsmBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_hsm: FabricaHsm = FabricaHsm()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_hsm(self):
        return self._fabrica_hsm