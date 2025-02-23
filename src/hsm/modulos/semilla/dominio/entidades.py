"""Entidades del dominio de hsm

En este archivo usted encontrará las entidades del dominio de hsm
"""

from __future__ import annotations
from dataclasses import dataclass, field

import hsm.modulos.semilla.dominio.objetos_valor as ov
from hsm.seedwork.dominio.entidades import Entidad

@dataclass
class Semilla(Entidad):
    """Representa un generador de semillas con parámetros específicos en el dominio de semilla."""
   
    length: ov.Length = field(default_factory=lambda: ov.Length(32))
    format: ov.Formato = field(default_factory=lambda: ov.Formato("hex"))