from hsm.seedwork.aplicacion.dto import Mapeador as AppMap
from hsm.seedwork.dominio.repositorios import Mapeador as RepMap
from hsm.modulos.semilla.dominio.entidades import 
from hsm.modulos.semilla.dominio.objetos_valor import 
from .dto import SemillaDTO

from datetime import datetime

class MapeadorSemillaDTOJson(AppMap):
   
    def externo_a_dto(self, externo: dict) -> SemillaDTO:
        semilla_dto = SemillaDTO()   
        semilla_dto.length  
        semilla_dto.formato     
      return semilla_dto

    def dto_a_externo(self, dto: SemillaDTO) -> dict:
        return dto.__dict__

class MapeadorSemilla(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Semilla.__class__
        

    def entidad_a_dto(self, entidad: Semilla) -> SemillaDTO:
        
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)               
        return SemillaDTO(fecha_creacion, fecha_actualizacion, _id, itinerarios)

    def dto_a_entidad(self, dto: ReservaDTO) -> Reserva:
        semilla = Semilla()            
        return reserva



