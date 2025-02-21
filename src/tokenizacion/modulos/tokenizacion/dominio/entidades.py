from _future_ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime

import tokenizacion.dominio.objetos_valor as ov
from tokenizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from tokenizacion.dominio.eventos import PacienteRegistrado, DiagnosticoCreado, ImagenAsociada

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
class Diagnostico(Entidad):
    id_diagnostico: uuid.UUID = field(default_factory=uuid.uuid4)
    descripcion: str = ""
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    imagenes: list[ImagenMedica] = field(default_factory=list)
    
    def agregar_imagen(self, imagen: ImagenMedica):
        self.imagenes.append(imagen)
        self.agregar_evento(ImagenAsociada(imagen.id_imagen, self.id_diagnostico))

@dataclass
class ImagenMedica(Entidad):
    id_imagen: uuid.UUID = field(default_factory=uuid.uuid4)
    tipo: str = ""
    url_segura: str = ""
    fecha_subida: datetime = field(default_factory=datetime.utcnow)
    
@dataclass
class TokenAnonimizacion(Entidad):
    id_token: uuid.UUID = field(default_factory=uuid.uuid4)
    valor: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_generacion: datetime = field(default_factory=datetime.utcnow)