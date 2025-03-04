from validacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from validacion.seedwork.aplicacion.queries import ejecutar_query as query
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioTokens
from dataclasses import dataclass
from .base import TokenQueryBaseHandler
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorToken
import uuid

@dataclass
class ObtenerToken(Query):
    id: str

class ObtenerTokenHandler(TokenQueryBaseHandler):

    def handle(self, query: ObtenerToken) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)
        token = self.fabrica_tokens.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorToken())
        return QueryResultado(resultado=token)

@query.register(ObtenerToken)
def ejecutar_query_obtener_token(query: ObtenerToken):
    handler = ObtenerTokenHandler()
    return handler.handle(query)