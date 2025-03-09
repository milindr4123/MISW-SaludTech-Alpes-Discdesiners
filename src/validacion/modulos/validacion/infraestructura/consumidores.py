from datetime import datetime
import aiopulsar
import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
import random
from validacion.modulos.validacion.dominio.objetos_valor import EstadoValidacion
from validacion.modulos.validacion.infraestructura.despachadores import Despachador
from validacion.modulos.validacion.infraestructura.schema.v1.eventos import EventoValidacionCreado
from validacion.modulos.validacion.infraestructura.schema.v1.comandos import ComandoCrearValidacion
from validacion.seedwork.infraestructura import utils
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacion
from validacion.seedwork.aplicacion.comandos import ejecutar_commando
from validacion.modulos.validacion.aplicacion.comandos.crear_validacion import CrearValidacion
from validacion.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from validacion.modulos.validacion.infraestructura.proyecciones import ProyeccionValidacionLista, ProyeccionValidacionTotales
from validacion.seedwork.infraestructura.timeUtils import unix_time_millis
from validacion.modulos.validacion.aplicacion.comandos.aprobar_validacion import AprobarValidacion

def crear_evento(dato, app):
    try:
        validacion_dict = dato

        map_validacion = MapeadorValidacion()
        validacion_dto = map_validacion.payload_a_dto(validacion_dict)
        
        # Asignar un valor aleatorio a estado con 70% de probabilidad de ser APROBADO y 30% de ser FALLIDO
        estado = random.choices(
            [EstadoValidacion.APROBADO.value, EstadoValidacion.FALLIDO.value],
            weights=[1, 99],
            k=1
        )[0]

        comando = AprobarValidacion(validacion_dto.id_solicitud, 
                                       validacion_dto.id_paciente, 
                                       validacion_dto.token_anonimo,
                                       estado,
                                       int(unix_time_millis(datetime.now())),
                                       int(unix_time_millis(datetime.now())))
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        
        # guardar en la BD
        ejecutar_proyeccion(ProyeccionValidacionTotales(comando.fecha_creacion, ProyeccionValidacionTotales.ADD), app=app)
        ejecutar_proyeccion(ProyeccionValidacionLista(comando.id_solicitud, comando.id_paciente, comando.fecha_actualizacion, comando.estado), app=app)
            
            
        despachador = Despachador()
        if estado == EstadoValidacion.APROBADO.value:
            topic = 'ValidacionAprobada'
        else:
            topic = 'ValidacionRechazada'
            
        despachador.publicar_evento(comando, topic)
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

async def suscribirse_a_comandos(app=None):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topic=['ValidacionCreada','ValidacionCompensada'], 
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='validacion-sub-comandos', 
                schema=AvroSchema(ComandoCrearValidacion)
            ) as consumidor:
                while True:
                    msg = await consumidor.receive()
                    print(msg)
                    topic = msg.topic_name()
                    datos = msg.value()
                    print(f'Evento recibido: {datos}')
                    
                    datos = msg.value().data
                    ## persistencia db
                    ejecutar_proyeccion(ProyeccionValidacionTotales(datos.fecha_creacion, ProyeccionValidacionTotales.ADD), app=app)
                    ejecutar_proyeccion(ProyeccionValidacionLista(datos.id_solicitud, datos.id_paciente, datos.fecha_actualizacion, datos.estado), app=app)

                    # Contestar que fue exitoso o fallido
                    if 'ValidacionCreada' in topic:
                        crear_evento(datos, app) 

                    await consumidor.acknowledge(msg)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()