from pulsar.schema import *
from dataclasses import dataclass, field
    
class CrearValidacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class AprobarValidacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class ComandoCrearValidacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = CrearValidacionPayload()
    
class ComandoAprobarValidacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = AprobarValidacionPayload()