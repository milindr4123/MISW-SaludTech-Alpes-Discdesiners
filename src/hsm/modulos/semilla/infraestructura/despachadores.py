import sys
import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Agregar la carpeta src al sys.path
sys.path.append(os.path.join(BASE_DIR, "src"))


import pulsar
import uuid
from pulsar.schema import *

from hsm.modulos.semilla.infraestructura.schema.v1.eventos import EventoSemillaCreada, SemillaCreadaPayload
from hsm.modulos.semilla.infraestructura.schema.v1.comandos import ComandoCrearSemilla, ComandoCrearSemillaPayload
from hsm.seedwork.infraestructura import utils

from hsm.modulos.semilla.infraestructura.mapeadores import MapadeadorEventosSemilla

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosSemilla()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        print("margarita")
        print(EventoSemillaCreada)
        print(utils.broker_host())
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearSemillaPayload(
            format=comando.formato,  # Usar datos del comando recibido
            length=comando.length
        )
        comando_integracion = ComandoCrearSemilla(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearSemilla))

