from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class SemillaDTO(DTO):
    length: str
    formato: str
