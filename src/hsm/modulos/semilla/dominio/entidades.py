"""Entidades del dominio de hsm

En este archivo usted encontrará las entidades del dominio de hsm
"""

from __future__ import annotations
from dataclasses import dataclass, field
from hsm.modulos.semilla.dominio.eventos import SemillaCreada
import hsm.modulos.semilla.dominio.objetos_valor as ov
from hsm.seedwork.dominio.entidades import Entidad, AgregacionRaiz

@dataclass
class Semilla(Entidad):
    """Representa un generador de semillas con parámetros específicos en el dominio de semilla."""
   
    length: ov.Length = field(default_factory=lambda: ov.Length(32))
    format: ov.Formato = field(default_factory=lambda: ov.Formato("hex"))

@dataclass
class Semilla(AgregacionRaiz):
    length: ov.Length = field(default_factory=lambda: ov.Length(32))
    format: ov.Formato = field(default_factory=lambda: ov.Formato("hex"))

    def crear_semilla(self, semilla: Semilla):
        self.length = semilla.length
        self.format = semilla.format

        self.agregar_evento(SemillaCreada(id_reserva=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
            # TODO Agregar evento de compensación