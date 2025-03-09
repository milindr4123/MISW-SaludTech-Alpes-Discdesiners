from pulsar.schema import *
from anonimizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from anonimizacion.seedwork.infraestructura.utils import time_millis
import uuid
class AnonimizacionCreadoPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class EventoAnonimizacionCreado(EventoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = AnonimizacionCreadoPayload()