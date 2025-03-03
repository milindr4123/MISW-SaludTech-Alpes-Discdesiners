import json
import requests
import datetime
import os

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp
from saludtech.pb2py.anonimizacion_pb2 import Anonimizacion, RespuestaAnonimizacion
from saludtech.pb2py.anonimizacion_pb2_grpc import AnonimizacionService
from saludtech.utils import dict_a_proto_datos_sensibles, dict_a_proto_tipo_informacion

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class Anonimizacion(AnonimizacionService):
    HOSTNAME_ENV: str = 'ANONIMIZACION_SERVICE_ADDRESS'
    REST_API_HOST: str = f'http://{os.getenv(HOSTNAME_ENV, default="localhost")}:5000'
    REST_API_ENDPOINT: str = '/anonimizaciones'

    def CrearAnonimizacion(self, request, context):
        dict_obj = MessageToDict(request, preserving_proto_field_name=True)
        
        r = requests.post(f'{self.REST_API_HOST}{self.REST_API_ENDPOINT}', json=dict_obj)
        if r.status_code == 200:
            respuesta = json.loads(r.text)

            timestamp_dt = datetime.datetime.strptime(respuesta['timestamp'], TIMESTAMP_FORMAT)
            timestamp = Timestamp()
            timestamp.FromDatetime(timestamp_dt)

            anonimizacion = Anonimizacion(
                anonimizacion_id=respuesta.get('anonimizacion_id'),
                datos_sensibles=dict_a_proto_datos_sensibles(respuesta.get('datos_sensibles', {})),
                tipo_informacion=dict_a_proto_tipo_informacion(respuesta.get('tipo_informacion', {})),
                imagen=respuesta.get('imagen', ''),
                timestamp=timestamp
            )

            return RespuestaAnonimizacion(mensaje='OK', anonimizacion=anonimizacion)
        else:
            return RespuestaAnonimizacion(mensaje=f'Error: {r.status_code}')

    def ConsultarAnonimizacion(self, request, context):
        # TODO: Implementar la consulta de anonimizacion
        raise NotImplementedError
