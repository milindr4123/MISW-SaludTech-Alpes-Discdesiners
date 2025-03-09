from pulsar.schema import *
from dataclasses import dataclass, field
    
class CrearHsmPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class AprobarHsmPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class ComandoCrearHsm(Record):
    correlation_id = String()
    timestamp = Long()
    data = CrearHsmPayload()
    
class ComandoAprobarHsm(Record):
    correlation_id = String()
    timestamp = Long()
    data = AprobarHsmPayload()