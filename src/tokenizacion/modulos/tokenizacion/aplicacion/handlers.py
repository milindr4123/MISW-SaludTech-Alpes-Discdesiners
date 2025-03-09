from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenizacionCreada
from tokenizacion.seedwork.aplicacion.handlers import Handler
from tokenizacion.modulos.tokenizacion.infraestructura.despachadores import Despachador

class HandlerTokenizacionIntegracion(Handler):

    @staticmethod
    def handle_tokenizacion_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'TokenizacionCreada')

    @staticmethod
    def handle_tokenizacion_aprobado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'TokenizacionAprobada')
        
    @staticmethod
    def handle_tokenizacion_fallido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'TokenizacionFallida')

    @staticmethod
    def handle_tokenizacion_compensada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'TokenizacionCompensada')
