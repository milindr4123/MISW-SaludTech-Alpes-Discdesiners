from _future_ import annotations
from dataclasses import dataclass
from tokenizacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

@dataclass
class TokenCreado(EventoDominio):
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_creacion: datetime = None

@dataclass
class DiagnosticoAsociado(EventoDominio):
    id_paciente: uuid.UUID = None
    id_diagnostico: uuid.UUID = None
    fecha_asociacion: datetime = None

@dataclass
class ImagenAsociada(EventoDominio):
    id_paciente: uuid.UUID = None
    id_imagen: uuid.UUID = None
    fecha_asociacion: datetime = None

@dataclass
class TokenRevocado(EventoDominio):
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    fecha_revocacion: datetime = None