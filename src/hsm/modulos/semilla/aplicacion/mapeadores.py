from hsm.seedwork.aplicacion.dto import Mapeador as AppMap
from hsm.seedwork.dominio.repositorios import Mapeador as RepMap
from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.modulos.semilla.dominio.objetos_valor import Formato, Length
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
        

    def entidad_a_dto(self) -> SemillaDTO:
        length = "32"
        formato = "hex"
        return SemillaDTO(length=length, formato=formato)

    def dto_a_entidad(self, dto: SemillaDTO) -> Semilla:
        semilla = Semilla()       
        semilla.length = dto.length
        semilla.format = dto.formato
        return semilla



