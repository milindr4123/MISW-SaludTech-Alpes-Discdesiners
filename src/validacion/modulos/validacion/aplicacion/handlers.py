from validacion.modulos.validacion.dominio.eventos import TokenCreado
from validacion.seedwork.aplicacion.handlers import Handler
from validacion.modulos.validacion.infraestructura.despachadores import Despachador

class HandlerTokenIntegracion(Handler):

    @staticmethod
    def handle_token_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'validacion-solicitud')

    @staticmethod
    def handle_token_cancelado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'validacion-solicitud')
