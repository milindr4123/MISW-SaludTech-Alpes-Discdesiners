import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from hsm.modulos.semilla.infraestructura.schema.v1.eventos import EventoSemillaCreada
from hsm.modulos.semilla.infraestructura.schema.v1.comandos import ComandoCrearSemilla


from hsm.modulos.semilla.infraestructura.proyecciones import ProyeccionSemillaLista, ProyeccionSemillasTotales
from hsm.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from hsm.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-semilla', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoSemillaCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionSemillasTotales(datos.fecha_creacion, ProyeccionSemillasTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionSemillasLista(datos.seed, datos.estado, datos.fecha_creacion, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-semilla', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='hsm-sub-comandos', schema=AvroSchema(ComandoCrearSemilla))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()