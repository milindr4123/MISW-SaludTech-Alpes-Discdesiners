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
from tokenizacion.modulos.tokenizacion.dominio.objetos_valor import EstadoTokenizacion
from tokenizacion.modulos.tokenizacion.infraestructura.despachadores import Despachador
from tokenizacion.modulos.tokenizacion.infraestructura.schema.v1.eventos import EventoTokenizacionCreado
from tokenizacion.modulos.tokenizacion.infraestructura.schema.v1.comandos import ComandoCrearTokenizacion
from tokenizacion.seedwork.infraestructura import utils
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacion
from tokenizacion.seedwork.aplicacion.comandos import ejecutar_commando
from tokenizacion.modulos.tokenizacion.aplicacion.comandos.crear_tokenizacion import CrearTokenizacion
from tokenizacion.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from tokenizacion.modulos.tokenizacion.infraestructura.proyecciones import ProyeccionTokenizacionLista, ProyeccionTokenizacionTotales

from tokenizacion.modulos.tokenizacion.aplicacion.comandos.aprobar_tokenizacion import AprobarTokenizacion

def crear_evento(dato, app):
    try:
        tokenizacion_dict = dato

        map_tokenizacion = MapeadorTokenizacion()
        tokenizacion_dto = map_tokenizacion.payload_a_dto(tokenizacion_dict)
        
        # Asignar un valor aleatorio a estado con 70% de probabilidad de ser APROBADO y 30% de ser FALLIDO
        estado = random.choices(
            [EstadoTokenizacion.APROBADO.value, EstadoTokenizacion.FALLIDO.value],
            weights=[99, 1],
            k=1
        )[0]

        comando = AprobarTokenizacion(tokenizacion_dto.id_solicitud, 
                                       tokenizacion_dto.id_paciente, 
                                       tokenizacion_dto.token_anonimo,
                                       estado,
                                       tokenizacion_dto.fecha_creacion, 
                                       datetime.now())
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        
        # guardar en la BD
        ejecutar_proyeccion(ProyeccionTokenizacionTotales(comando.fecha_creacion, ProyeccionTokenizacionTotales.ADD), app=app)
        ejecutar_proyeccion(ProyeccionTokenizacionLista(comando.id_solicitud, comando.id_paciente, comando.fecha_actualizacion, comando.estado), app=app)
            
            
        despachador = Despachador()
        if estado == EstadoTokenizacion.APROBADO.value:
            topic = 'TokenizacionAprobada'
        else:
            topic = 'TokenizacionRechazada'
            
        despachador.publicar_evento(comando, topic)
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

async def suscribirse_a_comandos(app=None):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topic=['TokenizacionCreada','TokenizacionCompensada'], 
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='tokenizacion-sub-comandos', 
                schema=AvroSchema(ComandoCrearTokenizacion)
            ) as consumidor:
                while True:
                    msg = await consumidor.receive()
                    print(msg)
                    topic = msg.topic_name()
                    datos = msg.value()
                    print(f'Evento recibido: {datos}')
                    
                    datos = msg.value().data
                    ## persistencia db
                    ejecutar_proyeccion(ProyeccionTokenizacionTotales(datos.fecha_creacion, ProyeccionTokenizacionTotales.ADD), app=app)
                    ejecutar_proyeccion(ProyeccionTokenizacionLista(datos.id_solicitud, datos.id_paciente, datos.fecha_actualizacion, datos.estado), app=app)

                    # Contestar que fue exitoso o fallido
                    if 'TokenizacionCreada' in topic:
                        crear_evento(datos, app) 

                    await consumidor.acknowledge(msg)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()