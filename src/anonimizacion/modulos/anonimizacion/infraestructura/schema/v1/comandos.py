from pulsar.schema import *
from dataclasses import dataclass, field
    
class CrearAnonimizacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class AprobarAnonimizacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    
class ComandoCrearAnonimizacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = CrearAnonimizacionPayload()
    
class ComandoAprobarAnonimizacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = AprobarAnonimizacionPayload()