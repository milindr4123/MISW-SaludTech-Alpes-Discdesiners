import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoTokenCreado
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearToken
from anonimizacion.seedwork.infraestructura import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-token', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-eventos', schema=AvroSchema(EventoTokenCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'eventos-token - Evento recibido OKR: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-token', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-comandos', schema=AvroSchema(ComandoCrearToken))

        while True:
            mensaje = consumidor.receive()
            print(f'comandos-token - Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()