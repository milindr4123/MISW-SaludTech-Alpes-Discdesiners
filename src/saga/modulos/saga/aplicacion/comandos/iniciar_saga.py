from dataclasses import dataclass
from datetime import datetime

@dataclass
class IniciarSaga:
    imagen_id: str
    datos_imagen: dict
    timestamp: datetime = datetime.now()