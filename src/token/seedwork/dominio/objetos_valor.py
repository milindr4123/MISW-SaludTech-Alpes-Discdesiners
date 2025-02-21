"""Objetos valor reusables parte del seedwork del proyecto

En este archivo usted encontrará los objetos valor relacionados con un paciente,
asegurando el atributo de calidad de seguridad mediante anonimización.

"""

from dataclasses import dataclass
from abc import ABC
import hashlib

@dataclass(frozen=True)
class ObjetoValor:
    ...

@dataclass(frozen=True)
class IdentificadorAnonimo(ABC, ObjetoValor):
    """Representa un identificador único y anonimizado de un paciente usando SHA-256."""
    hash_id: str

    @staticmethod
    def generar(entrada: str) -> "IdentificadorAnonimo":
        hash_object = hashlib.sha256(entrada.encode("utf-8"))
        return IdentificadorAnonimo(hash_id=hash_object.hexdigest())

@dataclass(frozen=True)
class NombrePaciente(ObjetoValor):
    """Representa el nombre del paciente pero no se almacena directamente en el sistema."""
    nombre_ofuscado: str

    @staticmethod
    def ofuscar(nombre_real: str) -> "NombrePaciente":
        hash_object = hashlib.sha256(nombre_real.encode("utf-8"))
        return NombrePaciente(nombre_ofuscado=hash_object.hexdigest())

@dataclass(frozen=True)
class EdadPaciente(ObjetoValor):
    """Representa la edad del paciente en años."""
    edad: int

@dataclass(frozen=True)
class GeneroPaciente(ObjetoValor):
    """Representa el género del paciente como un valor inmutable."""
    genero: str  # Puede ser 'Masculino', 'Femenino', 'No Binario', etc.

@dataclass(frozen=True)
class TipoSangre(ObjetoValor):
    """Representa el tipo de sangre del paciente como un valor inmutable."""
    tipo: str  # Ejemplo: "O+", "A-", "B+"...

@dataclass(frozen=True)
class HistorialMedico(ObjetoValor):
    """Representa el historial médico de un paciente anonimizando sus datos."""
    identificador: IdentificadorAnonimo
    condiciones: list[str]  # Lista de enfermedades o condiciones previas
    alergias: list[str]  # Lista de alergias
