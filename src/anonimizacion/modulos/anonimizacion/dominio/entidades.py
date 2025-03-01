from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import anonimizacion.modulos.anonimizacion.dominio.objetos_valor as ov
from anonimizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from anonimizacion.modulos.anonimizacion.dominio.eventos import TokenCreado
    
# @dataclass
# class TokenAnonimizacion(Entidad):
#     id_token: uuid.UUID = field(default_factory=uuid.uuid4)
#     valor: str = field(default_factory=lambda: str(uuid.uuid4()))
#     fecha_generacion: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class Token(AgregacionRaiz):
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token_anonimo: ov.TextoToken = field(default_factory=ov.TextoToken)
    # fecha_creacion: ov.FechaToken = field(default_factory=ov.FechaToken)
    
    
    def crear_token(self, token:Token):
        self.id_paciente = token.id_paciente
        self.token_anonimo = token.token_anonimo
        self.agregar_evento(TokenCreado(
            id_paciente=self.id_paciente,
            token_anonimo=self.token_anonimo,
            fecha_creacion=self.fecha_creacion))