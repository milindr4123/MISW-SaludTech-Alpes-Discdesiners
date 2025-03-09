from __future__ import annotations
from dataclasses import dataclass
from hsm.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EventoHsm(EventoDominio):
    ...

@dataclass
class TokenCreadoMMM(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None


@dataclass
class HsmCreada(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    

@dataclass
class HsmAprobada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class HsmFallida(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class HsmCompensada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None