""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from hsm.modulos.hsm.dominio.eventos import HsmFallida, HsmCreada, HsmAprobada, EventoHsm
from hsm.modulos.hsm.infraestructura.despachadores import unix_time_millis
from hsm.seedwork.dominio.repositorios import Mapeador
from hsm.modulos.hsm.dominio.entidades import Hsm
from .dto import Hsm as HsmDTO

from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosHsm(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            HsmCreada: self._entidad_a_anonimizaacion_creada,
            HsmAprobada: self._entidad_a_anonimizaacion_aprobada,
            HsmFallida: self._entidad_a_anonimizaacion_cancelada
        }

    def obtener_tipo(self) -> type:
        return EventoHsm.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_anonimizaacion_creada(self, entidad: HsmCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import HsmCreadoPayload, EventoHsmCreado

            payload = HsmCreadoPayload(
                id_reserva=str(evento.id_reserva), 
                id_paciente=str(evento.id_paciente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoHsmCreado(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ReservaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'hsm'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_anonimizaacion_aprobada(self, entidad: HsmAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_anonimizaacion_cancelada(self, entidad: HsmFallida, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoHsm, version=LATEST_VERSION) -> HsmDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: HsmDTO, version=LATEST_VERSION) -> Hsm:
        raise NotImplementedError



class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Hsm) -> HsmDTO:
        hsm_dto = HsmDTO()
        hsm_dto.id_solicitud = str(entidad.id_solicitud)
        hsm_dto.id_paciente = entidad.id_paciente
        hsm_dto.estado = entidad.estado
        hsm_dto.token_anonimo = entidad.token_anonimo
        hsm_dto.fecha_creacion = entidad.fecha_creacion 
        return hsm_dto

    def dto_a_entidad(self, dto: HsmDTO) -> Hsm:
        hsm = Hsm(
            id=dto.id,
            id_solicitud=dto.id_solicitud,
            id_paciente=dto.id_paciente,
            estado = dto.estado,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return hsm

    

    def obtener_tipo(self) -> type:
        return Hsm.__class__
    
