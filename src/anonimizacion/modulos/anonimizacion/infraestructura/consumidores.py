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
from anonimizacion.modulos.anonimizacion.dominio.objetos_valor import EstadoAnonimizacion
from anonimizacion.modulos.anonimizacion.infraestructura.despachadores import Despachador
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionCreado
from anonimizacion.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion
from anonimizacion.seedwork.infraestructura import utils
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from anonimizacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimizacion.modulos.anonimizacion.aplicacion.comandos.crear_anonimizacion import CrearAnonimizacion
from anonimizacion.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from anonimizacion.modulos.anonimizacion.infraestructura.proyecciones import ProyeccionAnonimizacionLista, ProyeccionAnonimizacionTotales

from anonimizacion.modulos.anonimizacion.aplicacion.comandos.aprobar_anonimizacion import AprobarAnonimizacion
from anonimizacion.seedwork.infraestructura.timeUtils import unix_time_millis

def crear_evento(dato, app):
    try:
        anonimizacion_dict = dato

        map_anonimizacion = MapeadorAnonimizacion()
        anonimizacion_dto = map_anonimizacion.payload_a_dto(anonimizacion_dict)
        
        # Asignar un valor aleatorio a estado con 70% de probabilidad de ser APROBADO y 30% de ser FALLIDO
        estado = random.choices(
            [EstadoAnonimizacion.APROBADO.value, EstadoAnonimizacion.FALLIDO.value],
            weights=[99, 1],
            k=1
        )[0]

        comando = AprobarAnonimizacion(anonimizacion_dto.id_solicitud, 
                                       anonimizacion_dto.id_paciente, 
                                       anonimizacion_dto.token_anonimo,
                                       estado,
                                       int(unix_time_millis(datetime.now())),
                                       int(unix_time_millis(datetime.now()))
                                       )
                                       
        
        # guardar en la BD
        ejecutar_proyeccion(ProyeccionAnonimizacionTotales(comando.fecha_creacion, ProyeccionAnonimizacionTotales.ADD), app=app)
        ejecutar_proyeccion(ProyeccionAnonimizacionLista(comando.id_solicitud, comando.id_paciente, comando.fecha_actualizacion, comando.estado), app=app)
            
            
        despachador = Despachador()
        if estado == EstadoAnonimizacion.APROBADO.value:
            topic = 'AnonimizacionAprobada'
        else:
            topic = 'AnonimizacionRechazada'
            
        despachador.publicar_evento(comando, topic)
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

async def suscribirse_a_comandos(app=None):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topic=['AnonimizacionCreada','AnonimizacionCompensada'], 
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='anonimizacion-sub-comandos', 
                schema=AvroSchema(ComandoCrearAnonimizacion)
            ) as consumidor:
                while True:
                    msg = await consumidor.receive()
                    print(msg)
                    topic = msg.topic_name()
                    datos = msg.value()
                    print(f'Evento recibido: {datos}')
                    
                    datos = msg.value().data
                    ## persistencia db
                    ejecutar_proyeccion(ProyeccionAnonimizacionTotales(datos.fecha_creacion, ProyeccionAnonimizacionTotales.ADD), app=app)
                    ejecutar_proyeccion(ProyeccionAnonimizacionLista(datos.id_solicitud, datos.id_paciente, datos.fecha_actualizacion, datos.estado), app=app)

                    # Contestar que fue exitoso o fallido
                    if 'AnonimizacionCreada' in topic:
                        crear_evento(datos, app) 

                    await consumidor.acknowledge(msg)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()