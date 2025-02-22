from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import tokenizacion.modulos.tokenizacion.dominio.objetos_valor as ov
from tokenizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from tokenizacion.seedwork.dominio.eventos import PacienteRegistrado, TokenCreado

@dataclass
class Paciente(AgregacionRaiz):
    id_paciente: uuid.UUID = field(default_factory=uuid.uuid4)
    token: ov.TokenAnonimizacion = field(default_factory=ov.TokenAnonimizacion)
    fecha_registro: datetime = field(default_factory=datetime.utcnow)
    diagnosticos: list[Diagnostico] = field(default_factory=list)
    
    def registrar_paciente(self):
        self.agregar_evento(PacienteRegistrado(self.id_paciente, self.fecha_registro))
    
    def asociar_diagnostico(self, diagnostico: Diagnostico):
        self.diagnosticos.append(diagnostico)
        self.agregar_evento(DiagnosticoCreado(diagnostico.id_diagnostico, self.id_paciente))


    
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
        self.fecha_revocacion