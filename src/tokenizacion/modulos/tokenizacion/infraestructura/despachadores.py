import pulsar
from pulsar.schema import *

from tokenizacion.modulos.tokenizacion.infraestructura.schema.v1.eventos import EventoTokenCreado, TokenCreadoPayload
from tokenizacion.modulos.tokenizacion.infraestructura.schema.v1.comandos import ComandoCrearToken, CrearTokenPayload
from tokenizacion.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = TokenCreadoPayload(
            id_token=str(evento.id_token), 
            id_usuario=str(evento.id_usuario), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoTokenCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoTokenCreado))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = CrearTokenPayload(
            id_usuario=str(comando.id_usuario)
            # agregar otros campos necesarios
        )
        comando_integracion = ComandoCrearToken(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearToken))