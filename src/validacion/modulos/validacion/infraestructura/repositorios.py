""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de tokenización

"""

from validacion.config.db import db
from validacion.modulos.validacion.dominio.repositorios import RepositorioTokens
from validacion.modulos.validacion.dominio.entidades import Token
from validacion.modulos.validacion.dominio.fabricas import FabricaTokenizacion
from .dto import Token as TokenDTO
from .mapeadores import MapeadorToken
from uuid import UUID

class RepositorioTokensSQLite(RepositorioTokens):

    def __init__(self):
        self._fabrica_validacion: FabricaTokenizacion = FabricaTokenizacion()

    @property
    def fabrica_validacion(self):
        return self._fabrica_validacion

    def obtener_por_id(self, id: UUID) -> Token:
        token_dto = db.session.query(TokenDTO).filter_by(id=str(id)).one()
        return self.fabrica_validacion.crear_objeto(token_dto, MapeadorToken())

    def obtener_todos(self) -> list[Token]:
        tokens_dto = db.session.query(TokenDTO).all()
        return [self.fabrica_validacion.crear_objeto(token_dto, MapeadorToken()) for token_dto in tokens_dto]

    def agregar(self, token: Token):
        token_dto = self.fabrica_validacion.crear_objeto(token, MapeadorToken())
        db.session.add(token_dto)
        db.session.commit()

    def actualizar(self, token: Token):
        token_dto = self.fabrica_validacion.crear_objeto(token, MapeadorToken())
        db.session.merge(token_dto)
        db.session.commit()

    def eliminar(self, token_id: UUID):
        token_dto = db.session.query(TokenDTO).filter_by(id=str(token_id)).one()
        db.session.delete(token_dto)
        db.session.commit()

