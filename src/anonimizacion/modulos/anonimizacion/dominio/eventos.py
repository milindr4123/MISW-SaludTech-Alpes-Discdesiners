from __future__ import annotations
from dataclasses import dataclass
from anonimizacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EventoAnonimizacion(EventoDominio):
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
class AnonimizacionCreada(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    

@dataclass
class AnonimizacionAprobada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class AnonimizacionFallida(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class AnonimizacionCompensada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None