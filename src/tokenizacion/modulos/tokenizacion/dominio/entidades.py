from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import tokenizacion.modulos.tokenizacion.dominio.objetos_valor as ov
from tokenizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from tokenizacion.modulos.tokenizacion.dominio.eventos import  TokenizacionAprobada, TokenizacionCreada, TokenizacionFallida
    
# @dataclass
# class TokenTokenizacion(Entidad):
#     id_token: uuid.UUID = field(default_factory=uuid.uuid4)
#     valor: str = field(default_factory=lambda: str(uuid.uuid4()))
#     fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Tokenizacion(AgregacionRaiz):
    id_solicitud: uuid.UUID = field(default_factory=uuid.uuid4)
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TextoToken = field(default_factory=ov.TextoToken)
    estado: ov.TextoToken = field(default_factory=ov.EstadoTokenizacion.CREADO)
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = field(default_factory=datetime.utcnow)
    
    
    def crear_tokenizacion(self, tokenizacion:Tokenizacion):
        self.id_solicitud = tokenizacion.id_solicitud
        self.id_paciente = tokenizacion.id_paciente
        self.token_anonimo = ""
        self.estado = ov.EstadoTokenizacion.CREADO
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(TokenizacionCreada(
            id_solicitud=self.id_solicitud,
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def aprobar_tokenizacion(self):
        self.estado = ov.EstadoTokenizacion.APROBADO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(TokenizacionAprobada(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))
        
    def fallar_tokenizacion(self):
        self.estado = ov.EstadoTokenizacion.FALLIDO
        self.fecha_actualizacion = datetime.now()
        self.agregar_evento(TokenizacionFallida(
            id_solicitud=self.id_solicitud,
            estado=self.estado,
            fecha_actualizacion=self.fecha_actualizacion))