import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from validacion.modulos.validacion.infraestructura.despachadores import Despachador
from validacion.modulos.validacion.infraestructura.schema.v1.eventos import EventoTokenCreado
from validacion.modulos.validacion.infraestructura.schema.v1.comandos import ComandoCrearToken
from validacion.seedwork.infraestructura import utils
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorToken
from validacion.seedwork.aplicacion.comandos import ejecutar_commando
from validacion.modulos.validacion.aplicacion.comandos.crear_token import CrearToken
from validacion.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from validacion.modulos.validacion.infraestructura.proyecciones import ProyeccionTokenLista, ProyeccionTokenTotales

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('validacion-solicitud-evento', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='validacion-sub-eventos', schema=AvroSchema(EventoTokenCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'validacion-solicitud - Evento recibido OKR: {mensaje.value().data}')

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
        despachador.publicar_evento(comando, 'validacion-solicitud')
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('validacion-solicitud-comando', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='validacion-sub-comandos', schema=AvroSchema(ComandoCrearToken))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'validacion-solicitud - Comando recibido: {datos}')
            
            ## persistencia db
            ejecutar_proyeccion(ProyeccionTokenTotales(datos.fecha_creacion, ProyeccionTokenTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionTokenLista(datos.id_solicitud, datos.id_paciente, datos.fecha_creacion), app=app)
            
            crear_evento(datos)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()