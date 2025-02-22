from tokenizacion.modulos.token.dominio.eventos import TokenCreado, TokenCancelado, TokenAprobado, TokenPagado
from tokenizacion.seedwork.aplicacion.handlers import Handler
from tokenizacion.modulos.token.infraestructura.despachadores import Despachador

class HandlerTokenIntegracion(Handler):

    @staticmethod
    def handle_token_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')

    @staticmethod
    def handle_token_cancelado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')

    @staticmethod
    def handle_token_aprobado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')

    @staticmethod
    def handle_token_pagado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-token')