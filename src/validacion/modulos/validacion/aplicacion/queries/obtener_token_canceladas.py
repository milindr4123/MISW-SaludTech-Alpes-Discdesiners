from validacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioTokens
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorToken
from .base import TokenQueryBaseHandler
from dataclasses import dataclass

@dataclass
class ObtenerTokensCancelados(Query):
    ...

class ObtenerTokensCanceladosHandler(TokenQueryBaseHandler):

    def handle(self, query: ObtenerTokensCancelados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokens.__class__)
        tokens_cancelados = repositorio.obtener_tokens_cancelados()
        tokens_dto = [self.fabrica_tokens.crear_objeto(token, MapeadorToken()) for token in tokens_cancelados]
        return QueryResultado(resultado=tokens_dto)