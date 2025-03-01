from anonimizacion.modulos.anonimizacion.dominio.eventos import TokenCreado
from anonimizacion.seedwork.aplicacion.handlers import Handler
from anonimizacion.modulos.anonimizacion.infraestructura.despachadores import Despachador

class HandlerTokenIntegracion(Handler):

    @staticmethod
    def handle_token_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')

    @staticmethod
    def handle_token_cancelado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')
