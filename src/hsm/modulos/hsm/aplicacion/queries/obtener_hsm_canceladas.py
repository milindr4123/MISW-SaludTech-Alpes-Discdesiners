from hsm.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from hsm.modulos.hsm.infraestructura.repositorios import RepositorioHsm
from hsm.modulos.hsm.aplicacion.mapeadores import MapeadorHsm
from .base import HsmQueryBaseHandler
from dataclasses import dataclass

@dataclass
class ObtenerHsmCancelados(Query):
    ...

class ObtenerHsmCanceladosHandler(HsmQueryBaseHandler):

    def handle(self, query: ObtenerHsmCancelados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioHsm.__class__)
        hsm_cancelados = repositorio.obtener_hsm_cancelados()
        hsm_dto = [self.fabrica_hsm.crear_objeto(hsm, MapeadorHsm()) for hsm in hsm_cancelados]
        return QueryResultado(resultado=hsm_dto)