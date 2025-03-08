""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de tokenización

"""

from hsm.config.db import db
from hsm.modulos.hsm.dominio.repositorios import RepositorioHsm
from hsm.modulos.hsm.dominio.entidades import Hsm
from hsm.modulos.hsm.dominio.fabricas import FabricaHsm
from .dto import Hsm as HsmDTO
from .mapeadores import MapeadorToken
from uuid import UUID

class RepositorioHsmSQLite(RepositorioHsm):

    def __init__(self):
        self._fabrica_hsm: FabricaHsm = FabricaHsm()

    @property
    def fabrica_hsm(self):
        return self._fabrica_hsm

    def obtener_por_id(self, id: UUID) -> Hsm:
        hsm_dto = db.session.query(HsmDTO).filter_by(id=str(id)).one()
        return self.fabrica_hsm.crear_objeto(hsm_dto, MapeadorToken())

    def obtener_todos(self) -> list[Hsm]:
        tokens_dto = db.session.query(HsmDTO).all()
        return [self.fabrica_hsm.crear_objeto(hsm_dto, MapeadorToken()) for hsm_dto in tokens_dto]

    def agregar(self, token: Hsm):
        hsm_dto = self.fabrica_hsm.crear_objeto(token, MapeadorToken())
        db.session.add(hsm_dto)
        db.session.commit()

    def actualizar(self, token: Hsm):
        hsm_dto = self.fabrica_hsm.crear_objeto(token, MapeadorToken())
        db.session.merge(hsm_dto)
        db.session.commit()

    def eliminar(self, token_id: UUID):
        hsm_dto = db.session.query(HsmDTO).filter_by(id=str(token_id)).one()
        db.session.delete(hsm_dto)
        db.session.commit()

