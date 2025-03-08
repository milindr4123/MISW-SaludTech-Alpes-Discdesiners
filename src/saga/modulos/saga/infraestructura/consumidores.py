import pulsar
from pulsar.schema import *
import json

from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionCreado
from saga.modulos.saga.aplicacion.saga_orchestrator import SagaOrchestrator


orchestrator = SagaOrchestrator()

async def saga_event_listener(app):
    client = pulsar.Client('pulsar://localhost:6650')
    # Suscripción a TODOS los eventos relevantes: anonimizador-eventos, tokenizacion-eventos, etc.
    # Puedes usar un patrón de topic multiplexado o suscribirte a varios en paralelo
    consumer = client.subscribe(
        topic=[
            #'AnonimizacionCreada',
            'AnonimizacionAprobada'
        ],
        subscription_name='anonimizacion-sub-comandos',
        consumer_type=pulsar.ConsumerType.Shared
    )

    while True:
        msg =  consumer.receive()
        topic = msg.topic_name()
        raw_data = msg.data()
        print(f"SagaOrchestrator topic_name recibido: {msg.topic_name()}")
        print(f"SagaOrchestrator Mensaje recibido: {msg.data()}")
        try:
            if 'AnonimizacionAprobada' in topic:
                evento = AvroSchema(ComandoCrearAnonimizacion).decode(raw_data)
                print(f"Evento de Anonimización recibido: {evento}")
                # Acceder a los atributos del payload
                if evento and evento.data:
                    print(f"ID Solicitud: {evento.data.id_solicitud}")
                    print(f"ID Paciente: {evento.data.id_paciente}")
                    print(f"Fecha Creación: {evento.data.fecha_creacion}")
                    print(f"Estado: {evento.data.estado}")
                    print(f"Token Anónimo: {evento.data.token_anonimo}")
                else:
                    print("No se encontraron datos en el evento")
                
            data = json.loads(msg.data())
            event_type = data.get("type")  # Podrías incluir un campo "type" en cada evento
            request_id = data.get("request_id")

            if event_type == "AnonymizationSucceeded":
                await orchestrator.handle_anonymization_succeeded(request_id)
            elif event_type == "AnonymizationFailed":
                await orchestrator.handle_anonymization_failed(request_id)
            # ...
            # Resto de eventos
            # TokenizationSucceeded, TokenizationFailed, etc.

            consumer.acknowledge(msg)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")
            consumer.negative_acknowledge(msg)
