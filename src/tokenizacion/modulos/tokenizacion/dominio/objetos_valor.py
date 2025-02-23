"""Objetos valor del dominio de tokenización

En este archivo usted encontrará los objetos valor del dominio de tokenización

"""

from __future__ import annotations

from dataclasses import dataclass
from tokenizacion.seedwork.dominio.objetos_valor import ObjetoValor
from enum import Enum
from datetime import datetime


@dataclass(frozen=True)
class TextoToken(ObjetoValor):
    texto: str
    
@dataclass(frozen=True)
class FechaToken(ObjetoValor):
    fecha_creacion: datetime


    
class IdPaciente(ObjetoValor):
    id_paciente:str

@dataclass(frozen=True)
class Token(ObjetoValor):
    token: TextoToken
    id_paciente: IdPaciente
    fecha_creacion: FechaToken

    
    
@dataclass(frozen=True)
class DetalleToken(ObjetoValor):
    id: str
    fecha_creacion: FechaToken
    fecha_expiracion: FechaToken
    tipo: TipoToken
    estado: EstadoToken
    id_paciente: IdPaciente
    token_anonimo: TextoToken
    fecha_revocacion: FechaToken
    fecha_creacion: FechaToken