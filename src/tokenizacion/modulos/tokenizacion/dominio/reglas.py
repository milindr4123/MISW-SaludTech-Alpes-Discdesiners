"""Reglas de negocio del dominio de tokenización

En este archivo usted encontrará reglas de negocio del dominio de tokenización

"""

from tokenizacion.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Tokenizacion
from datetime import datetime

class TokenNoExpirado(ReglaNegocio):

    token: Tokenizacion

    def __init__(self, token, mensaje='El token ha expirado'):
        super().__init__(mensaje)
        self.token = token

    def es_valido(self) -> bool:
        return self.tokenizacion.es_valido()

class TextoTokenValido(ReglaNegocio):

    texto: str

    def __init__(self, texto, mensaje='El texto del token no es válido'):
        super().__init__(mensaje)
        self.texto = texto

    def es_valido(self) -> bool:
        return bool(self.texto) and len(self.texto) > 0

class FechaTokenValida(ReglaNegocio):

    fecha_token: datetime

    def __init__(self, fecha_token, mensaje='La fecha del token no es válida'):
        super().__init__(mensaje)
        self.fecha_token = fecha_token

    def es_valido(self) -> bool:
        return self.fecha_token.fecha_expiracion > self.fecha_token.fecha_creacion