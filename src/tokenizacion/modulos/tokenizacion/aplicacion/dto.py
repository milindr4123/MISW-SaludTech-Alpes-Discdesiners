from dataclasses import dataclass, field
from tokenizacion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class FechaTokenDTO(DTO):
    fecha_creacion: str

@dataclass(frozen=True)
class TokenDTO(DTO):
    codigo: str
    texto: str
    fecha: FechaTokenDTO
    tipo: str

@dataclass(frozen=True)
class UsuarioDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    email: str = field(default_factory=str)
    tokens: list[TokenDTO] = field(default_factory=list)