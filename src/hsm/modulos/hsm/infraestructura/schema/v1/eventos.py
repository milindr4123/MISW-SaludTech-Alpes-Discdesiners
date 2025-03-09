from pulsar.schema import *
from hsm.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from hsm.seedwork.infraestructura.utils import time_millis
import uuid
class HsmCreadoPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class EventoHsmCreado(EventoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = HsmCreadoPayload()