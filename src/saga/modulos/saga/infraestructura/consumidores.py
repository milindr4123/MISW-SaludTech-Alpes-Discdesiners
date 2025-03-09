import logging
import traceback
import aiopulsar
import pulsar, _pulsar
from pulsar.schema import *
import json

from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionCreado
from saga.modulos.saga.aplicacion.saga_orchestrator import SagaOrchestrator
from saga.seedwork.infraestructura import utils


async def suscribirse_a_comandos(app=None):
    print(f"SagaOrchestrator suscribirse_a_comandos !!!!!!!!!!!!!!")
    orchestrator = SagaOrchestrator(app)
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topic=[
                    'AnonimizacionRechazada',
                    'AnonimizacionAprobada',
                    'TokenizacionAprobada',
                    'TokenizacionRechazada',
                    'HsmAprobada',
                    'HsmRechazada',
                    'ValidacionAprobada',
                    'ValidacionRechazada'
                ],
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='anonimizacion-sub-comandos', 
                schema=AvroSchema(ComandoCrearAnonimizacion)
            ) as consumidor:
                while True:
                    msg =  await consumidor.receive()
                    topic = msg.topic_name()
                    raw_data = msg.data()
                    datos = msg.value()
                    print(f"SagaOrchestrator topic_name recibido: {topic}")
                    print(f"SagaOrchestrator Mensaje recibido raw: {raw_data}")
                    print(f"SagaOrchestrator Mensaje recibido obj: {datos}")
                    
                    if 'AnonimizacionAprobada' in topic:
                        await orchestrator.manejador_anonimizacion_aprobada(datos.data)
                    elif 'AnonimizacionRechazada' in topic: #evento de compensacion
                        await orchestrator.manejador_anonimizacion_rechazada(datos.data)
                    elif 'TokenizacionAprobada' in topic:
                        await orchestrator.manejador_tokenizacion_aprobada(datos.data)
                    elif 'TokenizacionRechazada' in topic:
                        await orchestrator.manejador_tokenizacion_rechazada(datos.data)
                    elif 'HsmAprobada' in topic:
                        await orchestrator.manejador_hsm_aprobada(datos.data)
                    elif 'HsmRechazada' in topic:
                        await orchestrator.manejador_hsm_rechazada(datos.data)
                    elif 'ValidacionAprobada' in topic:
                        await orchestrator.manejador_validacion_aprobada(datos.data)
                    elif 'ValidacionRechazada' in topic:
                        await orchestrator.manejador_validacion_rechazada(datos.data)

                    await consumidor.acknowledge(msg)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()