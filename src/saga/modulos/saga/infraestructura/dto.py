"""DTOs para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de tokenización

"""

from saga.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, func

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla tokens y usuarios

class SagaState(db.Model):
    __tablename__ = "saga_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String(255))
    step = Column(String(255))
    event_time = Column(DateTime, default=func.now())