from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import anonimizacion.modulos.anonimizacion.dominio.objetos_valor as ov
from anonimizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from anonimizacion.modulos.anonimizacion.dominio.eventos import  AnonimizacionAprobada, AnonimizacionCreada, AnonimizacionFallida
    
# @dataclass
# class TokenAnonimizacion(Entidad):
#     id_token: uuid.UUID = field(default_factory=uuid.uuid4)
#     valor: str = field(default_factory=lambda: str(uuid.uuid4()))
#     fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Anonimizacion(AgregacionRaiz):
    id_solicitud: uuid.UUID = field(default_factory=uuid.uuid4)
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TextoToken = field(default_factory=ov.TextoToken)
    estado: ov.TextoToken = field(default_factory=ov.EstadoAnonimizacion.CREADO)
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = field(default_factory=datetime.utcnow)
    
    
    def crear_anonimizacion(self, anonimizacion:Anonimizacion):
        self.id_solicitud = anonimizacion.id_solicitud
        self.id_paciente = anonimizacion.id_paciente
        self.token_anonimo = ""
        self.estado = ov.EstadoAnonimizacion.CREADO
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(AnonimizacionCreada(
            id_solicitud=self.id_solicitud,
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def aprobar_anonimizacion(self):
        self.estado = ov.EstadoAnonimizacion.APROBADO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(AnonimizacionAprobada(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def fallar_anonimizacion(self):
        self.estado = ov.EstadoAnonimizacion.FALLIDO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(AnonimizacionFallida(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))