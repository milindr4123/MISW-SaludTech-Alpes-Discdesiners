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

class TipoToken(Enum):
    ACCESO = "Acceso"
    REFRESCO = "Refresco"
    
class EstadoToken(Enum):
    ACCESO = "Activo"
    REFRESCO = "Retirado"
    
class IdUsuarioToken(ObjetoValor):
    id_usuario:str

@dataclass(frozen=True)
class Token(ObjetoValor):
    texto: TextoToken
    tipo: TipoToken
    estado: EstadoToken
    id_usuario: IdUsuarioToken

    def obtener_tipo(self) -> TipoToken:
        return self.tipo
    
    
@dataclass(frozen=True)
class DetalleToken(ObjetoValor):
    id: str
    fecha_creacion: datetime
    fecha_expiracion: datetime
    tipo: TipoToken
    estado: str
    id_paciente: str
    token_anonimo: str
    fecha_revocacion: datetime
    fecha_creacion: datetime