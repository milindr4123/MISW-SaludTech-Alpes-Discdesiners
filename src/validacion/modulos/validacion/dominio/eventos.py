from __future__ import annotations
from dataclasses import dataclass
from validacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

@dataclass
class TokenCreado(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_creacion: datetime = None
