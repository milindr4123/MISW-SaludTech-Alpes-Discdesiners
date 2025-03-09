""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from validacion.modulos.validacion.dominio.eventos import ValidacionFallida, ValidacionCreada, ValidacionAprobada, EventoValidacion
from validacion.modulos.validacion.infraestructura.despachadores import unix_time_millis
from validacion.seedwork.dominio.repositorios import Mapeador
from validacion.modulos.validacion.dominio.entidades import Validacion
from .dto import Validacion as ValidacionDTO

from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosValidacion(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            ValidacionCreada: self._entidad_a_anonimizaacion_creada,
            ValidacionAprobada: self._entidad_a_anonimizaacion_aprobada,
            ValidacionFallida: self._entidad_a_anonimizaacion_cancelada
        }

    def obtener_tipo(self) -> type:
        return EventoValidacion.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_anonimizaacion_creada(self, entidad: ValidacionCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import ValidacionCreadoPayload, EventoValidacionCreado

            payload = ValidacionCreadoPayload(
                id_reserva=str(evento.id_reserva), 
                id_paciente=str(evento.id_paciente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoValidacionCreado(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ReservaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'validacion'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_anonimizaacion_aprobada(self, entidad: ValidacionAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_anonimizaacion_cancelada(self, entidad: ValidacionFallida, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoValidacion, version=LATEST_VERSION) -> ValidacionDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: ValidacionDTO, version=LATEST_VERSION) -> Validacion:
        raise NotImplementedError



class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Validacion) -> ValidacionDTO:
        validacion_dto = ValidacionDTO()
        validacion_dto.id_solicitud = str(entidad.id_solicitud)
        validacion_dto.id_paciente = entidad.id_paciente
        validacion_dto.estado = entidad.estado
        validacion_dto.token_anonimo = entidad.token_anonimo
        validacion_dto.fecha_creacion = entidad.fecha_creacion 
        return validacion_dto

    def dto_a_entidad(self, dto: ValidacionDTO) -> Validacion:
        validacion = Validacion(
            id=dto.id,
            id_solicitud=dto.id_solicitud,
            id_paciente=dto.id_paciente,
            estado = dto.estado,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return validacion

    

    def obtener_tipo(self) -> type:
        return Validacion.__class__
    
