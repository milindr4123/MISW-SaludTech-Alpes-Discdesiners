import pulsar
from pulsar.schema import AvroSchema, Record, String, Long
from datetime import datetime
import time
from uuid import uuid4

class CrearAnonimizacionPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    token_anonimo = String()
    estado = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class ComandoCrearAnonimizacion(Record):
    correlation_id = String()
    timestamp = Long()
    data = CrearAnonimizacionPayload()


def unix_time_millis(fecha):
    """
    Convierte una fecha en formato datetime a milisegundos desde epoch.
    """
    if fecha is None:
        return 0
    epoch = datetime(1970, 1, 1)
    return int((fecha - epoch).total_seconds() * 1000)


def crear_comando_payload(evento):
    """
    Crea un payload en formato compatible con Avro basado en los datos del evento.
    """
    return CrearAnonimizacionPayload(
        id_solicitud=str(evento.id_solicitud),
        id_paciente=str(evento.id_paciente),
        fecha_creacion=unix_time_millis(evento.fecha_creacion),
        fecha_actualizacion=unix_time_millis(evento.fecha_actualizacion),
        estado=evento.estado,
        token_anonimo=str(evento.token_anonimo)
    )


def crear_comando(evento):
    """
    Crea un comando con metadatos adicionales.
    """
    return ComandoCrearAnonimizacion(
        correlation_id=str(uuid4()),
        timestamp=unix_time_millis(datetime.now()),
        data=crear_comando_payload(evento)
    )


def enviar_mensaje_a_topico(evento, topico, intentos=3):
    """
    Envía un mensaje al tópico especificado utilizando Apache Pulsar con reintentos.
    """
    cliente = pulsar.Client('pulsar://localhost:6650')

    try:
        evento_integracion = crear_comando(evento)
        
        productor = cliente.create_producer(
            topic=topico,
            schema=AvroSchema(ComandoCrearAnonimizacion)
        )
        
        for intento in range(intentos):
            try:
                productor.send(evento_integracion)
                print(f"Mensaje enviado al tópico '{topico}' exitosamente. {evento_integracion}")
                return
            except Exception as e:
                print(f"Error enviando mensaje (intento {intento + 1} de {intentos}): {e}")
                time.sleep(2 ** intento)
    finally:
        cliente.close()


if __name__ == "__main__":
    # Ejemplo de uso
    class EventoEjemplo:
        def __init__(self, id_solicitud, id_paciente, fecha_creacion, fecha_actualizacion, token_anonimo):
            self.id_solicitud = id_solicitud
            self.id_paciente = id_paciente
            self.fecha_creacion = fecha_creacion
            self.fecha_actualizacion = fecha_actualizacion
            self.estado = "CREADO"
            self.token_anonimo = token_anonimo

    evento_ejemplo = EventoEjemplo(
        id_solicitud="12345",
        id_paciente="6789011",
        fecha_creacion=datetime.now(),
        fecha_actualizacion=datetime.now(),
        token_anonimo="abcde12345",
    )

    topico = "AnonimizacionCreada"
    enviar_mensaje_a_topico(evento_ejemplo, topico)
