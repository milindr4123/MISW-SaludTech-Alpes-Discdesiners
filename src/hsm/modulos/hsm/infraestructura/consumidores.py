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
from hsm.modulos.hsm.dominio.objetos_valor import EstadoHsm
from hsm.modulos.hsm.infraestructura.despachadores import Despachador
from hsm.modulos.hsm.infraestructura.schema.v1.eventos import EventoHsmCreado
from hsm.modulos.hsm.infraestructura.schema.v1.comandos import ComandoCrearHsm
from hsm.seedwork.infraestructura import utils
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsm
from hsm.seedwork.aplicacion.comandos import ejecutar_commando
from hsm.modulos.hsm.aplicacion.comandos.crear_hsm import CrearHsm
from hsm.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from hsm.modulos.hsm.infraestructura.proyecciones import ProyeccionHsmLista, ProyeccionHsmTotales

from hsm.modulos.hsm.aplicacion.comandos.aprobar_hsm import AprobarHsm

def crear_evento(dato, app):
    try:
        hsm_dict = dato

        map_hsm = MapeadorHsm()
        hsm_dto = map_hsm.payload_a_dto(hsm_dict)
        
        # Asignar un valor aleatorio a estado con 70% de probabilidad de ser APROBADO y 30% de ser FALLIDO
        estado = random.choices(
            [EstadoHsm.APROBADO.value, EstadoHsm.FALLIDO.value],
            weights=[99, 1],
            k=1
        )[0]

        comando = AprobarHsm(hsm_dto.id_solicitud, 
                                       hsm_dto.id_paciente, 
                                       hsm_dto.token_anonimo,
                                       estado,
                                       hsm_dto.fecha_creacion, 
                                       datetime.now())
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        
        # guardar en la BD
        ejecutar_proyeccion(ProyeccionHsmTotales(comando.fecha_creacion, ProyeccionHsmTotales.ADD), app=app)
        ejecutar_proyeccion(ProyeccionHsmLista(comando.id_solicitud, comando.id_paciente, comando.fecha_actualizacion, comando.estado), app=app)
            
            
        despachador = Despachador()
        if estado == EstadoHsm.APROBADO.value:
            topic = 'HsmAprobada'
        else:
            topic = 'HsmRechazada'
            
        despachador.publicar_evento(comando, topic)
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

async def suscribirse_a_comandos(app=None):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topic=['HsmCreada','HsmCompensada'], 
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name='hsm-sub-comandos', 
                schema=AvroSchema(ComandoCrearHsm)
            ) as consumidor:
                while True:
                    msg = await consumidor.receive()
                    print(msg)
                    topic = msg.topic_name()
                    datos = msg.value()
                    print(f'Evento recibido: {datos}')
                    
                    datos = msg.value().data
                    ## persistencia db
                    ejecutar_proyeccion(ProyeccionHsmTotales(datos.fecha_creacion, ProyeccionHsmTotales.ADD), app=app)
                    ejecutar_proyeccion(ProyeccionHsmLista(datos.id_solicitud, datos.id_paciente, datos.fecha_actualizacion, datos.estado), app=app)

                    # Contestar que fue exitoso o fallido
                    if 'HsmCreada' in topic:
                        crear_evento(datos, app) 

                    await consumidor.acknowledge(msg)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()