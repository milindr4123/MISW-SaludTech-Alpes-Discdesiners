from hsm.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from hsm.seedwork.aplicacion.queries import ejecutar_query as query
from hsm.modulos.hsm.infraestructura.repositorios import RepositorioHsm
from dataclasses import dataclass
from .base import HsmQueryBaseHandler
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsm
import uuid

@dataclass
class ObtenerHsm(Query):
    id: str

class ObtenerHsmHandler(HsmQueryBaseHandler):

    def handle(self, query: ObtenerHsm) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioHsm.__class__)
        hsm = self.fabrica_hsm.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorHsm())
        return QueryResultado(resultado=hsm)

@query.register(ObtenerHsm)
def ejecutar_query_obtener_hsm(query: ObtenerHsm):
    handler = ObtenerHsmHandler()
    return handler.handle(query)