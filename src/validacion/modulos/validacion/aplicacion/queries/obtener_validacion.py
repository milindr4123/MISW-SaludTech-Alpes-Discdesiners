from validacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from validacion.seedwork.aplicacion.queries import ejecutar_query as query
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioValidacion
from dataclasses import dataclass
from .base import ValidacionQueryBaseHandler
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacion
import uuid

@dataclass
class ObtenerValidacion(Query):
    id: str

class ObtenerValidacionHandler(ValidacionQueryBaseHandler):

    def handle(self, query: ObtenerValidacion) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion.__class__)
        validacion = self.fabrica_validacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorValidacion())
        return QueryResultado(resultado=validacion)

@query.register(ObtenerValidacion)
def ejecutar_query_obtener_validacion(query: ObtenerValidacion):
    handler = ObtenerValidacionHandler()
    return handler.handle(query)