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

class EventoAnonimizacionCreado(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = AnonimizacionCreadoPayload()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)