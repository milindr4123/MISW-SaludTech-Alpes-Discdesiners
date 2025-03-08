import pulsar
from pulsar.schema import AvroSchema, Record, String, Long
from datetime import datetime

from saga.modulos.saga.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, CrearAnonimizacionPayload
from saga.seedwork.infraestructura.utils import unix_time_millis

from saga.modulos.saga.infraestructura.despachadores import DespachadorComandos
    
class ManejarAnominizacionEvento:


    async def enviar_mensaje_anonimizacion(evento, topico):
        """
        Envía un mensaje al tópico especificado utilizando Apache Pulsar.
        """
        # Crear el payload
        payload = CrearAnonimizacionPayload(
            id_solicitud=str(evento.id_solicitud),        
            id_paciente=str(evento.id_paciente),
            fecha_creacion = unix_time_millis(evento.fecha_creacion),
            fecha_actualizacion = unix_time_millis(evento.fecha_creacion)
        )
        # Crear el evento
        evento_integracion = ComandoCrearAnonimizacion(data=payload)
        
        await DespachadorComandos.publicar_mensaje_async(evento_integracion, topico, AvroSchema(ComandoCrearAnonimizacion))
        # # Crear el cliente
        # cliente = pulsar.Client(f'pulsar://localhost:6650')
        # # Crear el productor
        # publicador = cliente.create_producer(topico, schema=AvroSchema(EventoAnonimizacionComandoCreado))
        # # Enviar el mensaje
        # publicador.send(evento_integracion)
        # # Cerrar el cliente
        # cliente.close()