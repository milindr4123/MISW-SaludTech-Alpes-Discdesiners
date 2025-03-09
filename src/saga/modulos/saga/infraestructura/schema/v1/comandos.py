from pulsar.schema import *
from dataclasses import dataclass, field
from anonimizacion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class CrearAnonimizacionPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class ComandoCrearAnonimizacion(ComandoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = CrearAnonimizacionPayload()
    
    
    
class CrearTokenizacionPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class ComandoCrearTokenizacion(ComandoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = CrearTokenizacionPayload()
    
    
    
class CrearHsmPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class ComandoCrearHsm(ComandoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = CrearHsmPayload()



class CrearValidacionPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class ComandoCrearValidacion(ComandoIntegracion):
    correlation_id = String()
    timestamp = Long()
    data = CrearValidacionPayload()