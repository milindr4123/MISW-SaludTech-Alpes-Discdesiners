""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from hsm.config.db import db
from hsm.modulos.semilla.dominio.repositorios import RepositorioSemilla,RepositorioEventosSemilla
from hsm.modulos.semilla.dominio.objetos_valor import Formato,Length
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.modulos.semilla.dominio.fabricas import _FabricaSemilla
from .dto import Semilla as SemillaDTO
from .dto import EventosSemilla
from .mapeadores import MapeadorSemilla, MapadeadorEventosSemilla
from uuid import UUID
from pulsar.schema import *




class RepositorioSemillaSQLAlchemy(RepositorioSemilla):

    def __init__(self):
        self._fabrica_semillas: _FabricaSemilla = _FabricaSemilla()

    @property
    def fabrica_semillas(self):
        return self._fabrica_semillas

    def obtener_por_id(self, id: UUID) -> Semilla:
        semilla_dto = db.session.query(SemillaDTO).filter_by(id=str(id)).one()
        return self.fabrica_semillas.crear_objeto(semilla_dto, MapeadorSemilla())

    def obtener_todos(self) -> list[Semilla]:
        # TODO
        raise NotImplementedError

    def agregar(self, semilla: Semilla):
        semilla_dto = self.fabrica_semillas.crear_objeto(semilla, MapeadorSemilla())

        db.session.add(semilla_dto)

    def actualizar(self, semilla: Semilla):
        # TODO
        raise NotImplementedError

    def eliminar(self, semilla_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosSemillasSQLAlchemy(RepositorioEventosSemilla):

    def __init__(self):
        self._fabrica_semilla: _FabricaSemilla = _FabricaSemilla()

    @property
    def fabrica_semilla(self):
        return self._fabrica_semilla

    def obtener_por_id(self, id: UUID) -> Semilla:
        semilla_dto = db.session.query(SemillaDTO).filter_by(id=str(id)).one()
        return self.fabrica_semilla.crear_objeto(semilla_dto, MapadeadorEventosSemilla())

    def obtener_todos(self) -> list[Semilla]:
        raise NotImplementedError

    def agregar(self, evento):
        semilla_evento = self.fabrica_semilla.crear_objeto(evento, MapadeadorEventosSemilla())

        parser_payload = JsonSchema(semilla_evento.data.__class__)
        json_str = parser_payload.encode(semilla_evento.data)

        evento_dto = EventosSemilla()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_semilla)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(semilla_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(semilla_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, semilla:Semilla):
        raise NotImplementedError

    def eliminar(self, semilla_id: UUID):
        raise NotImplementedError
