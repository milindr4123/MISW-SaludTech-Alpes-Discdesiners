from tokenizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from tokenizacion.modulos.tokenizacion.infraestructura.repositorios import RepositorioTokenizacion
from tokenizacion.modulos.tokenizacion.aplicacion.mapeadores import MapeadorTokenizacion
from .base import TokenizacionQueryBaseHandler
from dataclasses import dataclass

@dataclass
class ObtenerTokenizacionCancelados(Query):
    ...

class ObtenerTokenizacionCanceladosHandler(TokenizacionQueryBaseHandler):

    def handle(self, query: ObtenerTokenizacionCancelados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTokenizacion.__class__)
        tokenizacion_cancelados = repositorio.obtener_tokenizacion_cancelados()
        tokenizacion_dto = [self.fabrica_tokenizacion.crear_objeto(tokenizacion, MapeadorTokenizacion()) for tokenizacion in tokenizacion_cancelados]
        return QueryResultado(resultado=tokenizacion_dto)