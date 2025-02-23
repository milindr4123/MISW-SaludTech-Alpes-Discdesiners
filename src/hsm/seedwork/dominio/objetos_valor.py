"""Objetos valor reusables parte del seedwork del proyecto

En este archivo usted encontrará los objetos valor relacionados con un paciente,
asegurando el atributo de calidad de seguridad mediante anonimización.
"""

from dataclasses import dataclass, field

@dataclass(frozen=True)
class ObjetoValor:
    ...

@dataclass(frozen= True)
class Formato(ObjetoValor):
    nombre :str
@dataclass(frozen= True)
class Length(ObjetoValor):
    nombre :str
