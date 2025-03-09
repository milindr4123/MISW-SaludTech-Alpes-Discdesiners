from pulsar.schema import *
from validacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from validacion.seedwork.infraestructura.utils import time_millis
import uuid
class ValidacionCreadoPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class EventoValidacionCreado(EventoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = ValidacionCreadoPayload()