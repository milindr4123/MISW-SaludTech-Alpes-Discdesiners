"""Mixins del dominio de tokenización

En este archivo usted encontrará las Mixins con capacidades 
reusables en el dominio de tokenización

"""

from .entidades import Token

class FiltradoTokensMixin:

    def filtrar_mejores_tokens(self, tokens: list[Token]) -> list[Token]:
        # Lógica compleja para filtrar tokens
        # TODO
        return tokens