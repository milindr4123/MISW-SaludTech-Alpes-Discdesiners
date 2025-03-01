from pulsar.schema import *
from anonimizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class TokenCreadoPayload(Record):
    id = String()
    id_paciente = String()
    token_anonimo = String()
    fecha_creacion = Long()

class EventoTokenCreado(EventoIntegracion):
    data = TokenCreadoPayload()