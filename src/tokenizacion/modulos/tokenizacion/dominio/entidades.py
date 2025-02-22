from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import tokenizacion.modulos.tokenizacion.dominio.objetos_valor as ov
from tokenizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenCreado, TokenRevocado
    
@dataclass
class TokenAnonimizacion(Entidad):
    id_token: uuid.UUID = field(default_factory=uuid.uuid4)
    valor: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Token(AgregacionRaiz):
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TokenAnonimizacion = field(default_factory=ov.TokenAnonimizacion)
    
    
    def crear_token(self, token:Token):
        self.id_paciente = token.id_paciente
        self.token_anonimo = token.token_anonimo
        self.agregar_evento(TokenCreado(
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            fecha_creacion=self.fecha_creacion))
        
    def revocar_token(self):
        self.agregar_evento(TokenRevocado(
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            fecha_revocacion=self.fecha_revocacion))