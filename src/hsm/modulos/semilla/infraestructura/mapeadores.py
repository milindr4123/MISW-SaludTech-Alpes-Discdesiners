""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from hsm.seedwork.dominio.repositorios import Mapeador
from hsm.seedwork.infraestructura.utils import unix_time_millis
from hsm.modulos.semilla.dominio.objetos_valor import Length, Formato
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.modulos.semilla.dominio.eventos import  SemillaCreada

from .dto import Semilla as SemillaDTO

from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosSemilla(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            SemillaCreada: self._entidad_a_semilla_creada,
       
        }

    def obtener_tipo(self) -> type:
        return  SemillaCreada.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_semilla_creada(self, entidad:  SemillaCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import SemillaCreadaPayload, EventoSemillaCreada

            payload = SemillaCreadaPayload(
               
                seed=str(evento.seed), 
                estado=str(evento.estado), 
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoSemillaCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'SemillaCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'HSM'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)       

   
    def entidad_a_dto(self, entidad: SemillaCreada, version=LATEST_VERSION) -> SemillaDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: SemillaDTO, version=LATEST_VERSION) -> Semilla:
        raise NotImplementedError


class MapeadorSemilla(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

   

    def obtener_tipo(self) -> type:
        return Semilla.__class__

    def entidad_a_dto(self, entidad: Semilla) -> SemillaDTO:
        
        semilla_dto = SemillaDTO()
        semilla_dto.fecha_creacion = entidad.fecha_creacion
        semilla_dto.fecha_actualizacion = entidad.fecha_actualizacion
        semilla_dto.id = str(entidad.id)

        return semilla_dto

    def dto_a_entidad(self, dto: SemillaDTO) -> Semilla:
        semilla = Semilla(dto.seed, dto.fecha_creacion, dto.fecha_actualizacion)
   

       
        
        return semilla