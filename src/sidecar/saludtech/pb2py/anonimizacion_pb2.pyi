from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatosSensibles(_message.Message):
    __slots__ = ("nombre", "fecha_nacimiento", "direccion", "documento_id")
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    FECHA_NACIMIENTO_FIELD_NUMBER: _ClassVar[int]
    DIRECCION_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTO_ID_FIELD_NUMBER: _ClassVar[int]
    nombre: str
    fecha_nacimiento: str
    direccion: str
    documento_id: str
    def __init__(self, nombre: _Optional[str] = ..., fecha_nacimiento: _Optional[str] = ..., direccion: _Optional[str] = ..., documento_id: _Optional[str] = ...) -> None: ...

class TipoInformacion(_message.Message):
    __slots__ = ("modalidad", "region_anatomica", "patologia")
    MODALIDAD_FIELD_NUMBER: _ClassVar[int]
    REGION_ANATOMICA_FIELD_NUMBER: _ClassVar[int]
    PATOLOGIA_FIELD_NUMBER: _ClassVar[int]
    modalidad: str
    region_anatomica: str
    patologia: str
    def __init__(self, modalidad: _Optional[str] = ..., region_anatomica: _Optional[str] = ..., patologia: _Optional[str] = ...) -> None: ...

class Anonimizacion(_message.Message):
    __slots__ = ("anonimizacion_id", "datos_sensibles", "tipo_informacion", "imagen", "timestamp")
    ANONIMIZACION_ID_FIELD_NUMBER: _ClassVar[int]
    DATOS_SENSIBLES_FIELD_NUMBER: _ClassVar[int]
    TIPO_INFORMACION_FIELD_NUMBER: _ClassVar[int]
    IMAGEN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    anonimizacion_id: str
    datos_sensibles: DatosSensibles
    tipo_informacion: TipoInformacion
    imagen: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, anonimizacion_id: _Optional[str] = ..., datos_sensibles: _Optional[_Union[DatosSensibles, _Mapping]] = ..., tipo_informacion: _Optional[_Union[TipoInformacion, _Mapping]] = ..., imagen: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QueryAnonimizacion(_message.Message):
    __slots__ = ("anonimizacion_id",)
    ANONIMIZACION_ID_FIELD_NUMBER: _ClassVar[int]
    anonimizacion_id: str
    def __init__(self, anonimizacion_id: _Optional[str] = ...) -> None: ...

class RespuestaAnonimizacion(_message.Message):
    __slots__ = ("mensaje", "anonimizacion")
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    ANONIMIZACION_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    anonimizacion: Anonimizacion
    def __init__(self, mensaje: _Optional[str] = ..., anonimizacion: _Optional[_Union[Anonimizacion, _Mapping]] = ...) -> None: ...
