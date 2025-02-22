"""Entidades del dominio de hsm

En este archivo usted encontrará las entidades del dominio de hsm
"""

from __future__ import annotations
from dataclasses import dataclass, field

import hsm.modulos.hsm.dominio.objetos_valor as ov
from aeroalpes.seedwork.dominio.entidades import Entidad

@dataclass
class Semilla(Entidad):
    """Representa un generador de semillas con parámetros específicos en el dominio de vuelos."""
   
    length: ov.Longitud = field(default_factory=lambda: ov.Longitud(32))
    format: ov.Formato = field(default_factory=lambda: ov.Formato("hex"))