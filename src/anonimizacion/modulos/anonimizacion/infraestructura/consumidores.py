import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from anonimizacion.modulos.anonimizacion.infraestructura.despachadores import Despachador
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoTokenCreado
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearToken
from anonimizacion.seedwork.infraestructura import utils
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorToken
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimizacion.modulos.anonimizacion.aplicacion.comandos.crear_token import CrearToken

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('anonimizacion-solicitud-evento', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-eventos', schema=AvroSchema(EventoTokenCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'anonimizacion-solicitud - Evento recibido OKR: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
            
def crear_evento(dato):
    try:
        token_dict = dato

        map_token = MapeadorToken()
        token_dto = map_token.payload_a_dto(token_dict)

        comando = CrearToken(token_dto.id, token_dto.id_solicitud, token_dto.id_paciente, token_dto.token_anonimo, token_dto.fecha_creacion)
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        despachador = Despachador()
        despachador.publicar_evento(comando, 'anonimizacion-solicitud')
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('anonimizacion-solicitud-comando', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-comandos', schema=AvroSchema(ComandoCrearToken))

        while True:
            mensaje = consumidor.receive()
            print(f'anonimizacion-solicitud - Comando recibido: {mensaje.value().data}')
            crear_evento(mensaje.value().data)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()