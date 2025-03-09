from validacion.seedwork.aplicacion.comandos import ComandoHandler
from validacion.modulos.validacion.infraestructura.fabricas import FabricaRepositorio
from validacion.modulos.validacion.dominio.fabricas import FabricaValidacion

class ValidacionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_validacion: FabricaValidacion = FabricaValidacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_validacion(self):
        return self._fabrica_validacion