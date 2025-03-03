import pulsar
from pulsar.schema import AvroSchema, Record, String, Long
from datetime import datetime

class TokenCreadoComandoPayload(Record):
    id_solicitud = String()
    id_paciente = String()
    fecha_creacion = Long()
    fecha_actualizacion = Long()

class EventoTokenComandoCreado(Record):
    data = TokenCreadoComandoPayload()
    
# Definición del esquema Avro para el payload
class TokenCreadoPayload(Record):
    id = String()
    id_paciente = String()
    token_anonimo = String()
    fecha_creacion = Long()

# Definición del esquema Avro para el evento
class EventoTokenCreado(Record):
    data = TokenCreadoPayload()

def unix_time_millis(fecha):
    """
    Convierte una fecha en formato datetime a milisegundos desde epoch.
    """
    epoch = datetime(1970, 1, 1)
    return int((fecha - epoch).total_seconds() * 1000)

def crear_payload(evento):
    """
    Crea un payload en formato compatible con Avro basado en los datos del evento.
    """
    return TokenCreadoPayload(
        id=str(evento.id),
        id_paciente=str(evento.id_paciente),
        token_anonimo=str(evento.token_anonimo),
        fecha_creacion=unix_time_millis(evento.fecha_creacion)
    )
    
def crear_comando_payload(evento):
    """
    Crea un payload en formato compatible con Avro basado en los datos del evento.
    """
    return TokenCreadoComandoPayload(
        id_solicitud=str(evento.id_solicitud),        
        id_paciente=str(evento.id_paciente),
        fecha_creacion = unix_time_millis(evento.fecha_creacion),
        fecha_actualizacion = unix_time_millis(evento.fecha_creacion)
    )

def enviar_mensaje_a_topico(evento, topico):
    """
    Envía un mensaje al tópico especificado utilizando Apache Pulsar.
    """
    # Crear el payload
    payload = crear_comando_payload(evento)
    
    # Crear el evento de integración
    evento_integracion = EventoTokenComandoCreado(data=payload)

    # Configurar el cliente Pulsar
    cliente = pulsar.Client('pulsar://localhost:6650')  # Cambia la URL si es necesario

    try:
        # Crear un productor para el tópico con el esquema Avro
        productor = cliente.create_producer(
            topic=topico,
            schema=AvroSchema(EventoTokenComandoCreado)
        )

        # Enviar el mensaje
        productor.send(evento_integracion)
        print(f"Mensaje enviado al tópico '{topico}' exitosamente. {evento_integracion}")
    finally:
        # Cerrar el cliente Pulsar
        cliente.close()

if __name__ == "__main__":
    # Ejemplo de uso
    class EventoEjemplo:
        def __init__(self, id_solicitud, id_paciente, token_anonimo, fecha_creacion):
            self.id_solicitud = id_solicitud
            self.id_paciente = id_paciente
            self.token_anonimo = token_anonimo
            self.fecha_creacion = fecha_creacion

    # Datos de ejemplo para el evento
    evento_ejemplo = EventoEjemplo(
        id_solicitud="12345",
        id_paciente="6789011",
        token_anonimo="abcde12345",
        fecha_creacion=datetime.now()
    )

    # Tópico al que se enviará el mensaje
    topico = "anonimizacion-solicitud-comando"

    # Enviar el mensaje
    enviar_mensaje_a_topico(evento_ejemplo, topico)