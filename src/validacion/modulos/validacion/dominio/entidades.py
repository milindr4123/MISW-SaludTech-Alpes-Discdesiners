from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import validacion.modulos.validacion.dominio.objetos_valor as ov
from validacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from validacion.modulos.validacion.dominio.eventos import  ValidacionAprobada, ValidacionCreada, ValidacionFallida
    
# @dataclass
# class TokenValidacion(Entidad):
#     id_token: uuid.UUID = field(default_factory=uuid.uuid4)
#     valor: str = field(default_factory=lambda: str(uuid.uuid4()))
#     fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Validacion(AgregacionRaiz):
    id_solicitud: uuid.UUID = field(default_factory=uuid.uuid4)
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TextoToken = field(default_factory=ov.TextoToken)
    estado: ov.TextoToken = field(default_factory=ov.EstadoValidacion.CREADO)
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = field(default_factory=datetime.utcnow)
    
    
    def crear_validacion(self, validacion:Validacion):
        self.id_solicitud = validacion.id_solicitud
        self.id_paciente = validacion.id_paciente
        self.token_anonimo = ""
        self.estado = ov.EstadoValidacion.CREADO
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(ValidacionCreada(
            id_solicitud=self.id_solicitud,
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def aprobar_validacion(self):
        self.estado = ov.EstadoValidacion.APROBADO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(ValidacionAprobada(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def fallar_validacion(self):
        self.estado = ov.EstadoValidacion.FALLIDO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(ValidacionFallida(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))