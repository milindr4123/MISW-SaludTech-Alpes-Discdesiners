"""Objetos valor reusables parte del seedwork del proyecto

En este archivo usted encontrará los objetos valor relacionados con un paciente,
asegurando el atributo de calidad de seguridad mediante anonimización.
"""

from dataclasses import dataclass, field

@dataclass(frozen=True)
class ObjetoValor:
    ...

@dataclass(frozen=True)
class GeneradorSeed(ObjetoValor):
    """Representa un generador de semillas con parámetros específicos."""
    operation: str = field(default="generate_seed")
    length: int = field(default=32)
    format: str = field(default="hex")
