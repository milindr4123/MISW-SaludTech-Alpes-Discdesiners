from __future__ import annotations
from dataclasses import dataclass
from validacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EventoValidacion(EventoDominio):
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
class ValidacionCreada(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    

@dataclass
class ValidacionAprobada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class ValidacionFallida(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class ValidacionCompensada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None