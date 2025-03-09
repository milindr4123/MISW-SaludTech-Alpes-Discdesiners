from validacion.modulos.validacion.dominio.eventos import ValidacionCreada
from validacion.seedwork.aplicacion.handlers import Handler
from validacion.modulos.validacion.infraestructura.despachadores import Despachador

class HandlerValidacionIntegracion(Handler):

    @staticmethod
    def handle_validacion_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'ValidacionCreada')

    @staticmethod
    def handle_validacion_aprobado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'ValidacionAprobada')
        
    @staticmethod
    def handle_validacion_fallido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'ValidacionFallida')

    @staticmethod
    def handle_validacion_compensada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'ValidacionCompensada')
