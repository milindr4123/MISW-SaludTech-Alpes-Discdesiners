from dataclasses import dataclass, field
from tokenizacion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class FechaTokenDTO(DTO):
    fecha_creacion: str

@dataclass(frozen=True)
class TokenDTO(DTO):
    id:str = field(default_factory=str)
    id_paciente: str = field(default_factory=str)
    token_anonimo   : str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)

@dataclass(frozen=True)
class UsuarioDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    email: str = field(default_factory=str)
    tokens: list[TokenDTO] = field(default_factory=list)
    
@dataclass(frozen=True)
class DetalleTokenDTO(DTO):
    id: str
    fecha_creacion: str
    tipo: str
    estado: str
    id_paciente: str
    token_anonimo: str
    fecha_revocacion: str
    fecha_creacion: str