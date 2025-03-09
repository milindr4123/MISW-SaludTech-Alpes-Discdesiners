from hsm.modulos.hsm.dominio.eventos import HsmCreada
from hsm.seedwork.aplicacion.handlers import Handler
from hsm.modulos.hsm.infraestructura.despachadores import Despachador

class HandlerHsmIntegracion(Handler):

    @staticmethod
    def handle_hsm_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'HsmCreada')

    @staticmethod
    def handle_hsm_aprobado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'HsmAprobada')
        
    @staticmethod
    def handle_hsm_fallido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'HsmFallida')

    @staticmethod
    def handle_hsm_compensada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'HsmCompensada')
