from pulsar.schema import *
from dataclasses import dataclass, field
from anonimizacion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class CrearTokenPayload(ComandoIntegracion):
    id_solicitud = String()
    id_paciente = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()
    # Agrega otros campos necesarios para el comando

class ComandoCrearToken(ComandoIntegracion):
    data = CrearTokenPayload()