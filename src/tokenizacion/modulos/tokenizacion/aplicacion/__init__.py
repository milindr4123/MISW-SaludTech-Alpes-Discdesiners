from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenCreado, ReservaCancelada, ReservaAprobada, ReservaPagada

dispatcher.connect(HandlerReservaIntegracion.handle_reserva_creada, signal=f'{TokenCreado.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_reserva_cancelada, signal=f'{ReservaCancelada.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_reserva_pagada, signal=f'{ReservaPagada.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_reserva_aprobada, signal=f'{ReservaAprobada.__name__}Integracion')




@dataclass
class TokenCreado(EventoDominio):
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_creacion: datetime = None

@dataclass
class DiagnosticoAsociado(EventoDominio):
    id_paciente: uuid.UUID = None
    id_diagnostico: uuid.UUID = None
    fecha_asociacion: datetime = None

@dataclass
class ImagenAsociada(EventoDominio):
    id_paciente: uuid.UUID = None
    id_imagen: uuid.UUID = None
    fecha_asociacion: datetime = None

@dataclass
class TokenRevocado(EventoDominio):
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_revocacion: datetime = None