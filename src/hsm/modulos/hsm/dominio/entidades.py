from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import hsm.modulos.hsm.dominio.objetos_valor as ov
from hsm.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from hsm.modulos.hsm.dominio.eventos import  HsmAprobada, HsmCreada, HsmFallida
    
# @dataclass
# class TokenHsm(Entidad):
#     id_token: uuid.UUID = field(default_factory=uuid.uuid4)
#     valor: str = field(default_factory=lambda: str(uuid.uuid4()))
#     fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Hsm(AgregacionRaiz):
    id_solicitud: uuid.UUID = field(default_factory=uuid.uuid4)
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TextoToken = field(default_factory=ov.TextoToken)
    estado: ov.TextoToken = field(default_factory=ov.EstadoHsm.CREADO)
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = field(default_factory=datetime.utcnow)
    
    
    def crear_hsm(self, hsm:Hsm):
        self.id_solicitud = hsm.id_solicitud
        self.id_paciente = hsm.id_paciente
        self.token_anonimo = ""
        self.estado = ov.EstadoHsm.CREADO
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(HsmCreada(
            id_solicitud=self.id_solicitud,
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def aprobar_hsm(self):
        self.estado = ov.EstadoHsm.APROBADO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(HsmAprobada(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def fallar_hsm(self):
        self.estado = ov.EstadoHsm.FALLIDO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(HsmFallida(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))