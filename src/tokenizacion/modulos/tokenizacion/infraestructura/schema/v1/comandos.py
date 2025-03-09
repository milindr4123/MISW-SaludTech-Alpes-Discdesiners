from pulsar.schema import *
from dataclasses import dataclass, field
    
class CrearTokenizacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class AprobarTokenizacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class ComandoCrearTokenizacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = CrearTokenizacionPayload()
    
class ComandoAprobarTokenizacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = AprobarTokenizacionPayload()