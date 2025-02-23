"""DTOs para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de tokenización

"""

from tokenizacion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla tokens y usuarios
tokens_usuarios = db.Table(
    "tokens_usuarios",
    db.Model.metadata,
    db.Column("token_id", db.String, db.ForeignKey("tokens.id")),
    db.Column("usuario_id", db.String, db.ForeignKey("usuarios.id")),
    db.Column("fecha_asignacion", db.DateTime),
)

class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_paciente = db.Column(db.String, nullable=False)
    token_anonimo = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    
    
class DetalleToken(db.Model):
    __tablename__ = "detalles_tokens"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    id_paciente = db.Column(db.String, nullable=False)
    token_anonimo = db.Column(db.String, nullable=False)
    fecha_revocacion = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    