from dataclasses import dataclass, field
from validacion.seedwork.aplicacion.dto import DTO

# @dataclass(frozen=True)
# class FechaTokenDTO(DTO):
#     fecha_creacion: str

@dataclass(frozen=True)
class ValidacionDTO(DTO):
    id_solicitud:str = field(default_factory=str)
    id_paciente: str = field(default_factory=str)
    token_anonimo   : str = field(default_factory=str)
    estado: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)

