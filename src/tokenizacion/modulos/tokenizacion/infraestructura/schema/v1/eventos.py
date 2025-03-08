from pulsar.schema import *
from tokenizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from tokenizacion.seedwork.infraestructura.utils import time_millis
import uuid
class TokenizacionCreadoPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class EventoTokenizacionCreado(EventoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = TokenizacionCreadoPayload()