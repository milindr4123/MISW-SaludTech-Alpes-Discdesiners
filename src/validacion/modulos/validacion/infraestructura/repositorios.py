""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de tokenización

"""

from validacion.config.db import db
from validacion.modulos.validacion.dominio.repositorios import RepositorioValidacion
from validacion.modulos.validacion.dominio.entidades import Validacion
from validacion.modulos.validacion.dominio.fabricas import FabricaValidacion
from .dto import Validacion as ValidacionDTO
from .mapeadores import MapeadorToken
from uuid import UUID

class RepositorioValidacionSQLite(RepositorioValidacion):

    def __init__(self):
        self._fabrica_validacion: FabricaValidacion = FabricaValidacion()

    @property
    def fabrica_validacion(self):
        return self._fabrica_validacion

    def obtener_por_id(self, id: UUID) -> Validacion:
        validacion_dto = db.session.query(ValidacionDTO).filter_by(id=str(id)).one()
        return self.fabrica_validacion.crear_objeto(validacion_dto, MapeadorToken())

    def obtener_todos(self) -> list[Validacion]:
        tokens_dto = db.session.query(ValidacionDTO).all()
        return [self.fabrica_validacion.crear_objeto(validacion_dto, MapeadorToken()) for validacion_dto in tokens_dto]

    def agregar(self, token: Validacion):
        validacion_dto = self.fabrica_validacion.crear_objeto(token, MapeadorToken())
        db.session.add(validacion_dto)
        db.session.commit()

    def actualizar(self, token: Validacion):
        validacion_dto = self.fabrica_validacion.crear_objeto(token, MapeadorToken())
        db.session.merge(validacion_dto)
        db.session.commit()

    def eliminar(self, token_id: UUID):
        validacion_dto = db.session.query(ValidacionDTO).filter_by(id=str(token_id)).one()
        db.session.delete(validacion_dto)
        db.session.commit()

