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



def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('AnonimizacionCreada-evento', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-eventos', schema=AvroSchema(EventoAnonimizacionCreado))

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
        anonimizacion_dict = dato

        map_anonimizacion = MapeadorAnonimizacion()
        anonimizacion_dto = map_anonimizacion.payload_a_dto(anonimizacion_dict)
        
        # Asignar un valor aleatorio a estado con 70% de probabilidad de ser APROBADO y 30% de ser FALLIDO
        estado = random.choices(
            [EstadoAnonimizacion.APROBADO, EstadoAnonimizacion.FALLIDO],
            weights=[70, 30],
            k=1
        )[0]

        comando = AprobarAnonimizacion(anonimizacion_dto.id, anonimizacion_dto.id_solicitud, anonimizacion_dto.id_paciente, anonimizacion_dto.token_anonimo, anonimizacion_dto.fecha_creacion, estado)
        
        # TODO Reemplaze este código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        despachador = Despachador()
        despachador.publicar_evento(comando, 'AnonimizacionAprobada')
        

    except Exception as e:
        return print(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('AnonimizacionCreada', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimizacion-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'anonimizacion-solicitud - Comando recibido: {datos}')
            
            ## persistencia db
            ejecutar_proyeccion(ProyeccionAnonimizacionTotales(datos.fecha_creacion, ProyeccionAnonimizacionTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionAnonimizacionLista(datos.id_solicitud, datos.id_paciente, datos.fecha_actualizacion, datos.estado), app=app)
            
            
            # Contestar que fue exitoso o fallido
            crear_evento(datos) 
            
            
            

            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()