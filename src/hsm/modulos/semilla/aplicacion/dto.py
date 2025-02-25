from dataclasses import dataclass, field
from hsm.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class SemillaDTO(DTO):
    length: str
    formato: str
