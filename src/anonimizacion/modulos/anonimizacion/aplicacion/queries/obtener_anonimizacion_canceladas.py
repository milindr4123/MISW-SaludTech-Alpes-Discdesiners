from anonimizacion.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from anonimizacion.modulos.anonimizacion.infraestructura.repositorios import RepositorioAnonimizacion
from anonimizacion.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacion
from .base import AnonimizacionQueryBaseHandler
from dataclasses import dataclass

@dataclass
class ObtenerAnonimizacionCancelados(Query):
    ...

class ObtenerAnonimizacionCanceladosHandler(AnonimizacionQueryBaseHandler):

    def handle(self, query: ObtenerAnonimizacionCancelados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioAnonimizacion.__class__)
        anonimizacion_cancelados = repositorio.obtener_anonimizacion_cancelados()
        anonimizacion_dto = [self.fabrica_anonimizacion.crear_objeto(anonimizacion, MapeadorAnonimizacion()) for anonimizacion in anonimizacion_cancelados]
        return QueryResultado(resultado=anonimizacion_dto)