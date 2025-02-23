from hsm.seedwork.aplicacion.dto import Mapeador as AppMap
from hsm.seedwork.dominio.repositorios import Mapeador as RepMap
from hsm.modulos.semilla.dominio.entidades import Semilla
from .dto import SemillaDTO

class MapeadorSemillaDTOJson(AppMap):
   
    def externo_a_dto(self, externo: dict) -> SemillaDTO:
        "Convierte un diccionario JSON a un objeto DTO"
        length = externo.get("length")  
        formato = externo.get("formato")  
        return SemillaDTO(length=length, formato=formato)

    def dto_a_externo(self, dto: SemillaDTO) -> dict:
        "Convierte un DTO a un diccionario JSON"
        return dto.__dict__

class MapeadorSemilla(RepMap):    
    "Devuelve la clase que maneja este mapeador"
    def obtener_tipo(self) -> type:
        return Semilla.__class__
        

    def entidad_a_dto(self) -> SemillaDTO:
        "Convierte una entidad Semilla a un DTO"
        length = "32"
        formato = "hex"
        return SemillaDTO(length=length, formato=formato)

    def dto_a_entidad(self, dto: SemillaDTO) -> Semilla:
        "Convierte un DTO a una entidad Semilla"
        semilla = Semilla()       
        semilla.length = dto.length
        semilla.format = dto.formato
        return semilla



