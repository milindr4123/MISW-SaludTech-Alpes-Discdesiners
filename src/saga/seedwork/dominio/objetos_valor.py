from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime

@dataclass(frozen=True)
class ObjetoValor:
    ...

# -------------------------
# Objetos de Valor Generales
# -------------------------
@dataclass(frozen=True)
class NombreCompleto(ObjetoValor):
    nombres: str
    apellidos: str

@dataclass(frozen=True)
class DocumentoIdentidad(ObjetoValor):
    tipo: str  # Ejemplo: CC, PASAPORTE
    numero: str

@dataclass(frozen=True)
class Direccion(ObjetoValor):
    calle: str
    ciudad: str
    pais: str

@dataclass(frozen=True)
class FechaNacimiento(ObjetoValor):
    fecha: datetime

@dataclass(frozen=True)
class CorreoElectronico(ObjetoValor):
    email: str

@dataclass(frozen=True)
class NumeroTelefono(ObjetoValor):
    codigo_pais: str
    numero: str

@dataclass(frozen=True)
class Diagnostico(ObjetoValor):
    descripcion: str
    codigo_cie10: str  # Código internacional de enfermedad (CIE-10)

@dataclass(frozen=True)
class ResultadoEstudio(ObjetoValor):
    tipo: str  # Ejemplo: Radiografía, Tomografía
    resultado: str
    fecha_realizacion: datetime

# -------------------------
# Objetos de Valor para Tokenización
# -------------------------
@dataclass(frozen=True)
class TokenPaciente(ObjetoValor):
    token: str  # UUID generado

@dataclass(frozen=True)
class SemillaCifrado(ObjetoValor):
    seed: str  # Cadena hexadecimal de la semilla

@dataclass(frozen=True)
class HashIdentidad(ObjetoValor):
    hash: str  # Representación cifrada de la identidad

@dataclass(frozen=True)
class ReferenciaToken(ObjetoValor):
    token: TokenPaciente
    tipo_registro: str  # Ejemplo: Diagnóstico, Imagen
    id_registro: str  # ID asociado al registro clínico