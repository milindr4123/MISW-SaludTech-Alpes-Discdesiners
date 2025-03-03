from google.protobuf.timestamp_pb2 import Timestamp
from saludtech.pb2py.anonimizacion_pb2 import DatosSensibles, TipoInformacion, Anonimizacion

def dict_a_proto_datos_sensibles(dict_datos):
    return DatosSensibles(
        nombre=dict_datos.get('nombre', ''),
        fecha_nacimiento=dict_datos.get('fecha_nacimiento', ''),
        direccion=dict_datos.get('direccion', ''),
        documento_id=dict_datos.get('documento_id', '')
    )

def dict_a_proto_tipo_informacion(dict_tipo):
    return TipoInformacion(
        modalidad=dict_tipo.get('modalidad', ''),
        region_anatomica=dict_tipo.get('region_anatomica', ''),
        patologia=dict_tipo.get('patologia', '')
    )

def dict_a_proto_solicitud(dict_solicitud):
    timestamp = Timestamp()
    timestamp.FromJsonString(dict_solicitud.get('timestamp', ''))
    
    return Anonimizacion(
        solicitud_id=dict_solicitud.get('solicitud_id', ''),
        datos_sensibles=dict_a_proto_datos_sensibles(dict_solicitud.get('datos_sensibles', {})),
        tipo_informacion=dict_a_proto_tipo_informacion(dict_solicitud.get('tipo_informacion', {})),
        imagen=dict_solicitud.get('imagen', ''),
        timestamp=timestamp
    )
