from pulsar.schema import *
from dataclasses import dataclass, field
from anonimizacion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class CrearAnonimizacionPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    estado = String()
    token_anonimo = String()
    # Agrega otros campos necesarios para el comando

class ComandoCrearAnonimizacion(ComandoIntegracion):
    data = CrearAnonimizacionPayload()