from tokenizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from tokenizacion.seedwork.aplicacion.queries import ejecutar_query as query
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokenizacion
from dataclasses import dataclass
from .base import TokenizacionQueryBaseHandler
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacion
import uuid

@dataclass
class ObtenerTokenizacion(Query):
    id: str

class ObtenerTokenizacionHandler(TokenizacionQueryBaseHandler):

    def handle(self, query: ObtenerTokenizacion) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokenizacion.__class__)
        tokenizacion = self.fabrica_tokenizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorTokenizacion())
        return QueryResultado(resultado=tokenizacion)

@query.register(ObtenerTokenizacion)
def ejecutar_query_obtener_tokenizacion(query: ObtenerTokenizacion):
    handler = ObtenerTokenizacionHandler()
    return handler.handle(query)