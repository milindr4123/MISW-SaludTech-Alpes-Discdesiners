from anonimizacion.modulos.anonimizacion.dominio.eventos import AnonimizacionCreada
from anonimizacion.seedwork.aplicacion.handlers import Handler
from anonimizacion.modulos.anonimizacion.infraestructura.despachadores import Despachador

class HandlerAnonimizacionIntegracion(Handler):

    @staticmethod
    def handle_anonimizacion_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'AnonimizacionCreada')

    @staticmethod
    def handle_anonimizacion_aprobado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'AnonimizacionAprobada')
        
    @staticmethod
    def handle_anonimizacion_fallido(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'AnonimizacionFallida')

    @staticmethod
    def handle_anonimizacion_compensada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'AnonimizacionCompensada')
