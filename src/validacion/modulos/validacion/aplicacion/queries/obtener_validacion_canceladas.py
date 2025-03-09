from validacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from validacion.modulos.validacion.infraestructura.repositorios import RepositorioValidacion
from validacion.modulos.validacion.aplicacion.mapeadores import MapeadorValidacion
from .base import ValidacionQueryBaseHandler
from dataclasses import dataclass

@dataclass
class ObtenerValidacionCancelados(Query):
    ...

class ObtenerValidacionCanceladosHandler(ValidacionQueryBaseHandler):

    def handle(self, query: ObtenerValidacionCancelados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioValidacion.__class__)
        validacion_cancelados = repositorio.obtener_validacion_cancelados()
        validacion_dto = [self.fabrica_validacion.crear_objeto(validacion, MapeadorValidacion()) for validacion in validacion_cancelados]
        return QueryResultado(resultado=validacion_dto)