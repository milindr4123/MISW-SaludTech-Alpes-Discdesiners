from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenCreado
from tokenizacion.seedwork.aplicacion.handlers import Handler
from tokenizacion.modulos.tokenizacion.infraestructura.despachadores import Despachador

class HandlerTokenIntegracion(Handler):

    @staticmethod
    def handle_token_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')

    @staticmethod
    def handle_token_cancelado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')
