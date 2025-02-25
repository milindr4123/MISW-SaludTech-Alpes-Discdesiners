from hsm.modulos.semilla.dominio.eventos import SemillaCreada
from hsm.seedwork.aplicacion.handlers import Handler
from hsm.modulos.semilla.infraestructura.despachadores import Despachador

class HandlerSemillaIntegracion(Handler):

     @staticmethod
     def handle_semilla_creada(evento):
         despachador = Despachador()
         despachador.publicar_evento(evento, 'eventos-semilla')

#     @staticmethod
#     def handle_reserva_cancelada(evento):
#         despachador = Despachador()
#         despachador.publicar_evento(evento, 'eventos-reserva')

#     @staticmethod
#     def handle_reserva_aprobada(evento):
#         despachador = Despachador()
#         despachador.publicar_evento(evento, 'eventos-reserva')

#     @staticmethod
#     def handle_reserva_pagada(evento):
#         despachador = Despachador()
#         despachador.publicar_evento(evento, 'eventos-reserva')


