import pulsar
from pulsar.schema import *

from hsm.modulos.semilla.infraestructura.schema.v1.eventos import EventoSemillaCreada, SemillaCreadaPayload
from hsm.modulos.semilla.infraestructura.schema.v1.comandos import ComandoCrearSemilla, ComandoCrearSemillaPayload
from hsm.seedwork.infraestructura import utils

from hsm.modulos.semilla.infraestructura.mapeadores import MapadeadorEventosReserva

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosReserva()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoSemillaCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearSemillaPayload(
            seed=str(comando.seed)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearSemilla(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearSemilla))
