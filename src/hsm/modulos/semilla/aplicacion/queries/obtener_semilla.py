from hsm.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from hsm.seedwork.aplicacion.queries import ejecutar_query as query
from hsm.modulos.semilla.infraestructura.repositorios import RepositorioSemilla
from dataclasses import dataclass
from .base import SemillaQueryBaseHandler
from hsm.modulos.semilla.aplicacion.mapeadores import MapeadorReserva
import uuid

@dataclass
class ObtenerSemilla(Query):
    id: str

class ObtenerReservaHandler(SemillaQueryBaseHandler):

    def handle(self, query: ObtenerSemilla) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioSemilla.__class__)
        semilla =  self.fabrica_semillas.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorReserva())
        return QueryResultado(resultado=semilla)

@query.register(ObtenerReserva)
def ejecutar_query_obtener_reserva(query: ObtenerReserva):
    handler = ObtenerReservaHandler()
    return handler.handle(query)