""" Mapeadores para la capa de infraestructura del dominio de tokenización

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from tokenizacion.modulos.tokenizacion.dominio.eventos import TokenizacionFallida, TokenizacionCreada, TokenizacionAprobada, EventoTokenizacion
from tokenizacion.modulos.tokenizacion.infraestructura.despachadores import unix_time_millis
from tokenizacion.seedwork.dominio.repositorios import Mapeador
from tokenizacion.modulos.tokenizacion.dominio.entidades import Tokenizacion
from .dto import Tokenizacion as TokenizacionDTO

from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosTokenizacion(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            TokenizacionCreada: self._entidad_a_anonimizaacion_creada,
            TokenizacionAprobada: self._entidad_a_anonimizaacion_aprobada,
            TokenizacionFallida: self._entidad_a_anonimizaacion_cancelada
        }

    def obtener_tipo(self) -> type:
        return EventoTokenizacion.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_anonimizaacion_creada(self, entidad: TokenizacionCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import TokenizacionCreadoPayload, EventoTokenizacionCreado

            payload = TokenizacionCreadoPayload(
                id_reserva=str(evento.id_reserva), 
                id_paciente=str(evento.id_paciente), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoTokenizacionCreado(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'ReservaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'tokenizacion'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

    def _entidad_a_anonimizaacion_aprobada(self, entidad: TokenizacionAprobada, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entidad_a_anonimizaacion_cancelada(self, entidad: TokenizacionFallida, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entidad_a_dto(self, entidad: EventoTokenizacion, version=LATEST_VERSION) -> TokenizacionDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: TokenizacionDTO, version=LATEST_VERSION) -> Tokenizacion:
        raise NotImplementedError



class MapeadorToken(Mapeador):
    def entidad_a_dto(self, entidad: Tokenizacion) -> TokenizacionDTO:
        tokenizacion_dto = TokenizacionDTO()
        tokenizacion_dto.id_solicitud = str(entidad.id_solicitud)
        tokenizacion_dto.id_paciente = entidad.id_paciente
        tokenizacion_dto.estado = entidad.estado
        tokenizacion_dto.token_anonimo = entidad.token_anonimo
        tokenizacion_dto.fecha_creacion = entidad.fecha_creacion 
        return tokenizacion_dto

    def dto_a_entidad(self, dto: TokenizacionDTO) -> Tokenizacion:
        tokenizacion = Tokenizacion(
            id=dto.id,
            id_solicitud=dto.id_solicitud,
            id_paciente=dto.id_paciente,
            estado = dto.estado,
            token_anonimo = dto.token_anonimo,
            fecha_creacion=dto.fecha_creacion
        )
        return tokenizacion

    

    def obtener_tipo(self) -> type:
        return Tokenizacion.__class__
    
