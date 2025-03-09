""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de tokenización

"""

from tokenizacion.config.db import db
from tokenizacion.modulos.tokenizacion.dominio.repositorios import RepositorioTokenizacion
from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from tokenizacion.modulos.tokenizacion.dominio.fabricas import FabricaTokenizacion
from .dto import Tokenizacion as TokenizacionDTO
from .mapeadores import MapeadorToken
from uuid import UUID

class RepositorioTokenizacionSQLite(RepositorioTokenizacion):

    def __init__(self):
        self._fabrica_tokenizacion: FabricaTokenizacion = FabricaTokenizacion()

    @property
    def fabrica_tokenizacion(self):
        return self._fabrica_tokenizacion

    def obtener_por_id(self, id: UUID) -> Tokenizacion:
        tokenizacion_dto = db.session.query(TokenizacionDTO).filter_by(id=str(id)).one()
        return self.fabrica_tokenizacion.crear_objeto(tokenizacion_dto, MapeadorToken())

    def obtener_todos(self) -> list[Tokenizacion]:
        tokens_dto = db.session.query(TokenizacionDTO).all()
        return [self.fabrica_tokenizacion.crear_objeto(tokenizacion_dto, MapeadorToken()) for tokenizacion_dto in tokens_dto]

    def agregar(self, token: Tokenizacion):
        tokenizacion_dto = self.fabrica_tokenizacion.crear_objeto(token, MapeadorToken())
        db.session.add(tokenizacion_dto)
        db.session.commit()

    def actualizar(self, token: Tokenizacion):
        tokenizacion_dto = self.fabrica_tokenizacion.crear_objeto(token, MapeadorToken())
        db.session.merge(tokenizacion_dto)
        db.session.commit()

    def eliminar(self, token_id: UUID):
        tokenizacion_dto = db.session.query(TokenizacionDTO).filter_by(id=str(token_id)).one()
        db.session.delete(tokenizacion_dto)
        db.session.commit()

