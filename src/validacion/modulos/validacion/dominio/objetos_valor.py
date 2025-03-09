"""Objetos valor del dominio de tokenización

En este archivo usted encontrará los objetos valor del dominio de tokenización

"""

from __future__ import annotations

from dataclasses import dataclass
from validacion.seedwork.dominio.objetos_valor import ObjetoValor
from enum import Enum
from datetime import datetime


@dataclass(frozen=True)
class TextoToken(ObjetoValor):
    texto: str  = ""

class IdPaciente(ObjetoValor):
    id_paciente:str
    
class IdSolicitud(ObjetoValor):
    id_solicitud:str
    
class TextoEstado(ObjetoValor):
    estado:str

@dataclass(frozen=True)
class Validacion(ObjetoValor):
    token: TextoToken
    id_solicitud : IdSolicitud
    id_paciente: IdPaciente
    estado: TextoEstado
    fecha_creacion: datetime = datetime.now()
    fecha_actualizacion: datetime = datetime.now()

class EstadoValidacion(str, Enum):
    CREADO = "CREADO"
    APROBADO = "APROBADO"
    FALLIDO = "FALLIDO"
    COMPENSADO = "COMPENSADO"