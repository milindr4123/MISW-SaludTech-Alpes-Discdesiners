from hsm.seedwork.aplicacion.dto import Mapeador as AppMap
from hsm.seedwork.dominio.repositorios import Mapeador as RepMap
from hsm.modulos.semilla.dominio.entidades import Semilla
from .dto import SemillaDTO

class MapeadorSemillaDTOJson(AppMap):
   
    def externo_a_dto(self) -> SemillaDTO:
        semilla_dto = SemillaDTO()   
        semilla_dto.length  
        semilla_dto.formato   
        return semilla_dto

    def dto_a_externo(self, dto: SemillaDTO) -> dict:
        return dto.__dict__

class MapeadorSemilla(RepMap):
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



