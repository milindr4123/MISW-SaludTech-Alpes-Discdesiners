"""Objetos valor del dominio de tokenización

En este archivo usted encontrará los objetos valor del dominio de tokenización

"""

from __future__ import annotations

from dataclasses import dataclass
from tokenizacion.seedwork.dominio.objetos_valor import ObjetoValor
from enum import Enum


@dataclass(frozen=True)
class TextoToken(ObjetoValor):
    texto: str

class TipoToken(Enum):
    ACCESO = "Acceso"
    REFRESCO = "Refresco"

@dataclass(frozen=True)
class Token(ObjetoValor):
    codigo: CodigoToken
    texto: TextoToken
    tipo: TipoToken

    def obtener_tipo(self) -> TipoToken:
        return self.tipo