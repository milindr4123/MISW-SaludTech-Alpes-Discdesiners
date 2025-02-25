from __future__ import annotations
from dataclasses import dataclass, field
from hsm.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoSemilla(EventoDominio):
    ...

@dataclass
class SemillaCreada(EventoSemilla):
    length: str = None
    format: str = None