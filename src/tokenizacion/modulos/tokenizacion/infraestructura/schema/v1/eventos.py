from pulsar.schema import *
from tokenizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class TokenCreadoPayload(Record):
    id_token = String()
    id_usuario = String()
    estado = String()
    fecha_creacion = Long()

class EventoTokenCreado(EventoIntegracion):
    data = TokenCreadoPayload()