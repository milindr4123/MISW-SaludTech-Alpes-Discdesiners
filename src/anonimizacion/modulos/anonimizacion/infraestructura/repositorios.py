""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de tokenización

"""

from anonimizacion.config.db import db
from anonimizacion.modulos.anonimizacion.dominio.repositorios import RepositorioAnonimizacion
from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from anonimizacion.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from .dto import Anonimizacion as AnonimizacionDTO
from .mapeadores import MapeadorToken
from uuid import UUID

class RepositorioAnonimizacionSQLite(RepositorioAnonimizacion):

    def __init__(self):
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion

    def obtener_por_id(self, id: UUID) -> Anonimizacion:
        anonimizacion_dto = db.session.query(AnonimizacionDTO).filter_by(id=str(id)).one()
        return self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorToken())

    def obtener_todos(self) -> list[Anonimizacion]:
        tokens_dto = db.session.query(AnonimizacionDTO).all()
        return [self.fabrica_anonimizacion.crear_objeto(anonimizacion_dto, MapeadorToken()) for anonimizacion_dto in tokens_dto]

    def agregar(self, token: Anonimizacion):
        anonimizacion_dto = self.fabrica_anonimizacion.crear_objeto(token, MapeadorToken())
        db.session.add(anonimizacion_dto)
        db.session.commit()

    def actualizar(self, token: Anonimizacion):
        anonimizacion_dto = self.fabrica_anonimizacion.crear_objeto(token, MapeadorToken())
        db.session.merge(anonimizacion_dto)
        db.session.commit()

    def eliminar(self, token_id: UUID):
        anonimizacion_dto = db.session.query(AnonimizacionDTO).filter_by(id=str(token_id)).one()
        db.session.delete(anonimizacion_dto)
        db.session.commit()

