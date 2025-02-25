"""Entidades reusables parte del seedwork del proyecto

En este archivo usted encontrará las clases para eventos reusables parte del seedwork del proyecto

"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class EventoDominio():
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    fecha_evento: datetime =  field(default=datetime.now())


    @classmethod
    def siguiente_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id
