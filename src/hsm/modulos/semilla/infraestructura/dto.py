"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from hsm.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()





class Semilla(db.Model):
    __tablename__ = "semillas"
    seed = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(40),nullable =False)

class EventosSemilla(db.Model):
    __tablename__ = "eventos_semilla"
    seed = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

class SemillaAnalitica(db.Model):
    __tablename__ = "analitica_reservas"
    fecha_creacion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)