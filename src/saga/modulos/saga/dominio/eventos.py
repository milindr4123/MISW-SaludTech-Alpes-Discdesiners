from dataclasses import dataclass
from datetime import datetime

@dataclass
class AnonimizationSucceeded:
    imagen_id: str
    token: str
    timestamp: datetime = datetime.now()

@dataclass
class TokenizationFailed:
    imagen_id: str
    error: str
    timestamp: datetime = datetime.now()