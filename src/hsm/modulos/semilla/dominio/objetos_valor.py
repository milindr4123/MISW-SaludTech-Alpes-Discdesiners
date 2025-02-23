
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
