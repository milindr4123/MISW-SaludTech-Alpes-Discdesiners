"""DTOs para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de tokenización

"""

from saga.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla tokens y usuarios

class Anonimizacion(db.Model):
    __tablename__ = "anonimizaciones"
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_solicitud = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_paciente = db.Column(db.String(255), nullable=False)
    token_anonimo = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(255), nullable=False)

class ReservaAnonimizacion(db.Model):
    __tablename__ = "anonimizaciones_reservas"
    fecha_creacion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)