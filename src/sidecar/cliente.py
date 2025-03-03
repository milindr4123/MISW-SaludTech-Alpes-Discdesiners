from __future__ import print_function

from google.protobuf.timestamp_pb2 import Timestamp
from saludtech.pb2py import anonimizacion_pb2
from saludtech.pb2py import anonimizacion_pb2_grpc
from saludtech.utils import dict_a_proto_datos_sensibles, dict_a_proto_tipo_informacion

import logging
import grpc
import datetime
import os
import json


def importar_comando_anonimizacion(json_file):
    json_dict = json.load(json_file)

    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    json_dict['timestamp'] = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)

    return json_dict


def dict_a_proto_anonimizacion(dict_anonimizacion):
    return anonimizacion_pb2.Anonimizacion(
        anonimizacion_id=dict_anonimizacion.get('anonimizacion_id'),
        datos_sensibles=dict_a_proto_datos_sensibles(dict_anonimizacion.get('datos_sensibles', {})),
        tipo_informacion=dict_a_proto_tipo_informacion(dict_anonimizacion.get('tipo_informacion', {})),
        imagen=dict_anonimizacion.get('imagen', ''),
        timestamp=Timestamp().FromDatetime(datetime.datetime.strptime(dict_anonimizacion['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
    )


def run():
    print("Crear una anonimizacion")
    with grpc.insecure_channel('localhost:50051') as channel:
        json_file = open(f'{os.path.dirname(__file__)}/mensajes/crear_anonimizacion.json')
        json_dict = importar_comando_anonimizacion(json_file)
        anonimizacion = dict_a_proto_anonimizacion(json_dict)

        stub = anonimizacion_pb2_grpc.AnonimizacionServiceStub(channel)
        response = stub.CrearAnonimizacion(anonimizacion)
    print("Greeter client received: " + response.mensaje)
    print(f'Anonimizacion: {response.anonimizacion}')


if __name__ == '__main__':
    logging.basicConfig()
    run()