""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from anonimizacion.modulos.anonimizacion.dominio.eventos import AnonimizacionFallida, AnonimizacionCreada, AnonimizacionAprobada, EventoAnonimizacion
from anonimizacion.seedwork.infraestructura.timeUtils import unix_time_millis
from anonimizacion.seedwork.dominio.repositorios import Mapeador
from anonimizacion.modulos.anonimizacion.dominio.entidades import Anonimizacion
from .dto import Anonimizacion as AnonimizacionDTO

from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosAnonimizacion(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            AnonimizacionCreada: self._entidad_a_anonimizaacion_creada,
            AnonimizacionAprobada: self._entidad_a_anonimizaacion_aprobada,
            AnonimizacionFallida: self._entidad_a_anonimizaacion_cancelada
        }

    def obtener_tipo(self) -> type:
        return EventoAnonimizacion.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_anonimizaacion_creada(self, entidad: AnonimizacionCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import AnonimizacionCreadoPayload, EventoAnonimizacionCreado

            payload = AnonimizacionCreadoPayload(
                id_reserva=str(evento.id_reserva), 
                id_paciente=str(evento.id_paciente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoAnonimizacionCreado(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ReservaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'anonimizacion'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_anonimizaacion_aprobada(self, entidad: AnonimizacionAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_anonimizaacion_cancelada(self, entidad: AnonimizacionFallida, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoAnonimizacion, version=LATEST_VERSION) -> AnonimizacionDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: AnonimizacionDTO, version=LATEST_VERSION) -> Anonimizacion:
        raise NotImplementedError



class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Anonimizacion) -> AnonimizacionDTO:
        anonimizacion_dto = AnonimizacionDTO()
        anonimizacion_dto.id_solicitud = str(entidad.id_solicitud)
        anonimizacion_dto.id_paciente = entidad.id_paciente
        anonimizacion_dto.estado = entidad.estado
        anonimizacion_dto.token_anonimo = entidad.token_anonimo
        anonimizacion_dto.fecha_creacion = entidad.fecha_creacion 
        return anonimizacion_dto

    def dto_a_entidad(self, dto: AnonimizacionDTO) -> Anonimizacion:
        anonimizacion = Anonimizacion(
            id=dto.id,
            id_solicitud=dto.id_solicitud,
            id_paciente=dto.id_paciente,
            estado = dto.estado,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return anonimizacion

    

    def obtener_tipo(self) -> type:
        return Anonimizacion.__class__
    
