from __future__ import annotations
from dataclasses import dataclass
from tokenizacion.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EventoTokenizacion(EventoDominio):
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
class TokenizacionCreada(EventoDominio):
    id_solicitud: uuid.UUID = None
    id_paciente: uuid.UUID = None
    token_anonimo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    

@dataclass
class TokenizacionAprobada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class TokenizacionFallida(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None
    
@dataclass
class TokenizacionCompensada(EventoDominio):
    id_solicitud: uuid.UUID = None
    estado: str = None
    fecha_actualizacion: datetime = None