from __future__ import annotations
from dataclasses import dataclass
from anonimizacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

@dataclass
class TokenCreado(EventoDominio):
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_creacion: datetime = None
