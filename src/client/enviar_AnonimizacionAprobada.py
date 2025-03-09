import pulsar
from pulsar.schema import AvroSchema, Record, String, Long
from datetime import datetime

from anonimizacion.comandos import ComandoCrearAnonimizacion, CrearAnonimizacionPayload


    

def unix_time_millis(fecha):
    """
    Convierte una fecha en formato datetime a milisegundos desde epoch.
    """
    epoch = datetime(1970, 1, 1)
    return int((fecha - epoch).total_seconds() * 1000)


    
def crear_comando_payload(evento):
    """
    Crea un payload en formato compatible con Avro basado en los datos del evento.
    """
    return CrearAnonimizacionPayload(
        id_solicitud=str(evento.id_solicitud),        
        id_paciente=str(evento.id_paciente),
        fecha_creacion = unix_time_millis(evento.fecha_creacion),
        fecha_actualizacion = unix_time_millis(evento.fecha_creacion),
        estado = evento.estado, 
        token_anonimo = str(evento.token_anonimo)
    )

def enviar_mensaje_a_topico(evento, topico):
    """
    Envía un mensaje al tópico especificado utilizando Apache Pulsar.
    """
    # Crear el payload
    payload = crear_comando_payload(evento)
    
    # Crear el evento de integración
    evento_integracion = ComandoCrearAnonimizacion(data=payload)

    # Configurar el cliente Pulsar
    cliente = pulsar.Client('pulsar://localhost:6650')  # Cambia la URL si es necesario

    try:
        # Crear un productor para el tópico con el esquema Avro
        productor = cliente.create_producer(
            topic=topico,
            schema=AvroSchema(ComandoCrearAnonimizacion)
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
        def __init__(self, id_solicitud, id_paciente, fecha_creacion, fecha_actualizacion, token_anonimo):
            self.id_solicitud = id_solicitud
            self.id_paciente = id_paciente
            self.fecha_creacion = fecha_creacion
            self.fecha_actualizacion = fecha_actualizacion
            self.estado = "CREADO"
            self.token_anonimo = token_anonimo

    # Datos de ejemplo para el evento
    evento_ejemplo = EventoEjemplo(
        id_solicitud="12345",
        id_paciente="6789011",
        fecha_creacion=datetime.now(),
        fecha_actualizacion=datetime.now(),
        token_anonimo="abcde12345",
    )

    # Tópico al que se enviará el mensaje
    topico = "AnonimizacionAprobada"

    # Enviar el mensaje
    enviar_mensaje_a_topico(evento_ejemplo, topico)