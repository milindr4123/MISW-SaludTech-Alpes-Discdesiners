import pulsar
from pulsar.schema import *

from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionCreado, AnonimizacionCreadoPayload
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion, CrearAnonimizacionPayload
from anonimizacion.seedwork.infraestructura import utils
from anonimizacion.seedwork.infraestructura.timeUtils import unix_time_millis

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = AnonimizacionCreadoPayload(
            id_solicitud=str(evento.id_solicitud), 
            id_paciente=str(evento.id_paciente), 
            token_anonimo=str(evento.token_anonimo),
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion)),
            fecha_actualizacion=int(unix_time_millis(evento.fecha_actualizacion))
        )
        evento_integracion = EventoAnonimizacionCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoAnonimizacionCreado))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = CrearAnonimizacionPayload(
            id_solicitud=str(comando.id_solicitud), 
            id_paciente=str(comando.id_paciente), 
            token_anonimo=str(comando.token_anonimo),
            estado=str(comando.estado), 
            fecha_creacion=int(unix_time_millis(comando.fecha_creacion)),
            fecha_actualizacion=int(unix_time_millis(comando.fecha_actualizacion))
            # agregar otros campos necesarios
        )
        comando_integracion = ComandoCrearAnonimizacion(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearAnonimizacion))