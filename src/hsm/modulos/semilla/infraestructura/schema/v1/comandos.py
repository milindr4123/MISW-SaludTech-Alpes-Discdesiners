from pulsar.schema import *
from dataclasses import dataclass, field
from hsm.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearSemillaPayload(ComandoIntegracion):
    format=String()
    length=String()
    # TODO Cree los records para itinerarios

class ComandoCrearSemilla(ComandoIntegracion):
    data = ComandoCrearSemillaPayload()