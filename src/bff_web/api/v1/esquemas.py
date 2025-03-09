import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


SALUDTECH_HOST = os.getenv("SALUDTECH_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
def obtener_anonimizaciones(root) -> typing.List["Anonimizacion"]:
    anonimizaciones_json = requests.get(f'http://{SALUDTECH_HOST}:5000/saludtech/anonimizacion').json()
    anonimizaciones = []

    for anonimizacion in anonimizaciones_json:
        anonimizaciones.append(
            Anonimizacion(
                solicitud_id=anonimizacion.get('solicitud_id'),
                datos_sensibles=DatosSensibles(
                    nombre=anonimizacion['datos_sensibles'].get('nombre'),
                    fecha_nacimiento=anonimizacion['datos_sensibles'].get('fecha_nacimiento'),
                    direccion=anonimizacion['datos_sensibles'].get('direccion'),
                    documento_id=anonimizacion['datos_sensibles'].get('documento_id')
                ),
                tipo_informacion=TipoInformacion(
                    modalidad=anonimizacion['tipo_informacion'].get('modalidad'),
                    region_anatomica=anonimizacion['tipo_informacion'].get('region_anatomica'),
                    patologia=anonimizacion['tipo_informacion'].get('patologia')
                ),
                imagen=anonimizacion.get('imagen'),
                timestamp=datetime.strptime(anonimizacion.get('timestamp'), FORMATO_FECHA)
            )
        )

    return anonimizaciones


@strawberry.type
class DatosSensibles:
    nombre: str
    fecha_nacimiento: str
    direccion: str
    documento_id: str


@strawberry.type
class TipoInformacion:
    modalidad: str
    region_anatomica: str
    patologia: str


@strawberry.type
class Anonimizacion:
    solicitud_id: str
    datos_sensibles: DatosSensibles
    tipo_informacion: TipoInformacion
    imagen: str
    timestamp: datetime
