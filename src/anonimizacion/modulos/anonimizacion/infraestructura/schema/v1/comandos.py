from pulsar.schema import *
from dataclasses import dataclass, field
from anonimizacion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class CrearTokenPayload(ComandoIntegracion):
    id_paciente = String()
    # Agrega otros campos necesarios para el comando

class ComandoCrearToken(ComandoIntegracion):
    data = CrearTokenPayload()